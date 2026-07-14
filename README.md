\# Projeto Final — Qualificação Automática de Leads de Pré-Vendas com LLM



Trabalho final da disciplina AI Applications (MBA — Faculdade Impacta).  

Professor: Vítor Wilher — Análise Macro.



\## Sobre o projeto



Pipeline CRISP-DM que automatiza a triagem de leads de pré-vendas B2B usando a API da Anthropic com saída estruturada via Pydantic.



\*\*Resultado:\*\* 15 leads processados, 73.3% classificados como quentes.



\## Como rodar do zero



\### 1. Pré-requisitos



\- Python ≥ 3.10

\- Quarto ≥ 1.4

\- Git



\### 2. Clone o repositório



```bash

git clone https://github.com/ykerlabs-n8n-proxy/Projeto-MBA.git

cd Projeto-MBA

```



\### 3. Crie o ambiente virtual



```bash

python -m venv .venv

.\\.venv\\Scripts\\Activate.ps1   # Windows

pip install -r requirements.txt

```



\### 4. Configure a chave de API



Copie o arquivo de exemplo e preencha com sua chave:



```bash

copy .env.example .env

```



Edite o `.env` e coloque sua chave:

ANTHROPIC\_API\_KEY=sua-chave-aqui



\### 5. Execute o pipeline



```bash

python src/preparacao.py

python src/qualificacao.py

```



\### 6. Gere o paper em PDF



```bash

quarto render paper\_final.qmd --to pdf

```



\## Estrutura do projeto

.

├── data/

│   ├── leads.csv                  # leads de entrada

│   ├── leads\_preparados.csv       # após limpeza

│   ├── leads\_qualificados.csv     # após classificação LLM

│   └── avaliacao.md               # métricas dos resultados

├── src/

│   ├── preparacao.py              # Fase 3: limpeza e formatação

│   └── qualificacao.py            # Fase 4: classificação com LLM

├── paper\_final.qmd                # source do paper

├── paper\_final.pdf                # entregável final

├── CLAUDE.md                      # briefing do projeto

└── requirements.txt



\## Tecnologias



\- Python 3.14

\- Anthropic API (claude-haiku-4-5)

\- Pydantic (saída estruturada)

\- Pandas

\- Quarto + LaTeX (PDF)

