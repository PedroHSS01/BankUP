from requisicoes import ValorDolar, ValorEuro, ValorBTC
import json

def obter_cotacoes():
    dolar = ValorDolar()
    dolar.consulta()
    
    euro = ValorEuro()
    euro.consulta()
    
    btc = ValorBTC()
    btc.consulta()
    
    return {
        "dolar": dolar.valor,
        "euro": euro.valor,
        "bitcoin": btc.valor
    }

if __name__ == "__main__":
    cotacoes = obter_cotacoes()
    print(json.dumps(cotacoes)) 