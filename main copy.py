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

    return jsonify(resposta=resposta_pt)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
