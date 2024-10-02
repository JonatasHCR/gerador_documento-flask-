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
        if modelos == []:
            raise OperationalError
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

@word_route.route('/<int:modelo_id>/edit', methods=['POST', 'GET'])
def modelo_word_edit(modelo_id):
    '''Formulário para editar o modelo'''
    if request.method == 'POST':
        from pathlib import Path
        
        from functions.func_db_modelo import retirar_dados

        CAMINHO_MODELO = Path(__file__).cwd() / 'gerador_documento' / 'database' / 'modelos'
        
        dados = retirar_dados(modelo_id)
        
        nome_novo = request.values.get('nome_modelo')
        variaveis = request.values.getlist('variavel')
        ref_variaveis = request.values.getlist('ref_variavel')
        default_variavel = request.values.getlist('default_variavel')
        caminho_saida = request.values.get('caminho_saida')
        arquivo_saida = request.values.get('arquivo_saida')
                
        from functions.func_db_modelo import modificar
        
        modificar(modelo_id,variaveis,ref_variaveis,default_variavel,nome_novo,caminho_saida,arquivo_saida)
        
        try:
            from os import rename

            nome_antigo = CAMINHO_MODELO / dados[1]
            nome_novo = CAMINHO_MODELO / nome_novo
            # Verifica se o arquivo existe
            rename(nome_antigo, nome_novo)
        except UnboundLocalError:
            return render_template('word/form_criar_modelo.html', mensagem_error='O modelo não existe(não foi possível concluir a operação de renomear)')
        return listar_modelos_word()
    from functions.func_db_modelo import retirar_dados
    
    dados = retirar_dados(modelo_id)
    combinadas = [{'variavel': dados[2][i], 'ref_variavel': dados[3][i], 'defal_variavel': dados[4][i]} for i in range(len(dados[2]))]
    return render_template('word/form_criar_modelo.html', dados_modelo=combinadas, id_modelo=dados[0], nome_modelo=dados[1], caminho_saida=dados[5], arquivo_saida=dados[6])

@word_route.route('/<int:modelo_id>/delete')
def modelo_word_delete(modelo_id):
    '''Deletar o modelo'''
    try:
        from os import remove
        from pathlib import Path
        
        CAMINHO_MODELO = Path(__file__).cwd() / 'gerador_documento' / 'database' / 'modelos'
        
        from functions.func_db_modelo import deletar,retirar_dados
        
        dados = retirar_dados(modelo_id)
        caminho_arquivo = CAMINHO_MODELO / dados[1]
        deletar(modelo_id)
        remove(caminho_arquivo)
    except FileNotFoundError:
        return render_template('word/listar_modelos.html', mensagem_error='O modelo não existe na pasta modelo(não foi possível concluir a operação de apagar)')
    except UnboundLocalError:
        return render_template('word/listar_modelos.html', mensagem_error='O modelo não existe no banco(não foi possível concluir a operação de apagar)')
    return listar_modelos_word()

