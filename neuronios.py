import mysql.connector

# Função para criar a conexão com o banco de dados
def conectar_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",  # O endereço do seu banco de dados
            user="root",  # Seu usuário do MySQL
            password="sua_senha",  # Sua senha do MySQL
            database="cerebro"  # O nome do banco de dados que você criou
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao MySQL: {err}")
        return None


# Função para registrar a conversa no banco de dados
def registrar_conversa(id_pessoa, tipo_mensagem, mensagem):
    conn = conectar_db()
    if conn:
        cursor = conn.cursor()
        query = "INSERT INTO historico_conversa (id_pessoa, tipo_mensagem, mensagem) VALUES (%s, %s, %s)"
        cursor.execute(query, (id_pessoa, tipo_mensagem, mensagem))
        conn.commit()
        cursor.close()
        conn.close()

# Função para obter o histórico de conversa
def obter_historico_conversa(id_pessoa):
    conn = conectar_db()
    if conn:
        cursor = conn.cursor()
        query = "SELECT tipo_mensagem, mensagem FROM historico_conversa WHERE id_pessoa = %s ORDER BY data DESC"
        cursor.execute(query, (id_pessoa,))
        resultado = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultado
