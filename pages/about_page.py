import streamlit as st 


st.markdown("""
## **SentinelAI – Diagnóstico de Reputação Midiática Corporativa**

### 🧠 O que é o SentinelAI?

**SentinelAI** é um sistema de inteligência artificial conversacional especializado em **monitoramento e diagnóstico de reputação de empresas na mídia**. Ele simula um **consultor de reputação corporativa**, combinando múltiplos agentes inteligentes para identificar, analisar e interpretar notícias publicadas sobre uma organização.

O objetivo do SentinelAI é **traduzir o fluxo constante de informações públicas em insights estratégicos**, permitindo que empresas, analistas, investidores e stakeholders acompanhem **como a organização é percebida externamente**.

---

## 🧩 Estratégia de Análise Reputacional por Domínio

### 📊 Por que analisar por domínios?

A reputação corporativa é **multifacetada** — ela não depende apenas de um único fator. Uma empresa pode ser reconhecida por sua inovação, mas criticada por questões ambientais. Por isso, o SentinelAI divide a análise em **diferentes dimensões reputacionais**, ou seja, **áreas temáticas específicas que, juntas, formam o todo da reputação pública** da empresa.

---

### 🔍 Etapas da Análise por Domínio

#### 1. **Mapeamento Temático de Domínios**

A reputação é analisada com base em 8 domínios principais:

| Domínio | O que abrange? |
|--------|----------------|
| **ESG (Ambiental, Social e Governança)** | Sustentabilidade, meio ambiente, inclusão, transparência, relatórios ESG |
| **Ética e Escândalos** | Casos de corrupção, denúncias, fraudes, questões legais e reputacionais graves |
| **Liderança e Governança Corporativa** | Nomeações de executivos, decisões estratégicas, cultura de governança |
| **Inovação e Expansão** | Novos produtos, internacionalização, aquisições, transformação digital |
| **Marca Empregadora** | Condições de trabalho, imagem da empresa para talentos e funcionários |
| **Performance Financeira e Operacional** | Resultados financeiros, produtividade, eficiência operacional |
| **Responsabilidade com Clientes e Usuários** | Experiência do consumidor, recall, segurança de produtos, atendimento |
| **Reputação Institucional** | Imagem pública geral, prêmios, rankings, relacionamento com a sociedade |

---

#### 2. **Coleta Inteligente de Notícias**

Cada domínio tem **palavras-chave, temas e fontes preferenciais**. Um agente especializado em busca realiza consultas específicas para capturar notícias relevantes para cada dimensão.

> Exemplo: Para ESG, o sistema busca termos como “sustentabilidade”, “carbono”, “governança” etc., em fontes confiáveis.

---

#### 3. **Análise Qualitativa por Notícia**

Cada notícia passa por análise individual, onde são avaliados:

- **Sentimento (positivo, neutro, negativo)**
- **Relevância da fonte**
- **Intensidade do impacto**
- **Resumo e insights estratégicos**
- **Justificativa da análise**

Essas análises são feitas por um conjunto de agentes especializados em **interpretação de texto jornalístico com foco reputacional**.

---

#### 4. **Cálculo de Score por Domínio**

Após analisar as notícias, o sistema calcula um **score exclusivo por dimensão**, baseado em uma **métrica ponderada e normalizada (0 a 5)**.

> Assim, podemos identificar quais áreas da reputação estão fortes, estáveis ou críticas.

---

#### 5. **Geração do Diagnóstico Final**

O agente supervisor — que simula um consultor de reputação — compila os resultados de todos os domínios, gera insights agregados e entrega:

- **Pontos fortes e vulnerabilidades reputacionais**
- **Alertas de risco**
- **Tendências positivas a serem exploradas**
- **Comparações temporais ou entre concorrentes (quando aplicável)**

---

## 💼 Aplicações Práticas

- **Relações com investidores**
- **Gestão de crises**
- **Gestão de marca empregadora**
- **Compliance e governança**
- **Planejamento estratégico de comunicação**
- **Monitoramento de concorrentes**

---

## 🤖 Arquitetura do Sistema (resumida)

| Componente | Função |
|-----------|--------|
| 👨‍💻 **Agente Planejador** | Define como buscar as informações com base na dimensão |
| 🔍 **Agente de Busca** | Realiza pesquisas na internet com foco temático |
| 📚 **Agente de Relevância** | Filtra e valida notícias de interesse |
| 🧾 **Agente Leitor** | Faz leitura e interpretação detalhada da notícia |
| 📏 **Agente de Métrica** | Atribui a nota da notícia e calcula o score da dimensão |
| 🧠 **Agente Supervisor** | Conversa com o usuário, interpreta os dados e entrega o diagnóstico |

---

## 🧭 Conclusão

O SentinelAI não apenas monitora a reputação de empresas — ele **interpreta a mídia como um consultor humano faria**, mas com escalabilidade, agilidade e imparcialidade. A **análise por domínio** garante profundidade e foco, permitindo **ações corretivas e estratégicas baseadas em evidências reais**.
""")