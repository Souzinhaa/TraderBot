# Usar python 3.9 e TA_Lib-0.4.24-cp39-cp39-win_amd64.whl
# from binance.client import Clientcommand:workbench.trust.manage
import json
import datetime
import talib
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage


arquivo_json = "transactions.json"
path = 'C:/Users/Adrian/Dropbox/Projeto Trade TCC/TraderBot/transacoes/'
def convert_timestamp_to_datetime(timestamp):
    data = datetime.datetime.fromtimestamp(timestamp/1000)
    data = data.strftime("%Y-%m-%d 00:00:00")
    return pd.Timestamp(data)

#print(type(convert_timestamp_to_datetime(1578009600000)), convert_timestamp_to_datetime(1578009600000))

def slice_per_month(df, months, corte):
    last_index = df.index[-1]
    last_register = last_index - pd.DateOffset(months=months)
    if corte == 0:
        df = df.loc[last_register:]
    elif corte < 0:
        df = df.loc[last_register:][corte:]
    else:
        df = df.loc[last_register:][:corte]
    return df


def convert_ohlc(df_crypto):
    # Bollinger Bands 
    df_crypto['sma'] = talib.SMA(df_crypto['close'], 7) # Padrão 30 períodos
    upper, middle, lower = (nullos.dropna() for nullos in talib.BBANDS(df_crypto['close'], matype= talib.MA_Type.T3))
    
    det = pd.concat([upper,lower,df_crypto['close']],axis=1,join="inner")
    return det


def ler_carteira_json(number):
    try:
        with open(path + str(number) + arquivo_json, "r") as file:
            carteira = json.load(file)
        return carteira
    except FileNotFoundError:
        return {}
    
def gravar_carteira_json(carteira, number):        
    try:
        # Salve a carteira atualizada no arquivo JSON
        caminho = str(number) + arquivo_json
        with open(path + caminho, "w") as file:
            json.dump(carteira, file, indent=4)
        return carteira
    except FileNotFoundError:
        return {}
    
def gravar_resultados_json(resultados):        
    try:
        lista = []
        # Salve a carteira atualizada no arquivo JSON
        with open(path + 'results.json', "r") as file:
            lista = json.load(file)
        lista = lista + resultados
        with open(path + 'results.json', "w") as file:
            json.dump(lista, file, indent=4)
        return lista
    except FileNotFoundError:
        return {}
    
def corpo_email_compra(detalhes_operacao):
    corpo = f"""
    Assunto: Nova Operação de Compra de Criptomoeda

    Olá {detalhes_operacao["nome_destinatario"]},

    Espero que este e-mail o encontre bem. Gostaria de compartilhar uma emocionante novidade em nossa carteira de criptomoedas.
    Recentemente, realizamos uma operação de compra. Abaixo estão os detalhes da transação:

    **Compra em {detalhes_operacao["date"]}:**
       - Valor: ${detalhes_operacao["value_operation"]}
       - Quantidade: {detalhes_operacao["amount"]} BTC
       - Preço: ${detalhes_operacao["price"]} por BTC
       - Saldo na carteira em USD: ${detalhes_operacao["wallet_usd"]}
       - Seu preço médio é: ${detalhes_operacao["price_middle"]}
       - Resultado: {detalhes_operacao["earnings"]}

    Esta operação faz parte de nossa estratégia de investimento contínua. Se tiver alguma dúvida ou quiser mais informações, sinta-se à vontade para entrar em contato.

    Obrigado pela confiança em nosso trabalho!

    Atenciosamente,
    {detalhes_operacao["seu_nome"]}
    """
    return corpo


def corpo_email_venda(detalhes_operacao):
    corpo = f"""
    Assunto: Nova Operação de Venda de Criptomoeda

    Olá {detalhes_operacao["nome_destinatario"]},

    Espero que este e-mail o encontre bem. Gostaria de compartilhar uma nova operação emocionante em nossa carteira de criptomoedas.
    Recentemente, realizamos uma operação de venda. Abaixo estão os detalhes da transação:

    **Venda em {detalhes_operacao["date"]}:**
       - Valor: ${detalhes_operacao["value_operation"]}
       - Quantidade: {detalhes_operacao["amount"]} BTC
       - Preço: ${detalhes_operacao["price"]} por BTC
       - Saldo na carteira em USD: ${detalhes_operacao["wallet_usd"]}
       - Seu preço médio é: ${detalhes_operacao["price_middle"]}
       - Resultado: {detalhes_operacao["earnings"]}

    Esta operação faz parte de nossa estratégia de otimização de ganhos. Se tiver alguma dúvida ou quiser mais informações, sinta-se à vontade para entrar em contato.

    Obrigado pela confiança em nosso trabalho!

    Atenciosamente,
    {detalhes_operacao["seu_nome"]}
    """
    return corpo

def enviar_email_com_anexo(caminho_imagem, email_de, email_para, senha, servidor_smtp='smtp.gmail.com', porta_smtp=587, corpo_email=None, subject = None):
    # Configurar o e-mail
    msg = MIMEMultipart()
    msg['From'] = email_de
    msg['To'] = email_para
    msg['Subject'] = subject

    # Adicionar corpo do e-mail (opcional)
    if corpo_email:
        corpo = MIMEText(corpo_email)
        msg.attach(corpo)

    # Anexar a imagem do gráfico ao e-mail
    for caminho in caminho_imagem:
        with open(path + caminho, 'rb') as imagem:
            anexo = MIMEImage(imagem.read())
            anexo.add_header('Content-Disposition', 'attachment', filename=caminho)
            msg.attach(anexo)

    # Configurações do servidor SMTP
    servidor_smtp = servidor_smtp
    porta_smtp = porta_smtp

    # Iniciar uma conexão com o servidor SMTP
    conexao_smtp = smtplib.SMTP(servidor_smtp, porta_smtp)

    # Habilitar a comunicação segura
    conexao_smtp.starttls()

    # Login no e-mail
    conexao_smtp.login(email_de, senha)

    # Enviar o e-mail
    conexao_smtp.sendmail(email_de, email_para, msg.as_string())

    # Fechar a conexão SMTP
    conexao_smtp.quit()