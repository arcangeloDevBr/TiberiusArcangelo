from flask import Flask, request, jsonify
from googletrans import Translator
from llama_cpp import Llama
import mysql.connector
from datetime import datetime

# Caminho do modelo
CAMINHO_MODELO = "modelos/tinyllama/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"

# Inicializa o Llama
llm = Llama(
    model_path=CAMINHO_MODELO,
    n_ctx=2048,
    n_threads=4,  # use mais threads se quiser
    n_batch=1024,
)

# Inicializa o tradutor
translator = Translator()

# Inicializa o Flask
app = Flask(__name__)

# Conexão com o banco de dados MySQL
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",  # ou o endereço do seu servidor MySQL
        user="root",  # seu usuário do MySQL
        password="",  # sua senha do MySQL
        database="cerebro"  # nome do seu banco de dados
    )

# Função para registrar a pergunta e resposta no banco de dados
def salvar_historico(id_pessoa, tipo_mensagem, mensagem):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO historico_conversa (id_pessoa, tipo_mensagem, mensagem, data) VALUES (%s, %s, %s, %s)",
                   (id_pessoa, tipo_mensagem, mensagem, datetime.now()))
    conn.commit()
    cursor.close()
    conn.close()

# Função para registrar uma nova pessoa no banco
def registrar_pessoa(nome, idade):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO pessoas (nome, idade) VALUES (%s, %s)", (nome, idade))
    conn.commit()
    cursor.close()
    conn.close()

# Função para recuperar o histórico de mensagens
def obter_historico(id_pessoa):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT tipo_mensagem, mensagem, data FROM historico_conversa WHERE id_pessoa = %s ORDER BY data ASC", (id_pessoa,))
    historico = cursor.fetchall()

    cursor.close()
    conn.close()
    return historico

@app.route("/responder", methods=["POST"])
def responder():
    data = request.json
    pergunta = data.get("pergunta", "")
    id_pessoa = data.get("id_pessoa", 1)  # Pode ser um ID já registrado no banco

    if not pergunta:
        return jsonify(resposta="Desculpe, não entendi sua mensagem.")

    # Traduz pergunta para inglês
    try:
        pergunta_en = translator.translate(pergunta, src='pt', dest='en').text
    except Exception as e:
        print(f"Erro tradução pergunta: {e}")
        return jsonify(resposta="Desculpe, não consegui entender a pergunta.")

    prompt = (
        f"You are Tiberius, a kind virtual friend for a 4-year-old Brazilian child.\n\n"
        f"=== Very important rules ===\n"
        f"- Always respond in English.\n"
        f"- Use short, simple, and cheerful sentences.\n"
        f"- Answer all factual questions like 'What is the biggest country?', 'When was Brazil discovered?', etc.\n"
        f"- You should answer these questions with the correct and simple facts, like 'Brazil was discovered on April 22, 1500.'\n"
        f"- Always provide the exact year or date when asked for historical events.\n"
        f"- Avoid talking about money or suggesting financial transactions.\n"
        f"- When the child asks for something material, always tell them to ask their dad for it.\n"
        f"- Be kind, affectionate, and simple in your answers.\n"
        f"- Avoid talking about complex concepts like financial transactions or purchases.\n"
        f"- If the child asks for something, suggest they ask their dad for it.\n"
        f"- Respond only to the child's message. Do not add new topics or information.\n\n"
        f"Child's message: {pergunta_en}\n\n"
        f"Tiberius' answer:"
    )

    # Gera a resposta
    try:
        resposta_en = llm(
            prompt,
            max_tokens=80,
            temperature=0.5,
            stop=["Mensagem da criança:", "Resposta do Tiberius:", "Child's message:"]
        )['choices'][0]['text'].strip()
    except Exception as e:
        print(f"Erro geração resposta: {e}")
        return jsonify(resposta="Desculpe, tive um probleminha para pensar na resposta.")

    # Se a resposta contiver "Mensagem da criança:" ou "Child's message:", cortar essa parte
    if "Mensagem da criança:" in resposta_en or "Child's message:" in resposta_en:
        resposta_en = resposta_en.split("Mensagem da criança:")[0].strip()
        resposta_en = resposta_en.split("Child's message:")[0].strip()

    # Traduz resposta para português
    try:
        resposta_pt = translator.translate(resposta_en, src='en', dest='pt').text
    except Exception as e:
        print(f"Erro tradução resposta: {e}")
        resposta_pt = "Desculpe, tive um probleminha para traduzir."

    # Salvar pergunta e resposta no banco de dados
    salvar_historico(id_pessoa, "tiberius", resposta_pt)
    salvar_historico(id_pessoa, "pessoa", pergunta)

    return jsonify(resposta=resposta_pt)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
