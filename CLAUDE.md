# CLAUDE.md — Projeto Final: Qualificação automática de leads (SDR)

Briefing do projeto — entregue como PDF via Quarto. Leia antes de editar.

## Objetivo

Automatizar a qualificação de leads de pré-vendas (SDR) usando um LLM (Anthropic)
para analisar o conteúdo dos leads (CSV), atribuir score e tags de prioridade, e
gerar recomendações acionáveis para a equipe de vendas.

## Fontes de dados

- Arquivo CSV com os leads (colunas típicas: `nome`, `email`, `telefone`, `empresa`,
  `cargo`, `mensagem`, `origem`, `data_criacao`, etc.).
- Dados derivados gerados por código (ex.: features agregadas, contagem de palavras,
  histórico de interações).

## Metodologia

Seguiremos o fluxo CRISP-DM: Business Understanding → Data Understanding →
Data Preparation → Modeling → Evaluation → Deployment. Cada etapa do paper deve
conter código executável que gera os números e tabelas apresentados.

## Regra de ouro

Nunca inventar números. Todo valor numérico no relatório deve vir de uma execução
de código (chunk/arquivo) que pode ser reexecutado e auditar a fonte dos dados.

## APIs e segredo

Usaremos apenas a API da Anthropic. Coloque a chave em `.env` (veja `.env.example`).
Nunca commit o `.env` no repositório.

## Estrutura mínima do projeto (esperada)

```
.
├── CLAUDE.md
├── README.md
├── .gitignore
├── .env.example
├── requirements.txt
├── data/              # onde o CSV de leads ficará (não comitado se sensível)
├── src/               # código Python: coleta, pré-processamento, modelagem
└── paper/             # arquivos Quarto (.qmd) e templates do paper final
```

## Como criar e ativar o `.venv` (Windows / macOS / Linux)

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1    # ou .\.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Selecionar o interpretador no VS Code

1. Abra o comando: `Ctrl+Shift+P` (ou `Cmd+Shift+P` no macOS).
2. Digite: `Python: Select Interpreter`.
3. Escolha o interpretador apontando para `./.venv/bin/python` (macOS/Linux)
   ou `./.venv\Scripts\python.exe` (Windows).

Após isso, o VS Code usará o `.venv` para executar e depurar código, e para a
instalação de pacotes pelo gerenciador integrado.

## Renderizar o paper final (Quarto → PDF)

Coloque os arquivos `.qmd` em `paper/` e rode:

```bash
quarto render paper/paper.qmd --to pdf
```

Se houver erro de LaTeX, rode `quarto check` e instale dependências faltantes.
