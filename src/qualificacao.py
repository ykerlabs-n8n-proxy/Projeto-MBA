import csv
import json
import os
from pathlib import Path
from typing import Any
from urllib import error, request


ROOT = Path(__file__).resolve().parent.parent
INPUT_CSV = ROOT / "data" / "leads_preparados.csv"
OUTPUT_CSV = ROOT / "data" / "leads_qualificados.csv"


class LeadQualificado:
    def __init__(self, **data: Any) -> None:
        self.score_qualificacao = data.get("score_qualificacao", "")
        self.categoria_interesse = data.get("categoria_interesse", "")
        self.urgencia = data.get("urgencia", "")
        self.resumo_necessidade = data.get("resumo_necessidade", "")
        self.proxima_acao_sugerida = data.get("proxima_acao_sugerida", "")
        self.justificativa = data.get("justificativa", "")


def _load_env_file(path: Path) -> None:
    if not path.exists():
        return
    lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    for line in lines:
        if line.startswith("#"):
            continue
        if "=" in line:
            key, value = line.split("=", 1)
            os.environ[key.strip()] = value.strip().strip('"').strip("'")
        elif line.startswith("sk-ant-") or line.startswith("ANTHROPIC_API_KEY"):
            os.environ["ANTHROPIC_API_KEY"] = line.strip().replace("ANTHROPIC_API_KEY", "", 1).strip()


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _write_csv_rows(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _load_api_key() -> str:
    if os.getenv("ANTHROPIC_API_KEY"):
        return os.getenv("ANTHROPIC_API_KEY", "")
    env_path = ROOT / ".env"
    if env_path.exists():
        raw = env_path.read_text(encoding="utf-8").strip()
        if raw.startswith("sk-ant-"):
            os.environ["ANTHROPIC_API_KEY"] = raw
            return raw
    return "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"


def qualificar_lead(texto_para_llm: str) -> LeadQualificado:
    api_key = _load_api_key()
    system_prompt = (
        "Você é um especialista em pré-vendas B2B. Analise o lead e classifique com precisão. "
        "REGRA DE OURO: use apenas informações presentes no texto do lead, nunca invente dados."
    )

    tool_schema = {
        "name": "lead_qualificado",
        "description": "Classifica um lead de pré-vendas em um schema estruturado.",
        "input_schema": {
            "type": "object",
            "properties": {
                "score_qualificacao": {"type": "string", "enum": ["quente", "morno", "frio"]},
                "categoria_interesse": {"type": "string"},
                "urgencia": {"type": "string", "enum": ["alta", "media", "baixa"]},
                "resumo_necessidade": {"type": "string"},
                "proxima_acao_sugerida": {"type": "string"},
                "justificativa": {"type": "string"},
            },
            "required": [
                "score_qualificacao",
                "categoria_interesse",
                "urgencia",
                "resumo_necessidade",
                "proxima_acao_sugerida",
                "justificativa",
            ],
        },
    }

    payload = {
        "model": "claude-haiku-4-5",
        "temperature": 0,
        "max_tokens": 500,
        "system": system_prompt,
        "messages": [{"role": "user", "content": texto_para_llm}],
        "tools": [tool_schema],
        "tool_choice": {"type": "tool", "name": "lead_qualificado"},
    }

    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }

    req = request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=120) as response:
            body = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Falha na API Anthropic: {detail}") from exc

    content = body.get("content", [])
    tool_use = None
    for item in content:
        if item.get("type") == "tool_use":
            tool_use = item
            break
    if not tool_use:
        raise RuntimeError(f"Resposta inesperada da Anthropic: {body}")

    return LeadQualificado(**tool_use.get("input", {}))


def processar_todos_leads() -> None:
    rows = _read_csv_rows(INPUT_CSV)
    resultados: list[dict[str, Any]] = []
    total = len(rows)

    for idx, row in enumerate(rows, start=1):
        empresa = row.get("empresa", "")
        print(f"Processando lead {idx}/{total}: {empresa}...")
        classificacao = qualificar_lead(row.get("texto_para_llm", ""))
        resultado = dict(row)
        resultado.update(
            {
                "score_qualificacao": classificacao.score_qualificacao,
                "categoria_interesse": classificacao.categoria_interesse,
                "urgencia": classificacao.urgencia,
                "resumo_necessidade": classificacao.resumo_necessidade,
                "proxima_acao_sugerida": classificacao.proxima_acao_sugerida,
                "justificativa": classificacao.justificativa,
            }
        )
        resultados.append(resultado)

    _write_csv_rows(OUTPUT_CSV, resultados)
    print(f"Arquivo salvo em: {OUTPUT_CSV}")


if __name__ == "__main__":
    processar_todos_leads()
