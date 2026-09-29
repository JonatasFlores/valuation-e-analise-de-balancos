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

    # Adicionando a Depreciação e Amortização, caso exista
    dre_df['Depreciation and Amortization'] = fluxo_caixa_df.get('Depreciation And Amortization', fluxo_caixa_df.get('Depreciation', 0))

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
    # 1. Ajuste de Sinais: Garantir que Impostos reduzam o lucro (se vieram positivos na base, viram negativos)
    impostos_ajustados = resultado['Impostos (IR/CSLL)'].apply(lambda x: x if x < 0 else -x)
    nopat = resultado['EBIT / Lucro Operacional'] + impostos_ajustados # Lucro Operacional após impostos
            
    # 2. Calcular o FCFF (Fluxo de Caixa Livre)
    # Fórmula: NOPAT + Depreciação + CAPEX (O CAPEX do Yahoo já costuma vir negativo, então somamos)
    resultado['FCFF'] = nopat + resultado['Depreciation and Amortization'] + resultado['CAPEX']
        
    print("\nHistórico de Geração de Caixa Livre (FCFF):")
    print(resultado[['EBIT / Lucro Operacional', 'FCFF']])
    
    # 3. Motor de Valuation Automatizado
    # Premissas do Analista para o Grupo Mateus:
    wacc = 0.12 # Custo de Capital da empresa (Ex: 12% ao ano)
    g = 0.03    # Crescimento na Perpetuidade (Ex: 3% ao ano, acompanhando a inflação/PIB)
    crescimento_projetado = 0.08 # Projeção de crescimento agressivo de 8% nos próximos 5 anos
        
    # Pegar o FCFF do ano mais recente (linha 0 da tabela)
    ultimo_fcff = resultado['FCFF'].iloc[0] 
        
    print("\n--- PROJEÇÃO DE VALUATION (PRÓXIMOS 5 ANOS) ---")
    dcf_valor_presente = 0
        
    for ano in range(1, 6):
        fcff_projetado = ultimo_fcff * ((1 + crescimento_projetado) ** ano)
        # Descontando o valor para dinheiro de "hoje" usando o WACC
        valor_presente_ano = fcff_projetado / ((1 + wacc) ** ano)
        dcf_valor_presente += valor_presente_ano
        print(f"Ano {ano}: FCFF Projetado = R$ {fcff_projetado:,.2f} | Valor Presente = R$ {valor_presente_ano:,.2f}")
            
        # 4. Valor Terminal (O valor da empresa do ano 5 até o infinito)
        valor_terminal = (ultimo_fcff * ((1 + crescimento_projetado)**5) * (1 + g)) / (wacc - g)
        vt_descontado = valor_terminal / ((1 + wacc) ** 5)
        
    # 5. Enterprise Value (Valor da Firma)
    valor_firma = dcf_valor_presente + vt_descontado
    print(f"\nValor da Firma (Enterprise Value) Projetado: R$ {valor_firma:,.2f}")   
       

except KeyError as e:
    print(f"Erro no processamento: {e}")

  