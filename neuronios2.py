import mysql.connector
from datetime import datetime

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="cerebro",
            charset="utf8mb4"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao MySQL: {err}")
        return None

def salvar_historico(id_pessoa, tipo_mensagem, mensagem):
    if tipo_mensagem == "tiberius":
        id_pessoa = 2

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()

        query_versao = "SELECT id FROM ativacoes ORDER BY id DESC LIMIT 1"
        cursor.execute(query_versao)
        versao = cursor.fetchone()

        if versao is None:
            print("ERRO: Não há versões no banco de dados.")
            conn.close()
            return

        id_versao = versao[0]

        query = "INSERT INTO historico_conversa (id_pessoa, tipo_mensagem, mensagem, data, id_ativacao) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (id_pessoa, tipo_mensagem, mensagem, datetime.now(), id_versao))
        conn.commit()
        cursor.close()
        conn.close()

def obter_historico(id_pessoa):
    query = "SELECT tipo_mensagem, mensagem FROM historico_conversa WHERE id_pessoa = %s ORDER BY data ASC"
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (id_pessoa,))
        resultados = cursor.fetchall()

        historico = []
        for resultado in resultados:
            tipo_mensagem = resultado["tipo_mensagem"]
            mensagem = resultado["mensagem"]
            historico.append({"tipo_mensagem": tipo_mensagem, "mensagem": mensagem})

        return historico
    except mysql.connector.Error as err:
        print(f"Erro ao obter histórico: {err}")
        return []

def buscar_mensagens_relacionadas(palavras_chave):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT tipo_mensagem, mensagem FROM historico_conversa WHERE mensagem LIKE %s"
        cursor.execute(query, ('%' + palavras_chave + '%',))
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultados

def registrar_versao(versao):
    conexao = get_db_connection()
    if conexao is None:
        print("Não foi possível conectar ao banco de dados.")
        return

    cursor = conexao.cursor()

    query = "INSERT INTO ativacoes (versao) VALUES (%s)"
    try:
        cursor.execute(query, (versao,))
        conexao.commit()
        print(f"Versão {versao} registrada com sucesso!")
    except mysql.connector.Error as err:
        print(f"Erro ao registrar a versão: {err}")

    cursor.close()
    conexao.close()
