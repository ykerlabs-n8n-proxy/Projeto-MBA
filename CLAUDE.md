# CLAUDE.md — Projeto Final: Qualificação automática de leads (SDR)

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
- Espaço para a fase seguinte: [definir o conjunto de leads, colunas do CSV e critérios de negócio que serão validados na fase de Data Understanding].

### 2. Data Understanding

- Fonte principal: arquivo CSV com leads contendo colunas como nome, email, telefone, empresa, cargo, mensagem, origem e data_criacao.
- Objetivo desta fase: compreender a qualidade, cobertura e relevância das colunas disponíveis para a classificação automatizada.
- Perguntas a responder:
  - Quais colunas estão presentes no CSV?
  - Quais campos tendem a ter informação útil para qualificação?
  - Quais campos são incompletos, ruidosos ou inconsistentes?
  - Como o texto da mensagem pode ser usado para inferir necessidade e urgência?
- Espaço para preenchimento: [descrever a análise exploratória, estatísticas básicas, exemplos de leads e problemas de qualidade encontrados].
- Espaço para a fase seguinte: [definir quais colunas serão normalizadas, limpas e enriquecidas antes do treinamento/uso do LLM].

### 3. Data Preparation

- Objetivo: preparar os dados para entrada no pipeline de classificação.
- Tarefas previstas:
  - carregar o CSV de leads;
  - validar colunas obrigatórias;
  - limpar e padronizar textos;
  - criar registros estruturados para envio ao LLM;
  - preservar a rastreabilidade entre entrada e saída.
- Estratégia de saída estruturada: usar Pydantic para garantir que cada lead receba os campos esperados.
- Espaço para preenchimento: [descrever as regras de limpeza, normalização, tratamento de valores ausentes e formato final dos dados].
- Espaço para a fase seguinte: [definir o prompt, os exemplos e a estratégia de execução do modelo para a fase de Modeling].

### 4. Modeling

- Objetivo: construir o pipeline de qualificação automática com LLM.
- Abordagem: ler cada lead a partir de um CSV, enviar o conteúdo relevante para o modelo Anthropic e retornar uma estrutura padronizada.
- Configuração do modelo:
  - provider: Anthropic;
  - model: claude-haiku-4-5;
  - temperature: 0.
- Saída esperada: score_qualificacao, categoria_interesse, urgencia, resumo_necessidade, proxima_acao_sugerida.
- Espaço para preenchimento: [descrever o prompt, a lógica de parsing via Pydantic, o fluxo de iteração por lead e o tratamento de erros].
- Espaço para a fase seguinte: [definir a estratégia de avaliação quantitativa e qualitativa dos resultados].

### 5. Evaluation

- Objetivo: avaliar se o pipeline produz classificações úteis, consistentes e acionáveis.
- Critérios de avaliação:
  - precisão da qualificação;
  - coerência entre score, categoria e urgência;
  - utilidade da próxima ação sugerida;
  - redução de tempo em comparação ao processo manual.
- Métrica principal: comparação do tempo de triagem manual antes e depois da automação, medida a partir de código reexecutável.
- Espaço para preenchimento: [descrever os testes, amostras de validação, critérios de revisão humana e métricas adicionais].
- Espaço para a fase seguinte: [definir como o resultado será apresentado em produção e em formato executivo].

### 6. Deployment

- Objetivo: entregar o projeto de forma reproducível e utilizável.
- Entregáveis finais: paper em PDF via Quarto e apresentação executiva com os principais resultados, limitações e recomendações.
- Forma de uso esperada: execução do pipeline sobre um novo CSV de leads, com saída estruturada e pronta para análise ou uso operacional.
- Espaço para preenchimento: [descrever o fluxo de execução, dependências, instruções de uso e plano de manutenção].

## Regras do projeto

- Apenas Anthropic como provedor de LLM.
- A chave da API deve ficar no arquivo .env e nunca no código nem em commits.
- Nenhum número deve ser inventado; todo valor citado deve ser gerado por execução de código.

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

## Como criar e ativar o .venv (Windows / macOS / Linux)

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

1. Abra o comando: Ctrl+Shift+P (ou Cmd+Shift+P no macOS).
2. Digite: Python: Select Interpreter.
3. Escolha o interpretador apontando para ./ .venv/bin/python (macOS/Linux)
   ou ./.venv\Scripts\python.exe (Windows).

Após isso, o VS Code usará o .venv para executar e depurar código, e para a instalação de pacotes pelo gerenciador integrado.

## Renderizar o paper final (Quarto → PDF)

Coloque os arquivos .qmd em paper/ e rode:

```bash
quarto render paper/paper.qmd --to pdf
```

Se houver erro de LaTeX, rode quarto check e instale dependências faltantes.
