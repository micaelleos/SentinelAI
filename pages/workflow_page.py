import streamlit as st 

st.markdown("""

##  **Workflow de Agentes do SentinelAI**

## 🧠 Visão Geral

O SentinelAI é composto por um conjunto de **agentes especializados**, cada um com uma função bem definida na cadeia de análise reputacional. Eles operam como Agentes ReAct em um **fluxo de trabalho estruturado e colaborativo**, orientado por uma abordagem de **raciocínio passo a passo (chain-of-thought reasoning)**. Para evitar halicinações, a saída dos agente intermediários são sempre estruturadas.

O objetivo do sistema é coletar, interpretar e sintetizar informações públicas sobre uma empresa, entregando **um diagnóstico reputacional por domínio**, com base em análises qualitativas e quantitativas.

---

## 🧩 Arquitetura dos Agentes

### ⚙️ Componentes e Papéis

| Agente | Papel Principal | Descrição |
|--------|------------------|-----------|
| **Agente Planejador de Busca** | Estratégia | Define como buscar notícias para cada dimensão reputacional, estruturando prompts de pesquisa |
| **Agente de Busca** | Coleta | Executa pesquisas em fontes online confiáveis, com base na estratégia fornecida pelo planejador |
| **Agente de Avaliação de Relevância** | Curadoria | Avalia se as notícias encontradas são realmente relevantes para a dimensão analisada |
| **Agente Leitor e Analisador** | Interpretação | Faz leitura detalhada da notícia selecionada, preenchendo estrutura padronizada com análise reputacional |
| **Agente de Métricas** | Quantificação | Atribui notas e pontuações com base nos dados qualitativos gerados pelo leitor |
| **Agente Supervisor Conversacional** | Interface e Diagnóstico | Atua como consultor conversacional. Coordena os dados dos outros agentes e interage com o usuário final |

---

## 🔄 Workflow: Etapas do Processo

### 1. **Planejamento de Busca por Dimensão (Agente Planejador)**

- Recebe: Nome da empresa e dimensão reputacional (ex: ESG, Ética, etc.)
- Gera: Estratégia de busca, com palavras-chave, tipo de fonte e contexto temporal
- Output: Prompt estruturado para o agente de busca

> Exemplo: Para ESG → “Empresa + sustentabilidade + relatório + carbono + governança + ambiental”

- Este agente possui acesso a uma ferramenta de busca de site na web, chamada Tavily, para fazer buscas iniciais sobre as empresas. ​A Tavily é uma empresa especializada em fornecer APIs de busca otimizadas para Modelos de Linguagem de Grande Escala (LLMs) e agentes de inteligência artificial (IA). Seu principal produto, o Tavily Search API, oferece informações em tempo real, precisas e imparciais, permitindo que aplicações de IA acessem dados atualizados de forma eficiente. ​

---

### 2. **Execução da Busca (Agente de Busca)**

- Recebe: Prompt estruturado do agente planejador
- Realiza: Busca em tempo real em mecanismos de busca, com priorização de fontes confiáveis
- Coleta: Links, trechos de manchete, snippets e metadados (data, veículo)

> Exemplo: 5 a 10 resultados potenciais por dimensão
            
- Este agente também possui acesso à ferramenta de busca Tavily.

---

### 3. **Filtragem e Avaliação de Relevância (Agente de Relevância)**

- Recebe: Lista de notícias coletadas
- Analisa: Grau de aderência temática à dimensão
- Filtra: Apenas as notícias que realmente trazem conteúdo útil para o diagnóstico
- Output: Lista validada de notícias relevantes
- Este agente possui acesso a uma ferramenta de leitura de artigos na web chamada Jina AI. Essa ferramenta filtra e formata em markdown as informações relevantes nos sites.

---

### 4. **Leitura e Análise de Notícia (Agente Leitor)**

- Recebe: Uma notícia relevante (link ou texto completo)
- Executa:
  - Leitura compreensiva
  - Resumo
  - Extração de insights estratégicos
  - Avaliação de sentimento
  - Classificação da fonte
  - Determinação da intensidade de impacto
  - Justificativas e comentários

- Output: Estrutura `ListNewsAnalized`, preenchida com dados analíticos

---

### 5. **Cálculo de Métrica da Dimensão (Agente de Métricas)**

- Recebe: Lista de análises de notícias da dimensão
- Executa:
  - Normalização de dados qualitativos
  - Aplicação de pesos conforme: fonte, impacto, sentimento
  - Agregação ponderada
  - Atribuição de **nota entre 0 e 5** para a dimensão

> Exemplo de regra de impacto:

| Sentimento | Impacto | Peso |
|------------|---------|------|
| Negativo   | Alto    | -1.5 |
| Positivo   | Baixo   | +0.5 |

- Output: Score reputacional da dimensão (ex: ESG = 4.2)

---

### 6. **Síntese e Interação com o Usuário (Agente Supervisor)**

- Recebe: Notas e análises por dimensão
- Tarefas:
  - Elaborar diagnóstico global de reputação
  - Apontar vulnerabilidades e pontos fortes
  - Levantar tendências estratégicas
  - Responder perguntas do usuário
  - Guiar o usuário em decisões e interpretações

> Ele é o “consultor especialista em reputação” com quem o usuário conversa.

---

## 🛠️ Exemplo de Interação (Resumida)

```text
Usuário: Quero saber como está a reputação da Vale em ESG.

Supervisor → ativa Agente Planejador (dimensão ESG)
→ ativa Agente de Busca
→ ativa Agente de Relevância
→ ativa Agente Leitor
→ ativa Agente de Métrica
Supervisor → sintetiza o diagnóstico e retorna ao usuário:
“Nota 4.2 em ESG. A empresa foi elogiada por adotar padrões internacionais de sustentabilidade...”
```
---

## 🧩 Interdependência entre os Agentes

```mermaid
graph TD
  A[Usuário] --> S[Agente Supervisor]
  S --> P[Planejador de Busca]
  P --> B[Agente de Busca]
  B --> R[Agente de Relevância]
  R --> L[Agente Leitor]
  L --> M[Agente de Métricas]
  M --> S
```

Cada etapa é **ativada sob demanda**, e os dados trafegam entre os agentes em **formato estruturado e rastreável**, permitindo auditoria e explicabilidade.
""")

st.image('workflow.PNG')

st.markdown("""
---

## ✅ Vantagens da Arquitetura

- **Modularidade:** permite evoluir ou substituir partes do sistema sem impactar o todo
- **Escalabilidade:** cada agente pode ser paralelizado ou executado de forma assíncrona
- **Transparência:** todas as decisões (notas, análises) são justificadas
- **Interatividade:** o agente supervisor permite uma experiência consultiva, interpretando os dados com linguagem acessível

""")