from urllib import response
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd

def trataHTML(input):
    input=input.decode('ISO-8859-1')                        #Decodificar
    return " ".join(input.split()).replace('> <', '><')     #Transformar html em texto contínuo sem espaços

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

def coletaInfo(html):
    soup =  BeautifulSoup(html, 'html.parser')                  #Interpretador HTML
    colunas=[item.getText() for item in soup.find_all('th')]    #Coletando nome das colunas
    infoAtivos=pd.DataFrame(columns=colunas)                    #Criando dataFrame vazio
    
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


acoes = coletaInfo(htmlAcoes)
fiis = coletaInfo(htmlFiis)

print(acoes)
print(fiis)

