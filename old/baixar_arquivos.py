import os
import requests
from PyPDF2 import PdfMerger


def baixar_arquivos(url, endereco):
    #faz requisicao ao servidor
    resposta = requests.get(url)
    if resposta.status_code  == requests.codes.OK:
        with open(endereco, 'wb') as novo_arquivo:
            novo_arquivo.write(resposta.content)
        print("Download finalizado. Salvo em: {}".format(endereco))
    else:
        resposta.raise_for_status()


# Entrar no doerj e clicar na parte branca com botão direito e clica em exibir código fonte / depois pega o link cola aqui na url e tira a pagina
# pega os arquivo e junta no ilove pdf
if __name__== "__main__":
    BASE_URL = 'http://www.ioerj.com.br/portal/modules/conteudoonline/mostra_edicao.php?k=606F333F-69DF0-4D68-81C4-928C0E48659E{}'
    OUTPUT_DIR = 'output'

# inclusive range
start = 1
stop = 5
step = 1

# change stop
stop += step

for i in range(start, stop, step):
        nome_arquivo = os.path.join(OUTPUT_DIR, 'doerj_{}.pdf'.format(i))
        baixar_arquivos(BASE_URL.format(i), nome_arquivo)

merger = PdfMerger()

lista_arquivos = os.listdir("OUTPUT")
for arquivo in lista_arquivos:
     if ".pdf" in arquivo:
          if ".pdf" in arquivo:
               merger.append(f"OUTPUT/{arquivo}")

merger.write("DOERJ_Final.pdf")

       


