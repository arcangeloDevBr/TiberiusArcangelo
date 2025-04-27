# servidor_tiberius.py
from flask import Flask, request, jsonify
from googletrans import Translator
from llama_cpp import Llama
import sqlite3

CAMINHO_MODELO = "modelos/tinyllama/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"  # modelo novo!
DATABASE = 'memoria.db'

llm = Llama(
    model_path=CAMINHO_MODELO,
    n_ctx=2048,
    n_threads=4,
    n_batch=512,
)

translator = Translator()
app = Flask(__name__)

def salvar_mensagem(quem, mensagem):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO mensagens (quem, mensagem) VALUES (?, ?)", (quem, mensagem))
    conn.commit()
    conn.close()

def pegar_historico(limit=6):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT quem, mensagem FROM mensagens ORDER BY id DESC LIMIT ?", (limit,))
    dados = cursor.fetchall()
    conn.close()
    return dados[::-1]  # inverter para ordem correta

@app.route("/responder", methods=["POST"])
def responder():
    data = request.json
    pergunta = data.get("pergunta", "")

    try:
        pergunta_en = translator.translate(pergunta, src='pt', dest='en').text
    except Exception as e:
        print(f"Erro tradução pergunta: {e}")
        return jsonify(resposta="Desculpe, não consegui entender a pergunta.")

    salvar_mensagem("Criança", pergunta)

    historico = pegar_historico()

    contexto = "\n".join([f"{quem}: {msg}" for quem, msg in historico])

    prompt = (
        "Você é Tiberius, um amigo virtual gentil para uma criança brasileira de 4 anos. "
        "Responda em português simples, curto e carinhoso. "
        "Use o histórico para entender a conversa. "
        "Não continue a conversa depois da resposta.\n\n"
        f"Histórico:\n{contexto}\n\n"
        f"Mensagem da criança: {pergunta_en}\nResposta do Tiberius:"
    )

    try:
        resposta_en = llm(prompt, max_tokens=60, temperature=0.4)['choices'][0]['text'].strip()
    except Exception as e:
        print(f"Erro geração resposta: {e}")
        return jsonify(resposta="Desculpe, tive um probleminha para pensar na resposta.")

    try:
        resposta_pt = translator.translate(resposta_en, src='en', dest='pt').text
    except Exception as e:
        print(f"Erro tradução resposta: {e}")
        resposta_pt = "Desculpe, tive um probleminha para traduzir."

    salvar_mensagem("Tiberius", resposta_pt)

    return jsonify(resposta=resposta_pt)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
