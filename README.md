# 📊 Motor de Valuation e Análise de Balanços (GMAT3)

📌 **Visão Geral do Projeto**
Este projeto consiste na construção de um motor automatizado de Valuation utilizando a metodologia de Fluxo de Caixa Descontado (DCF). O script extrai dados contábeis em tempo real da B3, padroniza as demonstrações financeiras e projeta o Valor da Firma (Enterprise Value), tendo como caso de estudo o **Grupo Mateus (GMAT3)**.

---

## 🎯 Objetivos do Projeto
- **Automação de Extração:** Substituir o download manual de planilhas Excel pela extração direta via API.
- **Engenharia de Dados Financeiros:** Tratar dados no formato US GAAP (DRE e Fluxo de Caixa) e alinhá-los em séries temporais consolidadas.
- **Modelagem Financeira:** Calcular automaticamente Margem Bruta, Margem Líquida, EBIT e NOPAT.
- **Valuation (DCF):** Estruturar o Fluxo de Caixa Livre para a Firma (FCFF) e descontar a valor presente usando premissas de WACC e perpetuidade.

---

## 🛠️ Tecnologias Utilizadas
- **Python:** Linguagem base para o script de extração e lógica matemática.
- **Pandas:** Limpeza, transposição de matrizes contábeis e formatação global de floats.
- **yfinance:** Consumo de dados históricos de mercado e balanços patrimoniais.
- **Git/GitHub:** Versionamento de código e documentação contínua.

---

## 🧠 Lógica e Premissas do Modelo
O algoritmo de Valuation segue os padrões de mercado para projeções corporativas:
1. **Ajuste de Impostos:** Tratamento de créditos tributários (SUDENE) para refletir o NOPAT real.
2. **Recomposição do Caixa:** Soma de Depreciação e Amortização ao lucro operacional.
3. **Investimentos:** Dedução automática do CAPEX (Capital Expenditure).
4. **Taxas Aplicadas:** 
   - Crescimento Projetado (Anos 1 a 5): 8% a.a.
   - Custo Médio Ponderado de Capital (WACC): 12% a.a.
   - Crescimento na Perpetuidade (g): 3% a.a.

---

## 📈 Principais Insights (Business Case)
Durante o desenvolvimento do modelo, três aspectos cruciais da operação do varejo foram validados nos dados:
- **Margens Estreitas:** A Margem Líquida flutua perto de 4%, exigindo um altíssimo giro de estoque para alavancar o Retorno sobre o Capital Investido (ROIC).
- **Peso da Dívida:** A despesa financeira consome cerca de um terço do EBIT da companhia para sustentar sua expansão acelerada.
- **Impacto do CAPEX:** O alto investimento em novas lojas e centros de distribuição reduz drasticamente o Fluxo de Caixa Livre no curto prazo, uma característica padrão de empresas de varejo em fase agressiva de crescimento.

---

## 🚀 Como Executar
1. Clone este repositório.
2. Ative o ambiente virtual: `.\.venv\Scripts\activate`
3. Instale as dependências: `pip install yfinance pandas`
4. Execute o motor: `python extracao_gmat3.py`