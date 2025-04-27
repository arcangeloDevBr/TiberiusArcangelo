# cria_banco.py
import sqlite3

# Cria ou conecta no banco de dados
conn = sqlite3.connect('memoria.db')
cursor = conn.cursor()

# Cria a tabela de mensagens
cursor.execute('''
CREATE TABLE IF NOT EXISTS mensagens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quem TEXT,
    mensagem TEXT,
    hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()
conn.close()

print("Banco de dados criado com sucesso!")