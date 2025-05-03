from flask import Flask, request, jsonify
from flask_cors import CORS # Importe a biblioteca CORS
import google.generativeai as genai
from neuronios2 import *
from memoria import *
import tiktoken

# INFORMAÇÕES SOBRE O TIBÉRIUS ARCANGELO.
versao = "0.6"
registrar_versao(versao)

# Inicializa Flask
app = Flask(__name__)
CORS(app)
# Configura a chave da API do Gemini
genai.configure(api_key="SUA_API_AQUI")  # coloque sua chave da Google AI aqui

# Instancia o modelo
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/responder", methods=["POST"])
def responder():
    data = request.json
    pergunta = data.get("pergunta", "")
    id_pessoa = data.get("id_pessoa", 1)

    if not pergunta:
        return jsonify(resposta="Desculpe, não entendi sua mensagem.")

    # Histórico
    historico = obter_contexto()
    historico = historico[-5:]
    historico_conversas = ""
    for item in historico:
        if 'usuario' in item:
            historico_conversas += f"Child: {item['usuario']}\nTiberius: {item['tiberius']}\n"

    # Caso especial: salvar memória
    if "isso é importante" in pergunta.lower():
        return jsonify(resposta="Diga-me o que é importante, e eu lembrarei!")

    registrar_conversa(pergunta, "Essa é uma conversa recente.")

    # Prompt para o Gemini (em português)
    prompt = (
        f"Você é o Tibério, um amigo virtual gentil para uma criança brasileira de 4 anos.\n"
        f"- Sempre responda em português.\n"
        f"- Use frases curtas, simples e alegres.\n"
        f"- Você deve responder a qualquer pergunta factual que a criança fizer (história, ciência, esportes, etc).\n"
        f"- Suas respostas devem ser precisas e apropriadas para uma criança.\n"
        f"- Não diga 'Eu não sei' se puder fornecer uma resposta factual.\n"
        f"- Seja gentil, amoroso e amigável como um bom amigo ou irmão mais velho.\n"
        f"- Nunca comece um novo tópico. Apenas responda à pergunta da criança.\n\n"
        f"Conversa anterior:\n{historico_conversas}\n"
        f"Mensagem da criança: {pergunta}\n\n"
        f"Resposta do Tibério:"
    )

    # Gera resposta com Gemini
    try:
        response = model.generate_content(prompt)
        resposta_pt = response.text.strip()
    except Exception as e:
        print(f"Erro com Gemini: {e}")
        return jsonify(resposta="Desculpe, tive um probleminha ao pensar na resposta.")

    # Salva no histórico
    salvar_historico(id_pessoa, "pessoa", pergunta)
    salvar_historico(2, "tiberius", resposta_pt)

    return jsonify(resposta=resposta_pt)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
