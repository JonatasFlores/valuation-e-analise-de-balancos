import yfinance as yf
import pandas as pd

pd.options.display.float_format = '{:,.2f}'.format

# 1. Instanciar o ticker do Grupo Mateus
ticker = "GMAT3.SA"
gmat3 = yf.Ticker(ticker)

# 2. Extrair a DRE (Income Statement) anual
# O atributo .financials puxa os dados de resultados
dre = gmat3.financials

# 3. Transpor a matriz para que as datas fiquem nas linhas (formato padrão de análise de dados)
dre_df = dre.T

# 4. Calcular as Margens
# Os nomes das linhas no yfinance vêm em inglês: 'Total Revenue', 'Gross Profit', 'Net Income'
try:
    # Margem Bruta = (Lucro Bruto / Receita Total) * 100
    dre_df['Margem Bruta (%)'] = (dre_df['Gross Profit'] / dre_df['Total Revenue']) * 100
    
    # Margem Líquida = (Lucro Líquido / Receita Total) * 100
    dre_df['Margem Líquida (%)'] = (dre_df['Net Income'] / dre_df['Total Revenue']) * 100
    
    # 5. Filtrar e exibir apenas as colunas de interesse para o Valuation
    colunas_foco = ['Total Revenue', 'Gross Profit', 'Net Income', 'Margem Bruta (%)', 'Margem Líquida (%)']
    resultado = dre_df[colunas_foco]
    
    print("Análise de Margens - Grupo Mateus (GMAT3):\n")
    # Arredondando os valores decimais para facilitar a leitura no console
    print(resultado.round(2))
    
except KeyError as e:
    print(f"Erro ao encontrar a coluna: {e}")
    print("\nVerifique as colunas disponíveis na DRE extraída:")
    print(dre_df.columns.tolist())