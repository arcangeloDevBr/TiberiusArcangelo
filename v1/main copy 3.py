from flask import Flask, request, jsonify
from googletrans import Translator
from llama_cpp import Llama

CAMINHO_MODELO = "modelos/phi2/phi-2.Q4_K_M.gguf"

llm = Llama(
    model_path=CAMINHO_MODELO,
    n_ctx=4096,          # Aumentado para 4096 tokens
    n_threads=4,         # Usar mais threads (ajuste para seu CPU)
    n_batch=1024,        # Lotes maiores para mais velocidade
    n_gpu_layers=0       # Coloque >0 se quiser usar GPU (me avise!)
)

translator = Translator()
app = Flask(__name__)

@app.route("/responder", methods=["POST"])
def responder():
    data = request.json
    pergunta = data.get("pergunta", "")

    try:
        pergunta_en = translator.translate(pergunta, src='pt', dest='en').text
    except Exception as e:
        print(f"Erro tradução pergunta: {e}")
        return jsonify(resposta="Desculpe, não consegui entender a pergunta.")

    # Prompt reforçado
    prompt = (
        "Você é Tiberius, um amigo virtual gentil para uma criança brasileira de 4 anos. "
        "Responda SOMENTE como Tiberius, usando português simples, curto e carinhoso. "
        "Responda apenas UMA vez, com uma frase ou duas no máximo. "
        "NÃO inicie novas mensagens, NÃO continue a conversa, NÃO repita o que a criança falou. "
        "Seja sempre gentil e alegre.\n\n"
        f"Mensagem da criança: {pergunta_en}\nResposta do Tiberius:"
    )

    try:
        resposta_en = llm(
            prompt,
            max_tokens=60,
            temperature=0.4,
            stop=["\nMensagem da criança:", "\nCriança:", "\nResposta do Tiberius:"]
        )['choices'][0]['text'].strip()
    except Exception as e:
        print(f"Erro geração resposta: {e}")
        return jsonify(resposta="Desculpe, tive um probleminha para pensar na resposta.")

    try:
        resposta_pt = translator.translate(resposta_en, src='en', dest='pt').text
    except Exception as e:
        print(f"Erro tradução resposta: {e}")
        resposta_pt = "Desculpe, tive um probleminha para traduzir."

    return jsonify(resposta=resposta_pt)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
