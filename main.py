import tweepy
import requests
from bs4 import BeautifulSoup
import schedule
import time

# Armazenar os valores as 08:00 e 08:05
dollar_rate_morning = None
bitcoin_rate_morning = None

# Função para buscar a cotação do dólar
def get_dollar_rate():
    response = requests.get("https://dolarhoje.com/")
    soup = BeautifulSoup(response.content, "html.parser")
    cotacao_div = soup.find("div", {"id": "cotacao"})
    if cotacao_div:
        valor_dolar_input = cotacao_div.find("input", {"id": "nacional"})
        if valor_dolar_input:
            return valor_dolar_input.get("value")
    return "Valor do dólar não encontrado"

# Função para buscar a cotação do Bitcoin
def get_bitcoin_rate():
    response = requests.get("https://dolarhoje.com/bitcoin-hoje/")
    soup = BeautifulSoup(response.content, "html.parser")
    cotacao_div2 = soup.find("div", {"id": "cotacao"})
    if cotacao_div2:
        valor_bitcoin_input = cotacao_div2.find("input", {"id": "nacional"})
        if valor_bitcoin_input:
            return valor_bitcoin_input.get("value")
    return "Valor do Bitcoin não encontrado"

# Chaves Twiter
def post_tweet(message):
    api = tweepy.Client(
        consumer_key='qhQNkFCsrDRmzpsOhnrswINh6',
        consumer_secret='VqsRn4RwZ9Wos8jJd04zfRM5qB31nQqsR0jfJJK8kdSaZJGbzl',
        access_token='1816964729962893312-679i9oG1jTKfiZf4CIkLaZ81RRzKFg',
        access_token_secret='Vp3ZIqkO0lJmlsDHtsBqAPZSkG2neSXbwjqrhKM8juqjW'
    )

    try:
        response = api.create_tweet(text=message)
        print(response)
    except Exception as e:
        print(f"Algo deu erro: {e}")

# Postagem das 08:00
def morning_post_dollar():
    global dollar_rate_morning
    dollar_rate_morning = get_dollar_rate()
    tweet_text = f"Ibovespa abre em alta!; dólar está em: {dollar_rate_morning}"
    post_tweet(tweet_text)

# Postagem das 18:00
def evening_post_dollar():
    global dollar_rate_morning
    dollar_rate_evening = get_dollar_rate()
    
    # Calculando a porcentagem de mudança
    if dollar_rate_morning is not None and dollar_rate_evening is not None:
        dollar_rate_morning_float = float(dollar_rate_morning.replace(",", "."))
        dollar_rate_evening_float = float(dollar_rate_evening.replace(",", "."))
        percentual_mudanca = ((dollar_rate_evening_float - dollar_rate_morning_float) / dollar_rate_morning_float) * 100
        
        if percentual_mudanca > 0:
            tweet_text = f"Ibovespa fecha em dólar em ALTA! +{percentual_mudanca:.2f}%; dólar em sobe a R$ {dollar_rate_evening}"
        elif percentual_mudanca == 0:
            tweet_text = f"Ibovespa fecha em {percentual_mudanca:.2f}%; dólar mantem-se em R$ {dollar_rate_evening}"
        else:
            tweet_text = f"Ibovespa fecha em dólar em BAIXA! -{percentual_mudanca:.2f}%; dólar cai a R$ {dollar_rate_evening}"
    else:
        tweet_text = f"Mensagem enviada por GuerreiroBOT: Valor do dólar às 18:00: {dollar_rate_evening}.."
    
    post_tweet(tweet_text)

    #BITCOIN

    # # Função para a postagem das 08:05
    # def morning_post_bitcoin():
    #     global bitcoin_rate_morning
    #     bitcoin_rate_morning = get_bitcoin_rate()
    #     tweet_text = f"Mensagem enviada por GuerreiroBOT: Valor do Bitcoin às 08:05: {bitcoin_rate_morning}"
    #     post_tweet(tweet_text)

    # # Função para a postagem das 18:05
    # def evening_post_bitcoin():
    #     global bitcoin_rate_morning
    #     bitcoin_rate_evening = get_bitcoin_rate()
        
    #     # Calculando a porcentagem de mudança
    #     if bitcoin_rate_morning is not None and bitcoin_rate_evening is not None:
    #         bitcoin_rate_morning_float = float(bitcoin_rate_morning.replace(",", "."))
    #         bitcoin_rate_evening_float = float(bitcoin_rate_evening.replace(",", "."))
    #         percentual_mudanca = ((bitcoin_rate_evening_float - bitcoin_rate_morning_float) / bitcoin_rate_morning_float) * 100
    #         tweet_text = f"Mensagem enviada por GuerreiroBOT: Valor do Bitcoin às 18:05: {bitcoin_rate_evening}. Mudança: {percentual_mudanca:.2f}%"
    #     else:
    #         tweet_text = f"Mensagem enviada por GuerreiroBOT: Valor do Bitcoin às 18:05: {bitcoin_rate_evening}."
    
    # post_tweet(tweet_text)

#dolar inicio
schedule.every().day.at("09:30").do(morning_post_dollar)
#dolar fim
schedule.every().day.at("17:25").do(evening_post_dollar)

# #bitcoin inicio
# schedule.every().day.at("20:15").do(morning_post_bitcoin)
# #bitcoin inicio
# schedule.every().day.at("20:25").do(evening_post_bitcoin)


while True:
    schedule.run_pending()
    time.sleep(1)
