# 🛡️ SentinelAI – Diagnóstico Reputacional de Empresas na Mídia

**SentinelAI** é um sistema inteligente composto por múltiplos agentes que coletam, analisam e sintetizam informações públicas sobre empresas, com foco em reputação e percepção pública na mídia. Ele entrega diagnósticos estruturados por dimensão reputacional (como ESG, Ética, Governança, etc.), utilizando uma abordagem modular, conversacional e explicável.

---

## 🚀 Funcionalidades Principais

- 🔍 Busca estratégica de notícias por dimensão de análise
- 🧠 Interpretação automatizada e estruturada das notícias
- 📊 Geração de métricas de reputação normalizadas (0–5)
- 💬 Interface conversacional com agente especialista em reputação
- 📈 Diagnóstico estratégico baseado em sentimentos, impacto e relevância
- 🏷️ Classificação por fonte (grande mídia, especializada, oficial etc.)

---

## 🧠 Arquitetura de Agentes

O sistema é composto por 6 agentes principais, cada um com função específica no workflow:

| Agente                        | Papel                                       |
|------------------------------|---------------------------------------------|
| **Planejador de Busca**      | Estratégia de coleta por dimensão           |
| **Executor de Busca e Relevância**| Busca em fontes confiáveis (via internet) e faz curadoria das notícias encontradas  |
| **Leitor/Analisador**        | Interpretação semântica das notícias        |
| **Gerador de Métrica**       | Cálculo de pontuação reputacional (0–5)     |
| **Supervisor Conversacional**| Interação com o usuário e síntese estratégica|

---

## 📊 Sobre a Métrica Reputacional

A pontuação por dimensão reputacional é calculada com base em:

- **Sentimento da notícia** (positivo, neutro, negativo)
- **Intensidade de impacto** (muito alto, alto, moderado, baixo)
- **Peso da fonte** (influência e credibilidade do veículo)
- **Relevância estratégica** da informação

Esses fatores são ponderados e transformados em um **score normalizado entre 0 e 5**. A ausência de notícias também é tratada na lógica de reputação, refletindo neutralidade ou visibilidade reduzida.

[📄 Ver documentação completa da métrica.](https://sentinelaiscore.streamlit.app/score_page)

---

## 🧭 Workflow do Sistema

![Workflow](workflow.PNG)

---

## 🧪 Exemplo de Uso

```bash
# Interação com agente conversacional
Usuário: "Quero saber como está a reputação da Vale em ESG."
SentinelAI: "A nota da dimensão ESG é 4.3. A empresa foi destaque em rankings de sustentabilidade..."
```

---

## ⚙️ Instalação e Execução

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/sentinelai.git
cd sentinelai

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute o app principal
python main.py
```

---

## 📬 Contato
Tem dúvidas, sugestões?

Entre em contato com a equipe responsável:

📧 Email: micaelle.osouza@gmail.com

🌐 Website: https://sentinelaiscore.streamlit.app/


Sinta-se à vontade para abrir Issues neste repositório para reportar bugs, propor melhorias ou solicitar funcionalidades.

