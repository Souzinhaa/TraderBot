# Usar python 3.9 e TA_Lib-0.4.24-cp39-cp39-win_amd64.whl
# from binance.client import Clientcommand:workbench.trust.manage
import datetime
import pandas_ta as pdta
from collections import defaultdict
import time
import utils
import integration


teste_complete = integration.get_price_coin_range('btc', int(datetime.datetime(2013, 1, 1).timestamp()), int(time.time())) # Ano, mês, dia
teste_complete = teste_complete[~teste_complete.index.duplicated(keep='first')]

teste = integration.get_price_coin_ohlc('btc')
teste = teste[~teste.index.duplicated(keep='first')]
# Calculando os níveis de suporte e resistência
def calculate_supports_lines(crypto, qtd):
    lines = defaultdict(int)
    close = crypto['close'].apply(int).tail(120)
    high = crypto['high'].apply(int).iloc[-1]
    low = crypto['low'].apply(int).iloc[-1]
    close_mean = close.mean()

    for price in close:
        price = round(price, -1) 
        lines[price] += 1
        
    lines_final = {'support': [], 'resistence': []}

    sorted_lines = dict(sorted(lines.items(), key=lambda item: item[1], reverse=True))
    
    for line, count in sorted_lines.items():
        if (line >= low and len(lines_final['resistence']) < qtd and line >= close_mean):
            lines_final['resistence'].append(line)
        elif (line <= high and len(lines_final['support']) < qtd and line <= close_mean):
            lines_final['support'].append(line)
            
    lines_final['support'] = sorted(lines_final['support'])
    lines_final['resistence'] = sorted(lines_final['resistence'], reverse=True)
    return lines_final

# Agora você pode usar x para fatiar o DataFrame até o índice atual
""" testado = slice_per_month(teste, 48, 365)
print(testado)
print(calculate_supports_lines(testado, 2)) """

#Performa melhor com range do fechamento de todos os dias
def create_rsi_indicator(det, days):
    # Crie uma cópia do DataFrame para evitar alterar o original
    df_rsi = det.copy()
    # Calcule o RSI
    df_rsi['rsi'] = pdta.rsi(df_rsi['close'], length=14).dropna()
    df_rsi = df_rsi.dropna()
    # Crie a coluna 'rsi_indicator' com base nas condições
    df_rsi['rsi_indicator'] = 'nada'
    df_rsi.loc[df_rsi['rsi'] < 40, 'rsi_indicator'] = 'compra'
    df_rsi.loc[df_rsi['rsi'] > 65, 'rsi_indicator'] = 'venda'

    # Remova linhas com valores nulos
    df_rsi = df_rsi.dropna()

    # Crie uma coluna que indique quando há uma mudança no valor de 'rsi_indicator'
    df_rsi['rsi_change'] = (df_rsi['rsi_indicator'] != df_rsi['rsi_indicator'].shift()).cumsum()

    # Encontre as séries onde 'rsi_indicator' é 'compra' ou 'venda' e a contagem é igual a 3
    df_rsi['count'] = df_rsi.groupby(['rsi_change', 'rsi_indicator']).cumcount() + 1
    result = df_rsi[((df_rsi['rsi_indicator'] == 'compra') | (df_rsi['rsi_indicator'] == 'venda')) & (df_rsi['count'] == days)]

    # Remova as colunas 'rsi', 'rsi_change', e 'count'
    series = result.drop(['rsi', 'rsi_change', 'count'], axis=1)
    
    return series

#print(create_rsi_indicator(teste_complete, 2))

def create_trend_indicator(df_crypto, limit):
    # Média Móvel Simples (sma)
    det = df_crypto.copy()
    det["sma"] = pdta.ma("sma", df_crypto["close"], length=7)
    
    det["ema100"] = pdta.ma("sma", det["close"], length=100)
    det["ema200"] = pdta.ma("sma", det["close"], length=200)
    det = utils.slice_per_month(det.dropna(), 36, -365)
    #det = det.dropna()[-730:].iloc[::-1]
    trend_final = {'bulls': [], 'bears': []}
    bulls = []
    bears = []
    for i in det.index:
        ema100 = det['ema100'][i]
        ema200 = det['ema200'][i]
        
        # Índices anteriores
        ema100_prev = det['ema100'].shift(1).loc[i]
        ema200_prev = det['ema200'].shift(1).loc[i]
        
        # Índices posteriores
        ema100_next = det['ema100'].shift(-1).loc[i]
        ema200_next = det['ema200'].shift(-1).loc[i]
        
        if ema100_prev > ema200_prev and ema100 <= ema200 and ema100_next < ema200_next:
            bulls.append(i)

        if ema100_prev < ema200_prev and ema100 > ema200 and ema100_next > ema200_next:
            bears.append(i)
    for i in range(0, limit):
        if len(bulls) > i and len(bears) > i:
            trend_final['bulls'].append(bulls[i])
            trend_final['bears'].append(bears[i])
    
    return trend_final
""" 
index = 4

df_invest = teste_complete.copy()
df_invest_trend = create_trend_indicator(df_invest, 3)

print(df_invest_trend)
# Crie o gráfico de linha para 'coluna1' e 'coluna2'.

plt1 = plt
plt1.figure(figsize=(25, 6))
plt1.plot(df_invest['close'], label='Close')
# Adicione linhas verticais em verde para 'bulls'
for bull_date in df_invest_trend['bulls']:
    plt1.axvline(x=bull_date, color='green', linestyle=':', label='Bull Date')

# Adicione linhas verticais em vermelho para 'bears'
for bear_date in df_invest_trend['bears']:
    plt1.axvline(x=bear_date, color='red', linestyle=':', label='Bear Date')
        
# Adicione um título ao gráfico.
plt1.title("Gráfico de Preços")

# Adicione uma legenda para as linhas.
plt1.legend()

# Exiba o gráfico.
plt1.show() """