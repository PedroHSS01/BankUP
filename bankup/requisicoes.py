import requests

class ValorDolar():

    def __init__(self):
        self.valor = -1

    def consulta(self):
        url = "https://economia.awesomeapi.com.br/json/daily/USD-BRL/1"
        retorno = requests.get(url)        
        if (retorno.status_code==200):
            jsonparsed = retorno.json()
            self.valor = jsonparsed[0]['high']

class ValorEuro():
    
    def __init__(self):
        self.valor = -1

    def consulta(self):
        url = "https://economia.awesomeapi.com.br/json/daily/EUR-BRL/1"
        retorno = requests.get(url)        
        if (retorno.status_code==200):
            jsonparsed = retorno.json()
            self.valor = jsonparsed[0]['high']

class ValorBTC():
    
    def __init__(self):
        self.valor = -1
        
    def consulta(self):
        url = "https://economia.awesomeapi.com.br/json/daily/BTC-BRL/1"
        retorno = requests.get(url)        
        if (retorno.status_code==200):
            jsonparsed = retorno.json()
            self.valor = jsonparsed[0]['high']
