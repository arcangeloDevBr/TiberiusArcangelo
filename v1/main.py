from flask import Flask, request, jsonify
from flask_cors import CORS
from googletrans import Translator
from llama_cpp import Llama

CAMINHO_MODELO = "modelos/phi2/phi-2.Q4_K_M.gguf"

llm = Llama(
    model_path=CAMINHO_MODELO,
    n_ctx=4096,
    n_threads=8,
    n_batch=1024,
)

translator = Translator()
app = Flask(__name__)
CORS(app)  # <- ADICIONADO AQUI

@app.route("/responder", methods=["POST"])
def responder():
    data = request.json
    pergunta = data.get("pergunta", "")

    try:
        pergunta_en = translator.translate(pergunta, src='pt', dest='en').text
    except Exception as e:
        print(f"Erro tradução pergunta: {e}")
        return jsonify(resposta="Desculpe, não consegui entender a pergunta.")

    prompt = (
    "Atue como Tiberius, um amigo virtual carinhoso que conversa com uma criança brasileira de 4 anos. "
    "Quando receber uma mensagem, responda com uma frase curta, carinhosa e fechada. "
    "Não continue a conversa, não invente falas da criança. "
    "A resposta deve ser somente a resposta do Tiberius.\n\n"
    f"Mensagem recebida: {pergunta_en}\nResposta:"
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

    return jsonify(resposta=resposta_pt)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
