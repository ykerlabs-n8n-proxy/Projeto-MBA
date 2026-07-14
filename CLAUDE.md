CLAUDE.md — Projeto Final: Qualificação automática de leads (SDR)

Briefing do projeto — entregue como PDF via Quarto e apresentação executiva. Leia antes de editar.

## Fluxo CRISP-DM do projeto

### 1. Business Understanding

- Tema: Qualificação automática de leads de pré-vendas (SDR).
- Problema de negócio: times de pré-vendas recebem leads de formulários, eventos e inbound marketing. O SDR gasta tempo lendo cada lead manualmente para decidir: é quente ou frio? Qual produto faz sentido? Qual a urgência?
- Objetivo do projeto: automatizar a triagem de leads para reduzir o tempo de análise manual e melhorar a priorização para a equipe comercial.
- Solução proposta: pipeline que lê um CSV de leads e usa a API da Anthropic para classificar cada lead em campos estruturados via Pydantic.
- Modelo/LLM: apenas Anthropic, com o modelo claude-haiku-4-5 e temperature=0.
- Campos esperados de saída: score_qualificacao, categoria_interesse, urgencia, resumo_necessidade, proxima_acao_sugerida.
- Métrica de sucesso: redução do tempo de triagem manual. Antes: [medir em minutos por lead via código]; depois: [medir automaticamente após a execução do pipeline]. O ganho será comparado com base reexecutável.
- Entregáveis: paper em PDF via Quarto e apresentação executiva.
- Regra de ouro: nunca inventar números. Todo valor citado deve vir de uma execução de código reexecutável.
- Premissas e restrições: a chave da API já está configurada no arquivo .env via ANTHROPIC_API_KEY; o projeto deve usar apenas a API da Anthropic.
- Resultado da fase seguinte: conjunto de 15 leads B2B fictícios em data/leads.csv com 9 colunas, incluindo mensagem_necessidade como campo principal para qualificação.

### 2. Data Understanding

- Fonte principal: arquivo CSV local chamado data/leads.csv, contendo leads fictícios e realistas de pré-vendas B2B.
- Volume da amostra: 15 leads.
- Colunas disponíveis: id, empresa, segmento, porte, nome_contato, cargo, origem, mensagem_necessidade e data_entrada.
- Objetivo desta fase: compreender a qualidade, cobertura e relevância das colunas disponíveis para a classificação automatizada.
- Perguntas a responder:
  - Quais colunas estão presentes no CSV?
  - Quais campos tendem a ter informação útil para qualificação?
  - Quais campos são incompletos, ruidosos ou inconsistentes?
  - Como o texto da mensagem pode ser usado para inferir necessidade e urgência?
- Estimativa de tokens por lead: os caracteres da coluna mensagem_necessidade foram contados e a estimativa foi feita como caracteres / 4. Para a base atual, a estimativa ficou em torno de 70 a 90 tokens por lead, com média aproximada de 80 tokens por lead.
- Resultado: 15 leads carregados, nenhum com mensagem_necessidade vazia. Segmentos presentes: tecnologia, logística, saúde, indústria, varejo. Origens: formulario_site (4), indicacao (4), inbound (4), evento (3).
- Resultado da fase seguinte: colunas segmento, porte, origem e cargo normalizadas para lowercase. Coluna texto_para_llm criada concatenando os campos relevantes de cada lead.

### 3. Data Preparation

- Objetivo: preparar os dados para entrada no pipeline de classificação.
- Tarefas previstas:
  - carregar o CSV de leads;
  - validar colunas obrigatórias;
  - limpar e padronizar textos;
  - criar registros estruturados para envio ao LLM;
  - preservar a rastreabilidade entre entrada e saída.
- Estratégia de saída estruturada: usar Pydantic para garantir que cada lead receba os campos esperados.
- Resultado: script src/preparacao.py executado com sucesso. 15 leads limpos, textos normalizados para lowercase, coluna texto_para_llm criada. Saída: data/leads_preparados.csv.
- Resultado da fase seguinte: prompt com persona de especialista em pré-vendas B2B, temperature=0, schema Pydantic com 6 campos fixos garantindo comparabilidade entre todos os leads.

### 4. Modeling

- Objetivo: construir o pipeline de qualificação automática com LLM.
- Abordagem: ler cada lead a partir de um CSV, enviar o conteúdo relevante para o modelo Anthropic e retornar uma estrutura padronizada.
- Configuração do modelo:
  - provider: Anthropic;
  - model: claude-haiku-4-5;
  - temperature: 0.
- Saída esperada: score_qualificacao, categoria_interesse, urgencia, resumo_necessidade, proxima_acao_sugerida.
- Resultado: script src/qualificacao.py executado com sucesso. 15 leads classificados via API Anthropic (claude-haiku-4-5, temperature=0). Schema Pydantic com 6 campos. Saída: data/leads_qualificados.csv.
- Resultado da fase seguinte: avaliação por distribuição de scores, cruzamento segmento x score e análise de consistência entre urgência e próxima ação sugerida.

### 5. Evaluation

- Objetivo: avaliar se o pipeline produz classificações úteis, consistentes e acionáveis.
- Critérios de avaliação:
  - precisão da qualificação;
  - coerência entre score, categoria e urgência;
  - utilidade da próxima ação sugerida;
  - redução de tempo em comparação ao processo manual.
- Métrica principal: comparação do tempo de triagem manual antes e depois da automação, medida a partir de código reexecutável.
- Resultado real (data/avaliacao.md): 11 leads quentes (73.3%), 4 mornos (26.7%), 0 frios. Urgência alta: 10 leads. Indústria e saúde: 100% quentes. Varejo: maior proporção de mornos.
- Resultado da fase seguinte: paper_final.pdf gerado via Quarto + LaTeX com os resultados reais do pipeline. Apresentação executiva com problema, solução, resultados e próximos passos.

### 6. Deployment

- Objetivo: entregar o projeto de forma reproducível e utilizável.
- Entregáveis finais: paper em PDF via Quarto e apresentação executiva com os principais resultados, limitações e recomendações.
- Forma de uso esperada: execução do pipeline sobre um novo CSV de leads, com saída estruturada e pronta para análise ou uso operacional.
- Resultado: paper_final.pdf gerado via quarto render paper_final.qmd --to pdf. Pipeline completo: src/preparacao.py → src/qualificacao.py → data/leads_qualificados.csv → paper_final.pdf.

## Regras do projeto

- Apenas Anthropic como provedor de LLM.
- A chave da API deve ficar no arquivo .env e nunca no código nem em commits.
- Nenhum número deve ser inventado; todo valor citado deve ser gerado por execução de código.

## Estrutura mínima do projeto (esperada)
.
├── CLAUDE.md
├── README.md
├── .gitignore
├── .env.example
├── requirements.txt
├── data/
├── src/
└── paper/

## Como criar e ativar o .venv (Windows / macOS / Linux)

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
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

1. Abra o comando: Ctrl+Shift+P (ou Cmd+Shift+P no macOS).
2. Digite: Python: Select Interpreter.
3. Escolha o interpretador apontando para ./.venv/bin/python (macOS/Linux) ou ./.venv\Scripts\python.exe (Windows).

## Renderizar o paper final (Quarto → PDF)

```bash
quarto render paper_final.qmd --to pdf
```

Se houver erro de LaTeX, rode quarto check e instale dependências faltantes.