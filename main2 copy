from flask import Flask, request, jsonify
from googletrans import Translator
from llama_cpp import Llama

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

@app.route("/responder", methods=["POST"])
def responder():
    data = request.json
    pergunta = data.get("pergunta", "")

    if not pergunta:
        return jsonify(resposta="Desculpe, não entendi sua mensagem.")

    # Traduz pergunta para inglês
    try:
        pergunta_en = translator.translate(pergunta, src='pt', dest='en').text
    except Exception as e:
        print(f"Erro tradução pergunta: {e}")
        return jsonify(resposta="Desculpe, não consegui entender a pergunta.")

    # Gera o prompt com a pergunta corretamente inserida (traduzido para inglês)
    prompt = (
        f"You are Tiberius, a kind virtual friend to a 4-year-old Brazilian child.\n\n"
        f"=== Very important rules ===\n"
        f"- Always respond in English.\n"
        f"- Use short, simple, and cheerful sentences.\n"
        f"- DO NOT invent ANYTHING. Do not create stories or contexts that the child did not provide.\n"
        f"- DO NOT add information that the child did not say. Do not invent 'messages from the child.'\n"
        f"- DO NOT create characters or contexts beyond what the child says.\n"
        f"- If the child asks for a story, tell a very short and simple story.\n"
        f"- DO NOT continue the conversation on your own, just respond to what was asked.\n"
        f"- DO NOT mention your name (Tiberius) in the answers, just respond as if you were a virtual friend.\n"
        f"- Be kind, affectionate, and polite.\n"
        f"- Respond as if you were talking to a small child.\n"
        f"- Respond ONLY ONCE and then stop your reply.\n\n"
        f"Child's message: {pergunta_en}\n\n"
        f"Tiberius' answer:"
    )

    # Gera a resposta
    try:
        resposta_en = llm(
            prompt,
            max_tokens=80,
            temperature=0.5,
            stop=["Mensagem da criança:", "Resposta do Tiberius:"]
        )['choices'][0]['text'].strip()
    except Exception as e:
        print(f"Erro geração resposta: {e}")
        return jsonify(resposta="Desculpe, tive um probleminha para pensar na resposta.")

    # Traduz resposta para português
    try:
        resposta_pt = translator.translate(resposta_en, src='en', dest='pt').text
    except Exception as e:
        print(f"Erro tradução resposta: {e}")
        resposta_pt = "Desculpe, tive um probleminha para traduzir."

    return jsonify(resposta=resposta_pt)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
