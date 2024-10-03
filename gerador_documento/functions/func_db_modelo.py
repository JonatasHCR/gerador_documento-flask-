import sqlite3
from pathlib import Path
import json

from functions.alterando_documento import gerando_modelo

ROOT_DIR = Path(__file__).cwd() / 'gerador_documento' / 'database'
DB_NAME = 'modelos.sqlite3'
DB_FILE = ROOT_DIR / DB_NAME

def criar_banco():
    '''Criar o banco de dados para armazenar as informações do modelo'''
    try:
        update()
    except (UnboundLocalError,sqlite3.OperationalError):
        try:
            connection = sqlite3.connect(DB_FILE)
            cursor = connection.cursor()

            # SQL
            cursor.execute(
                f'CREATE TABLE IF NOT EXISTS modelos'
                '('
                'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                'name TEXT UNIQUE NOT NULL,'
                'variaveis TEXT,'
                'ref_variaveis TEXT,'
                'default_variaveis TEXT,'
                'caminho_saida TEXT,'
                'arquivo_saida TEXT'
                ')'
            )
            connection.commit()
        finally:
            """Garantir que a função sempre feche a conexão"""
            cursor.close()
            connection.close()

def inserir(nome,dados,ref_dados,default_var,caminho_saida,arquivo_saida):
    '''função para inserir os dados no banco'''
    try:
        criar_banco()
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        lista_convert_dados = json.dumps(dados)
        lista_convert_ref = json.dumps(ref_dados) 
        lista_convert_defal = json.dumps(default_var) 

        cursor.execute('''
        INSERT INTO modelos (name,variaveis,ref_variaveis,default_variaveis,caminho_saida,arquivo_saida) VALUES (?,?,?,?,?,?)
    ''', (nome, lista_convert_dados,lista_convert_ref,lista_convert_defal,caminho_saida,arquivo_saida)
        )
        connection.commit()
        gerando_modelo(nome)
    finally:
        cursor.close()
        connection.close()

def retirar_dados(id_modelo):
    """Função para retirar os dados do modelo"""
    try:
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM modelos WHERE id = ?',(id_modelo,))
        resultado = cursor.fetchall()
        for var in resultado:
            modelo_id = var[0]
            nome = var[1]
            variavel = json.loads(var[2])
            ref_variavel = json.loads(var[3])
            defal_var = json.loads(var[4])
            caminho_saida = var[5]
            arquivo_saida = var[6]
        return (modelo_id,nome,variavel,ref_variavel,defal_var,caminho_saida,arquivo_saida)
    finally:
        cursor.close()
        connection.close()
def modificar(id,dados,ref_dados,default_var,nome_novo,caminho_saida,arquivo_saida):
    '''Função para editar os dados do modelo no banco'''
    try:
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        lista_convert_dados = json.dumps(dados)
        lista_convert_ref = json.dumps(ref_dados) 
        lista_convert_defal = json.dumps(default_var)
        cursor.execute('''
        UPDATE modelos
        SET default_variaveis = ?, ref_variaveis = ?, variaveis = ?, name = ?, caminho_saida = ?, arquivo_saida = ?
        WHERE id = ?;
    ''', (lista_convert_defal,lista_convert_ref,lista_convert_dados,nome_novo,caminho_saida,arquivo_saida,id)
        )
        connection.commit()
    finally:
        cursor.close()
        connection.close()

def listar(page):
    try:
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        page = int(page)
        itens_por_page = 15
        offset = (page - 1) * itens_por_page
        cursor.execute('SELECT id,name FROM modelos ORDER BY id ASC LIMIT ? OFFSET ?',(itens_por_page, offset,))
        resultado = cursor.fetchall()
        cursor.execute('SELECT COUNT(*) FROM modelos')
        total_itens = cursor.fetchone()[0]

        total_pages = (total_itens + itens_por_page - 1) // itens_por_page
        modelos = []
        for modelo in resultado:
            modelos.append({'id': modelo[0],'nome': modelo[1]})
        
        return [modelos,total_pages]
    finally:
        cursor.close()
        connection.close()

def deletar(modelo_id):
    try:
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute('''DELETE FROM modelos WHERE id = ?''',(modelo_id,))
        connection.commit()
    finally:
        cursor.close()
        connection.close()

def update():
    # Nome da tabela e da coluna que você deseja adicionar
    tabela = 'modelos'
    novas_colunas = ('caminho_saida', 'arquivo_saida')
    tipo_coluna = 'TEXT'

    # Verificando se a coluna já existe
    try:
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute(f"PRAGMA table_info({tabela})")
        colunas_existentes = [coluna[1] for coluna in cursor.fetchall()]

        # Se a coluna não existir, adicione-a
        for coluna in novas_colunas:
            if coluna not in colunas_existentes:
                cursor.execute(f"ALTER TABLE {tabela} ADD COLUMN {coluna} {tipo_coluna}")
                cursor.execute(f'UPDATE {tabela} SET {coluna} = ?', (' ',))
                connection.commit()
    finally:
        # Fechando a conexão
        cursor.close()
        connection.close()

def dados_anterior(id,dados):
    try:
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        lista_convert_dados = json.dumps(dados)
        cursor.execute('''
        UPDATE modelos
        SET default_variaveis = ?
        WHERE id = ?;
    ''', (lista_convert_dados,id)
        )
        connection.commit()
    finally:
        cursor.close()
        connection.close()

def retirar_dados_campo(id, campo):
    try:
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute(f'SELECT {campo} FROM modelos WHERE id = ?',( id,))
        resultado = cursor.fetchone()
        try:
            dados_campo = json.loads(resultado[0])
            return dados_campo
        except json.JSONDecodeError: 
            dados_campo = resultado[0]
            return dados_campo
    finally:
        cursor.close()
        connection.close()
