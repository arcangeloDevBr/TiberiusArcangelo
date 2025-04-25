import mysql.connector
import json

def conectar_db():
    """Conecta ao banco de dados MySQL e retorna a conexão e o cursor."""
    db = mysql.connector.connect(
        host="localhost",
        user="root",  # Usuário do MySQL
        password="",  # Senha do MySQL (caso tenha)
        database="cerebro"  # Nome do banco de dados
    )
    return db, db.cursor()

def salvar_preferencias(nome, preferencias):
    """Salva as preferências de um usuário no banco de dados."""
    db, cursor = conectar_db()
    preferencias_json = json.dumps(preferencias)  # Convertendo para JSON
    cursor.execute("INSERT INTO pessoas (nome, preferencias) VALUES (%s, %s)", (nome, preferencias_json))
    db.commit()
    cursor.close()
    db.close()

def recuperar_preferencias(nome):
    """Recupera as preferências de um usuário do banco de dados."""
    db, cursor = conectar_db()
    cursor.execute("SELECT preferencias FROM pessoas WHERE nome = %s", (nome,))
    preferencias = cursor.fetchone()
    cursor.close()
    db.close()
    
    if preferencias:
        return json.loads(preferencias[0])  # Convertendo de volta de JSON para dict
    return None