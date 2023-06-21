import os
import requests

def baixar_arquivos(url, endereco):
    #faz requisicao ao servidor
    resposta = requests.get(url)
    if resposta.status_code  == requests.codes.OK:
        with open(endereco, 'wb') as novo_arquivo:
            novo_arquivo.write(resposta.content)
        print("Download finalizado. Salvo em: {}".format(endereco))
    else:
        resposta.raise_for_status()

if __name__== "__main__":
    BASE_URL = 'http://www.ioerj.com.br/portal/modules/conteudoonline/mostra_edicao.php?k=BEE44B7B-E39DD-4D40-BC29-2067D630F00E{}'
    OUTPUT_DIR = 'output'

# inclusive range
start = 1
stop = 1
step = 1

# change stop
stop += step

for i in range(start, stop, step):
        nome_arquivo = os.path.join(OUTPUT_DIR, 'doerj_{}.pdf'.format(i))
        baixar_arquivos(BASE_URL.format(i), nome_arquivo)

        #Entrar no doerj e clicar na parte branca com botão direito e clica em exibir código fonte / depois pega o link cola aqui na url e tira a pagina
        #pega os arquivo e junta no ilove pdf