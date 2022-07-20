from urllib import response
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd
from sqlalchemy import create_engine

my_conn=create_engine("mysql://sqluser:password@localhost/ATIVOS")

def trataHTML(input):
    input=input.decode('ISO-8859-1')
    return " ".join(input.split()).replace('> <', '><')

def requisitaURL(url, headers):
    try:
        req = Request(url, headers=headers)
        response=urlopen(req)
        html=response.read()
    #Erros de requisição
    except HTTPError as e:
        print(e.status,e.reason)
    except URLError as e:
        print(e.reason)
    return trataHTML(html)

def coletaDadosHTML(html):
    soup =  BeautifulSoup(html, 'html.parser')
    colunas=[item.getText() for item in soup.find_all('th')] # Esconder 'th'
    infoAtivos=pd.DataFrame(columns=colunas)
    
    k=0
    for item in soup.find_all('tr'):                            #Lendo e adicionando linha a linha
        if k!=0:
            infoAtivos.loc[-1] = [i.getText() for i in item.find_all('td')]  
            infoAtivos.index = infoAtivos.index + 1  
            infoAtivos = infoAtivos.sort_index()
        k+=1
    return infoAtivos

urlAcoes ='https://www.fundamentus.com.br/resultado.php'
urlFiis = 'https://www.fundamentus.com.br/fii_resultado.php'
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'}

htmlAcoes = requisitaURL(urlAcoes, headers)
htmlFiis = requisitaURL(urlFiis, headers)

acoes = coletaDadosHTML(htmlAcoes)
fiis = coletaDadosHTML(htmlFiis)

print(acoes)
print(fiis)

acoes.to_sql(name='ACOES',con=my_conn)
fiis.to_sql(name='FIIS',con=my_conn)