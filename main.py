import tweepy
import requests
from bs4 import BeautifulSoup
import schedule
import time

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

# Função para postar no Twitter
def post_tweet():
    api = tweepy.Client(
        consumer_key='qhQNkFCsrDRmzpsOhnrswINh6',
        consumer_secret='VqsRn4RwZ9Wos8jJd04zfRM5qB31nQqsR0jfJJK8kdSaZJGbzl',
        access_token='1816964729962893312-679i9oG1jTKfiZf4CIkLaZ81RRzKFg',
        access_token_secret='Vp3ZIqkO0lJmlsDHtsBqAPZSkG2neSXbwjqrhKM8juqjW'
    )

    try:
        valor_dolar = get_dollar_rate()
        valor_bitcoin = get_bitcoin_rate()
        tweet_text = f"Mensagem enviada por GuerreiroBOT: Valor do dólar: {valor_dolar} e o Valor do Bitcoin: {valor_bitcoin}"
        response = api.create_tweet(text=tweet_text)
        print(response)
    except Exception as e:
        print(f"Algo deu erro: {e}")

schedule.every().day.at("14:40").do(post_tweet)
schedule.every().day.at("18:00").do(post_tweet)

while True:
    schedule.run_pending()
    time.sleep(1)
