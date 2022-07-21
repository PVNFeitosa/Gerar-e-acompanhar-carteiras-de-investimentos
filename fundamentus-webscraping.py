from urllib import response
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd
from sqlalchemy import create_engine
import os

def trataHTML(input):

    input=input.decode('ISO-8859-1')

    return " ".join(input.split()).replace('> <', '><')

def requisitaURL(url, headers):

    try:
        requisicao = Request(url, headers=headers)
        response=urlopen(requisicao)
        html=response.read()
    #Erros de requisição
    except HTTPError as e:
        print(e.status,e.reason)
    except URLError as e:
        print(e.reason)

    return trataHTML(html)

def coletaDadosHTML(html):

    soup =  BeautifulSoup(html, 'html.parser')
    htmlTabela=str(soup.find_all('table')[0])  
    with open("tmp.html", "w",encoding="ISO-8859-1") as arquivoTemporario:
        arquivoTemporario.write(htmlTabela)
    infoAtivos = pd.read_html("tmp.html")
    os.remove("tmp.html")

    return infoAtivos[0]
    
if __name__== "__main__":
    urlAcoes ='https://www.fundamentus.com.br/resultado.php'
    urlFiis = 'https://www.fundamentus.com.br/fii_resultado.php'
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'}

    htmlAcoes = requisitaURL(urlAcoes, headers)
    htmlFiis = requisitaURL(urlFiis, headers)

    acoes = coletaDadosHTML(htmlAcoes)
    fiis = coletaDadosHTML(htmlFiis)

    print(acoes)
    print(fiis)

    conexao=create_engine("mysql://sqluser:password@localhost/ATIVOS")

    acoes.to_sql(name='acoes',con=conexao,if_exists='replace')
    fiis.to_sql(name='fiis',con=conexao,if_exists='replace')