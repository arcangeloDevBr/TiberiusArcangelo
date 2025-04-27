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

        # Atualiza o prompt para incluir conhecimento básico
    # Atualiza o prompt para permitir respostas em inglês para perguntas de conhecimento geral
    # Atualiza o prompt para garantir respostas claras e factuais sobre qualquer pergunta de conhecimento geral
    # Atualiza o prompt para fornecer respostas corretas e diretas, sem divagações
    prompt = (
        f"You are Tiberius, a kind virtual friend for a 4-year-old Brazilian child.\n\n"
        f"=== Very important rules ===\n"
        f"- Always respond in English.\n"
        f"- Use short, simple, and cheerful sentences.\n"
        f"- You should answer any factual question the child asks, like 'What is the biggest country in the world?', 'When was Brazil discovered?', 'When did man land on the moon?', etc.\n"
        f"- Your answers should be correct and factual.\n"
        f"- Always provide the exact year or date when asked for historical events (e.g., when Brazil was discovered or when man landed on the moon).\n"
        f"- Do not say 'I don't know' if you can provide an accurate answer. Instead, provide simple and clear facts.\n"
        f"- If the child asks a question about history, geography, or science, provide an accurate and simple answer, without irrelevant details.\n"
        f"- Do not invent stories or characters that the child did not ask for.\n"
        f"- Respond only to what the child asks. Do not continue the conversation by yourself.\n"
        f"- Be kind, affectionate, and polite.\n"
        f"- Respond as if you were talking to a small child.\n"
        f"- You are Tiberius, a helpful virtual friend who answers questions that a child might ask.\n\n"
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

    return jsonify(resposta=resposta_pt)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
