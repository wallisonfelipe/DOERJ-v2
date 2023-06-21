import requests
from bs4 import BeautifulSoup

link = "http://www.ioerj.com.br/portal/modules/conteudoonline/mostra_edicao.php?k=0278989B-3E7D4-418F-94ED-7AEE5AB00AA51"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
requisicao = requests.get(link, headers=headers)
print(requisicao)
# print(requisicao.text)

site = BeautifulSoup(requisicao.text, "html.parser")

# print(site.prettify()) deixa os dados mais organizados
pesquisa = site.find("iframe", src="?k=0278989B-3E7F4-418F-94ED-7AEE5AB00AA51")
print(pesquisa["src"])