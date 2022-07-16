from urllib import response
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

def trataHTML(input):
    #Decodificar
    input=input.decode('ISO-8859-1')
    #Transformar html em texto contínuo sem espaços
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

urlAcoes ='https://www.fundamentus.com.br/resultado.php'
urlFii = 'https://www.fundamentus.com.br/fii_resultado.php'
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'}

htmlAcoes = requisitaURL(urlAcoes, headers)
htmlFii = requisitaURL(urlFii, headers)

soup =  BeautifulSoup(htmlAcoes, 'html.parser')

for item in soup.find_all('tr'):
    for i in item.find_all('td'):
        print(i.getText())
        input()
    #print(item.find('p', class_='txt-value').getText())