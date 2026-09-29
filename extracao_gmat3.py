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

fluxo_caixa_df = gmat3.cashflow.T

# 4. Calcular as Margens
# Os nomes das linhas no yfinance vêm em inglês: 'Total Revenue', 'Gross Profit', 'Net Income'
try:
    # Margem Bruta = (Lucro Bruto / Receita Total) * 100
    dre_df['Margem Bruta (%)'] = (dre_df['Gross Profit'] / dre_df['Total Revenue']) * 100
    
    # Margem Líquida = (Lucro Líquido / Receita Total) * 100
    dre_df['Margem Líquida (%)'] = (dre_df['Net Income'] / dre_df['Total Revenue']) * 100

    # Adicionando colunas de EBIT e Impostos, caso existam
    dre_df['EBIT / Lucro Operacional'] = dre_df.get('EBIT', dre_df.get('Operating Income', 0))
    dre_df['Impostos (IR/CSLL)'] = dre_df.get('Tax Provision', 0)

    # Adicionando coluna de Resultado Financeiro, caso exista
    dre_df['Resultado Financeiro'] = dre_df.get('Net Non Operating Interest Income Expense', dre_df.get('Interest Expense', 0))

    # Adicionando coluna de Depreciação e Amortização, caso exista
    dre_df['Depreciation and Amortization'] = dre_df.get('Depreciation', 0)

    #Adicionando o CAPEX (Capital Expenditures) caso exista
    dre_df['CAPEX'] = fluxo_caixa_df.get('Capital Expenditure', 0)
    
    # 5. Filtrar e exibir apenas as colunas de interesse para o Valuation
    colunas_foco = ['Total Revenue', 'Gross Profit', 'Net Income', 'Margem Bruta (%)', 'Margem Líquida (%)', 
                    'EBIT / Lucro Operacional', 'Impostos (IR/CSLL)', 'Resultado Financeiro', 'Depreciation and Amortization', 'CAPEX']
    resultado = dre_df[colunas_foco]
    
    # Filtrar apenas as colunas que realmente existem no DataFrame para evitar erros
    colunas_existentes = [col for col in colunas_foco if col in dre_df.columns]
    resultado = dre_df[colunas_existentes]
    
    print("DRE Expandida para Valuation - Grupo Mateus (GMAT3):\n")
    print(resultado)

except KeyError as e:
    print(f"Erro no processamento: {e}")