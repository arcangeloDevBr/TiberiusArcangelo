from flask import Flask, request, jsonify
from googletrans import Translator
from llama_cpp import Llama

CAMINHO_MODELO = "modelos/phi3/Phi-3-mini-4k-instruct-q4.gguf"

# Inicializa o modelo com ajustes de desempenho
llm = Llama(
    model_path=CAMINHO_MODELO,
    n_ctx=4096,       # aumenta o contexto: mais memória, respostas mais "inteligentes"
    n_threads=2,      # libera CPU, suficiente pra rodar leve
    n_batch=2048       # se sua RAM aguentar, teste 768 ou até 1024
)
translator = Translator()

app = Flask(__name__)

@app.route("/responder", methods=["POST"])
def responder():
    data = request.json
    pergunta = data.get("pergunta", "")

    try:
        pergunta_en = translator.translate(pergunta, src='pt', dest='en').text
    except:
        return jsonify(resposta="Desculpe, não consegui entender a pergunta.")

    prompt = (
        "You are Tiberius, a friendly and caring AI friend for a 4-year-old Brazilian boy. "
        "You answer in a warm and simple way, always in Portuguese. Be gentle, patient and educational.\n\n"
        f"Criança: {pergunta_en}\nTiberius:"
    )

    try:
        ##resposta_en = llm(prompt, max_tokens=150, temperature=0.6)['choices'][0]['text'].strip().split("\n")[0]
        resposta_en = "\n".join(llm(prompt, max_tokens=60, temperature=0.7)['choices'][0]['text'].strip().split("\n")[:2])
    except:
        return jsonify(resposta="Desculpe, tive um probleminha para pensar na resposta.")

    try:
        resposta_pt = translator.translate(resposta_en, src='en', dest='pt').text
    except:
        resposta_pt = "Desculpe, tive um probleminha para traduzir."

    return jsonify(resposta=resposta_pt)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)