from flask import Blueprint,render_template,request

from database.banco import MODELOS

word_route = Blueprint('word', __name__)

'''
Rota de Word
    -/word/ (GET) - Listar os modelos Words
    -/word/ (POST) - Inserir um modelo word no servidor
    -/word/<id> (GET) - Renderizar um formulário usar o modelo
    -/word/<id> (POST) - Receber os dados e usar o modelo
    -/word/<id>/edit (GET) - Renderizar um formulário para editar um modelo word
    -/word/<id>/delete (GET) - Deleta o registro do usuário 
'''

@word_route.route('/')
def listar_modelos_word():
    '''Listar os Modelos no banco de dados'''
    from sqlite3 import OperationalError

    from functions.func_db_modelo import listar
    try:
        modelos = listar()
    except OperationalError:
        return render_template('word/listar_modelos.html', mensagem_error='Você ainda nao criou um modelo')
    return render_template('word/listar_modelos.html', modelos_word=modelos)

@word_route.route('/novo_modelo', methods=['POST', 'GET'])
def form_modelo_word():
    '''Formulário para Gerar um Novo Modelo'''
    if request.method ==  'POST' and request.values.get('quant_var') != None:
        '''Verificando se o está na primeira parte do formulário'''
        try:
            quant_vars = int(request.values.get('quant_var'))
        except ValueError:
            return render_template('word/form_criar_modelo.html', mensagem_error='Isso não é um numero')
        from string import ascii_uppercase
        alfabeto_maiusculo = ascii_uppercase
        nome = request.values.get('nome_modelo')+'.doc'
        campos_vars = [(numero+1,alfabeto_maiusculo[numero]*3)for numero in range(quant_vars)]
        return render_template('word/form_criar_modelo.html', nome_modelo=nome, quant_var=campos_vars)
    elif request.method ==  'POST':
        '''Formulário que é pra criar o modelo realmente'''
        from sqlite3 import IntegrityError

        from functions.func_db_modelo import inserir

        nome = request.values.get('nome_modelo')
        variaveis = request.values.getlist('variavel')
        ref_variaveis = request.values.getlist('ref_variavel')
        default_variaveis = request.values.getlist('default_variavel')
        caminho_saida = request.values.get('caminho_saida')
        arquivo_saida = request.values.get('arquivo_saida')
        try:
            inserir(nome,variaveis,ref_variaveis,default_variaveis,caminho_saida,arquivo_saida)
        except IntegrityError:
            return render_template('word/form_criar_modelo.html', mensagem_error='Já existe um modelo com esse nome')
    return render_template('word/form_criar_modelo.html')

@word_route.route('/<int:modelo_id>')
def modelo_word(modelo_id):
    '''Formulário do modelo criado'''
    from functions.func_db_modelo import retirar_dados
    
    dados = retirar_dados(modelo_id)
    combinadas = [{'variavel': dados[2][i], 'ref_variavel': dados[3][i], 'defal_variavel': dados[4][i]} for i in range(len(dados[2]))]
    return render_template('word/form_modelo.html', dados_modelo=combinadas, id_modelo=dados[0], nome_modelo=dados[1], caminho_saida=dados[5], arquivo_saida=dados[6])


@word_route.route('/<int:modelo_id>', methods=['POST'])
def form_dados_word(modelo_id):
    '''Recebendo dados do formulário do modelo'''
    from functions.formatando_dados import FormatAll
    from functions.alterando_documento import gerando_documento

    dados_formatados = FormatAll(request.values.items())
    try:
        gerando_documento(dados_formatados.dados_dict.items())
    except FileNotFoundError:
        return render_template('word/form_modelo.html', mensagem_error='O modelo ou o caminho do arquivo de saída não existem(não foi possível concluir a operação)')

    return modelo_word(modelo_id)

@word_route.route('/<int:modelo_id>/edit')
def modelo_word_edit(modelo_id):
    '''Formulário para editar o modelo'''
    # import os

    # arquivo_antigo = "arquivo_original.txt"
    # novo_arquivo = "arquivo_novo.txt"

    # # Verifica se o arquivo existe
    # if os.path.exists(arquivo_antigo):
    #     os.rename(arquivo_antigo, novo_arquivo)
    #     print(f"O arquivo foi renomeado de {arquivo_antigo} para {novo_arquivo}.")
    # else:
    #     print(f"O arquivo {arquivo_antigo} não existe.")
    from functions.func_db_modelo import retirar_dados
    
    dados = retirar_dados(modelo_id)
    combinadas = [{'variavel': dados[2][i], 'ref_variavel': dados[3][i], 'defal_variavel': dados[4][i]} for i in range(len(dados[2]))]
    return render_template('word/form_criar_modelo.html', dados_modelo=combinadas, id_modelo=dados[0], nome_modelo=dados[1], caminho_saida=dados[5], arquivo_saida=dados[6])

@word_route.route('/<int:modelo_id>/delete')
def modelo_word_delete(modelo_id):
    '''Deletar o modelo'''
    return render_template('word/form_modelo.html', modelo_word=MODELOS)

