from flask import Flask, render_template, request, redirect, url_for, flash
import PyPDF2
import os

app = Flask(__name__)
app.secret_key = 'chavedeseguranca'# os formulario so renderizam se esta chave estiver configurada 
app.config['UPLOAD_FOLDER'] = 'uploads'# configuraçao do caminho para o uploads de arquivos


# aqui vai criar a pasta para armazenar os uploads se a pasta nao existir
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


# aqui vai ler o conteudo do PDF
def ler_pdf(caminho_pdf):
    with open(caminho_pdf, 'rb') as arquivo: # bati muito a cabeca, mas o arquivo so vai ser lido se for de forma BINARIA, NAO ESQUEÇA!!!!!!!
        leitor_pdf = PyPDF2.PdfReader(arquivo)# variavel recebe funcao de leitura da prorpia bilbioteca PyPDF
        conteudo = "" # o ce[onteudo inicia vazio
        for pagina in leitor_pdf.pages:# percorre as paginas e coloca na variavel conteudo que estava vazio, e estrai o texto
            conteudo += pagina.extract_text()
        return conteudo

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# essa rota so vai aparecer após enviar o arquivo porque ela so pode atender a requisiçao do method POST!!!!
@app.route('/upload', methods=['POST'])
def upload_pdf():
 
    # antes que se pergunte que diabos é isso
    # vá no html 'index.html' e veja de onde essa variavel está puxando esse request
    # como voce vai saber se o arquivo .PDF foi enviado se voce nao fez uma requisicao pra saber se realmente ele foi enviado!!!!
    # a variavel arquivo esta basicamente recebendo o conteudo do formulario que foi preenchido
    arquivo = request.files['pdfFile'] 

    # se o arquivo existir E for do tipo .PDF
    # salve o caminho dele e ele

    # duas vefiricaçoes, a primeira se arquivo estiver preenchido, e se a extencao do arquivo for .PDF
    # isso garante que voce realmente preencha o formulario, e que seja preenchido de forma correta.
    if arquivo and arquivo.filename.endswith('.pdf'):
        # salva o arquivo que for True pelo if no caminho:
        # app.config['UPLOAD_FOLDER'] que foi setado la encima na linha 7
        caminho_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], arquivo.filename)
        arquivo.save(caminho_arquivo)# salva o arquivo 

        # Funçao que ler o conteúdo do PDF | linha 17
        conteudo_pdf = ler_pdf(caminho_arquivo) # essa funcao é da porpria biblioteca

        # aqui so vai renderizar o conteudo do pdf que foi passado para a variavel conteudo_pdf 
        return render_template('resultado.html', conteudo=conteudo_pdf)


if __name__ == '__main__':
    app.run(debug=True)
