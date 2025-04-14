import streamlit as st 


st.markdown("""
## Score de Reputação 
O **Índice de Reputação SentinelAI** foi desenvolvido para **traduzir a percepção da mídia sobre uma empresa em um indicador numérico compreensível e confiável**. Ele permite:
- Monitorar a reputação corporativa de forma contínua.
- Detectar riscos e oportunidades reputacionais.
- Comparar desempenho reputacional entre áreas ou períodos.

---

### 🧱 Fundamentos da Métrica

A métrica é baseada em três pilares:

1. **Sentimento da Notícia**  
   Notícias transmitem opiniões positivas, negativas ou neutras sobre a empresa.

2. **Relevância da Fonte**  
   Fontes mais confiáveis e amplamente lidas têm maior peso na construção da reputação pública.

3. **Intensidade do Impacto**  
   Algumas notícias causam impactos reputacionais maiores — positivas ou negativas — dependendo da sua gravidade ou importância.

---

## 🧮 Como a Métrica é Calculada

### 1. **Atribuição de Valores Base**

Para cada notícia avaliada, são atribuídos valores numéricos com base em três fatores:

#### 🧠 Sentimento da Notícia
| Sentimento   | Valor Numérico |
|--------------|----------------|
| Positivo     | +1             |
| Neutro       |  0             |
| Negativo     | -1             |

---

#### 📰 Peso da Fonte  
Reflete o **nível de influência da fonte na opinião pública**:

| Tipo da Fonte                               | Peso |
|---------------------------------------------|------|
| Grande mídia nacional (Ex: Estadão, Globo)  | 1.0  |
| Mídia especializada ou setorial             | 0.8  |
| Sites regionais ou blogs institucionais     | 0.5  |
| Fontes oficiais da empresa (site próprio)   | 0.3  |

---

#### 🚨 Intensidade do Impacto  
Mede o **quanto a notícia afeta a reputação da empresa**:

| Impacto                | Valor |
|------------------------|-------|
| Muito alto             | 1.0   |
| Alto                   | 0.8   |
| Moderado               | 0.5   |
| Baixo                  | 0.3   |

---

### 2. **Nota Ponderada da Notícia**

Cada notícia recebe uma **nota ponderada**, calculada assim:

```
Nota Ponderada = Sentimento × Peso da Fonte × Intensidade do Impacto
```

**Exemplo prático:**

- Notícia positiva (+1)
- Fonte = Mídia especializada (0.8)
- Impacto = Alto (0.8)

```python
Nota = +1 × 0.8 × 0.8 = +0.64
```

Se fosse uma notícia negativa:
```python
Nota = -1 × 0.8 × 0.8 = -0.64
```

---

### 3. **Score Bruto por Dimensão**

As notícias são agrupadas por **dimensão reputacional**. O score bruto da dimensão é a média ponderada:

```
Score Bruto = (Soma das Notas Ponderadas) / (Número de Notícias)
```

---

### 4. **Normalização do Score (0 a 5)**

Para facilitar a leitura e permitir comparações, o score é normalizado para uma **escala de 0 a 5**, onde:

- 0 = reputação extremamente negativa
- 2.5 = reputação neutra
- 5 = reputação extremamente positiva

A fórmula usada é:

```
Score Normalizado = ((Score Bruto + 1) / 2) × 5
```

| Score Bruto | Score Final |
|-------------|-------------|
| -1          | 0           |
| -0.5        | 1.25        |
| 0           | 2.5         |
| +0.5        | 3.75        |
| +1          | 5.0         |

---

### 5. **Tratamento para Dimensões Sem Notícias**

Se **nenhuma notícia for encontrada para uma dimensão**, usamos uma **abordagem neutra**, atribuindo:

```
Score = 2.5 (neutro)
```

> ⚠️ Isso evita penalizar empresas por ausência de exposição, especialmente em tópicos menos debatidos.

---

### 6. **Cálculo do Score Final da Empresa**

Após calcular o score de cada dimensão, o score final da empresa pode ser:

- **Média simples**: se todas as dimensões tiverem o mesmo peso.
- **Média ponderada**: se algumas dimensões forem consideradas mais críticas (ex: ESG ou Ética).

---

## 📊 Dimensões Reputacionais Monitoradas

O SentinelAI analisa 8 dimensões:

1. **ESG (Ambiental, Social e Governança)**
2. **Ética e Escândalos**
3. **Liderança e Governança Corporativa**
4. **Inovação e Expansão**
5. **Marca Empregadora (Employer Branding)**
6. **Performance Financeira e Operacional**
7. **Responsabilidade com Clientes e Usuários**
8. **Reputação Geral e Institucional**

Cada uma dessas áreas recebe um score individual, permitindo um diagnóstico reputacional completo e acionável.

---

## 📈 Interpretação dos Resultados

| Score Final | Interpretação                        |
|-------------|--------------------------------------|
| 0.0 – 1.5   | Reputação crítica (exposição grave)  |
| 1.6 – 2.5   | Reputação frágil (negativa)          |
| 2.6 – 3.4   | Reputação neutra/estável             |
| 3.5 – 4.4   | Reputação positiva                   |
| 4.5 – 5.0   | Reputação excelente / consolidada    |

---

## 🧠 Conclusão

Essa métrica oferece uma abordagem estruturada e escalável para traduzir conteúdo subjetivo (notícias) em dados confiáveis para tomada de decisão. Ao considerar **sentimento, impacto e fonte**, ela garante **profundidade analítica**, evitando distorções comuns em métricas reputacionais genéricas.

""")