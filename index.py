import requests
import re
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import datetime
import os

url_base = "https://www.ioerj.com.br"
current_date = datetime.datetime.now().strftime("%Y-%m-%d")
path = "/var/www/robos/files/"
file_path = os.path.join(directory, "Poder_Executivo" + current_date + ".pdf")

if os.path.exists(file_path):
    print(f'The file {file_name} already exists in the directory {directory}. Finalizando execucao.')
    exit()

def get_today_link():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
    response = requests.get(url_base + "/portal/modules/conteudoonline/do_ultima_edicao.php", headers=headers)
    pattern = r"<a\s+href='([^']+)'"
    sub_link = re.search(pattern, response.text).group(1)

    parsed_url = urlparse(sub_link)
    query_parameters = parse_qs(parsed_url.query)
    data_param = query_parameters.get('data', None)

    return "https://www.ioerj.com.br/portal/modules/conteudoonline/do_seleciona_edicao.php?data=" + data_param[0]

def get_file_links(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
    response = requests.get(url, headers=headers)
    
    site = BeautifulSoup(response.text, "html.parser")
    real_links = []
    links = site.select("#xo-content > font > div > ul > li")
    for anchor in links:
        real_links.append("https://www.ioerj.com.br/portal/modules/conteudoonline/" + anchor.select_one("a").get("href"))
    
    return real_links

def get_file_from_link(link, name):
    chromeIntall = ChromeDriverManager().install()
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=ChromeService(chromeIntall), options=options)
    driver.get(link)
    driver.implicitly_wait(10)
    
    driver.execute_script('var hiddenInput = document.createElement("input");hiddenInput.setAttribute("type", "hidden");hiddenInput.setAttribute("value", pd);hiddenInput.setAttribute("id", "pd");document.body.appendChild(hiddenInput);')
    documentId = driver.find_element("id", "pd").get_attribute("value")
    driver.close()
    documentId = documentId[:12] + 'P' + documentId[12:]
    print(documentId)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
    response = requests.get("https://www.ioerj.com.br/portal/modules/conteudoonline/mostra_edicao.php?k=" + documentId, headers=headers)
    with open(name, "wb") as file:
        file.write(response.content)

today=get_today_link()
links = get_file_links(today)


mapper = {
    0: path + "Poder_Executivo" + current_date + ".pdf",
    1: path + "Tribunal_de_contas" + current_date + ".pdf",
    2: path + "Poder_Legislativo" + current_date + ".pdf",
    3: path + "Municipalidades" + current_date + ".pdf",
    4: path + "Publicacoes_a_pedido" + current_date + ".pdf",
}
count = 0

for link in links:
    get_file_from_link(link, mapper[count])
    count = count + 1

