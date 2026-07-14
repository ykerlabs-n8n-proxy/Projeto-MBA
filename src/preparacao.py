from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
INPUT_CSV = ROOT / "data" / "leads.csv"
OUTPUT_CSV = ROOT / "data" / "leads_preparados.csv"


def main() -> None:
    df = pd.read_csv(INPUT_CSV, encoding="utf-8")

    df = df.copy()
    df = df.dropna(subset=["mensagem_necessidade"])
    df["mensagem_necessidade"] = df["mensagem_necessidade"].astype(str).str.strip()
    df = df[df["mensagem_necessidade"].str.len() >= 10]

    text_columns = ["segmento", "porte", "origem", "cargo", "empresa", "mensagem_necessidade"]
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    for col in ["segmento", "porte", "origem", "cargo", "empresa"]:
        if col in df.columns:
            df[col] = df[col].str.lower()

    df["texto_para_llm"] = (
        "Empresa: " + df["empresa"].astype(str)
        + " | Segmento: " + df["segmento"].astype(str)
        + " | Porte: " + df["porte"].astype(str)
        + " | Cargo: " + df["cargo"].astype(str)
        + " | Origem: " + df["origem"].astype(str)
        + " | Necessidade: " + df["mensagem_necessidade"].astype(str)
    )

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")

    print(f"total_leads_lidos: {len(pd.read_csv(INPUT_CSV, encoding='utf-8'))}")
    print(f"total_apos_limpeza: {len(df)}")
    print("exemplo_texto_para_llm:")
    if not df.empty:
        print(df.iloc[0]["texto_para_llm"])
    else:
        print("<sem dados>")


if __name__ == "__main__":
    main()
