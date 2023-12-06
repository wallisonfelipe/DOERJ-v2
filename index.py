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
import asyncio
import telegram

url_base = "https://www.ioerj.com.br"
current_date = datetime.datetime.now().strftime("%Y-%m-%d")
path = "/var/www/robos/files/"

file_path = os.path.join(path, "Poder_Executivo" + current_date + ".pdf")

def listFilesFromDir():
    files = []
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            files.append(file)
    return files

def sendedToday():
    if os.path.exists("lastSend.txt"):
        f = open("lastSend.txt", "r")
        lastSend = f.read()
        f.close()
        if lastSend == current_date:
            return True
        else:
            return False
        
    return False

async def sendFilesToTelegram():
    if sendedToday():
        return
    print("Enviando arquivos para o telegram")
    files = listFilesFromDir()
    f = open("lastSend.txt", "w")
    f.write(current_date)
    f.close()

    for file in files:
        new_file_name = file.split("-", 1)[1]
        bot = telegram.Bot(token='6985325316:AAG75Jh29MeHQBEwFfH2m3nq9d1N-RNLmAA')
        await bot.send_document(chat_id=-1002058293768, document=open(path + file, 'rb'), filename=new_file_name)


months = {
    1: "janeiro",
    2: "fevereiro",
    3: "março",
    4: "abril",
    5: "maio",
    6: "junho",
    7: "julho",
    8: "agosto",
    9: "setembro",
    10: "outubro",
    11: "novembro",
    12: "dezembro"
}

def isset(nameVar):
    return nameVar in globals()

def file_exists(file_path):
    if os.path.exists(file_path):
        return True
    return False    

if os.path.exists(file_path):
    print('Finalizando execucao.')
    exit()

def remove_files_in_directory(directory_path):
    try:
        # List all files in the directory
        files = os.listdir(directory_path)

        # Loop through the files and remove them
        for file in files:
            file_path = os.path.join(directory_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Removed: {file_path}")
            else:
                print(f"Skipping: {file_path} (not a file)")

        print("All files removed successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

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
    names = []
    links = site.select("#xo-content > font > div > ul > li")
    page_date = site.select_one("#xo-content > font > b").text
    pattern = r"\d+\s+de\s+\w+\s+de\s+\d+"
    match = re.search(pattern, page_date)
    page_date = match.group(0)
    print(match.group(0))
    inner_current_date = f"{datetime.datetime.now().day} de {months[datetime.datetime.now().month]} de {datetime.datetime.now().year}" 
    count = 0
    for anchor in links:
        extra_edition = anchor.select_one('span')
        if extra_edition:
            extra_edition = "-" + extra_edition.text
        else:
            extra_edition = ""
        temp_name = anchor.select_one("a").text + extra_edition
        print(temp_name)
        # if inner_current_date != match.group(0):
        #     print("O arquivo de hoje ainda não foi postado")
        real_links.append("https://www.ioerj.com.br/portal/modules/conteudoonline/" + anchor.select_one("a").get("href"))
        names.append(temp_name)
    
    return {
        "real_links": real_links,
        "names": names,
        "page_date": page_date
    }

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

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
    response = requests.get("https://www.ioerj.com.br/portal/modules/conteudoonline/mostra_edicao.php?k=" + documentId, headers=headers)
    with open(name, "wb") as file:
        file.write(response.content)

today = get_today_link()
links = get_file_links(today)

count = 0

remove_files_in_directory(path)

for link in links["real_links"]:
    if link:
        get_file_from_link(link, f"files/{links['page_date']}-{links['names'][count]}.pdf")
    count = count + 1


asyncio.run(sendFilesToTelegram())