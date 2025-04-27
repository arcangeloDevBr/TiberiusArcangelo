import speech_recognition as sr
import pyttsx3
from googletrans import Translator
import requests

# =====================
# CONFIGURAÇÃO
# =====================
HUGGINGFACE_TOKEN = "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"  # <-- Cole seu token aqui
API_URL = "https://api-inference.huggingface.co/models/openchat/openchat-3.5-0106"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}

translator = Translator()

# Fala com voz em português
def falar(texto):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'portuguese' in voice.languages or 'pt' in voice.id.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.say(texto)
    engine.runAndWait()

# Captura o áudio e reconhece a fala
def escutar():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Diga algo...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        texto = r.recognize_google(audio, language="pt-BR")
        print("Você disse: " + texto)
        return texto
    except sr.UnknownValueError:
        print("Não entendi o que você disse.")
        return None
    except sr.RequestError as e:
        print(f"Erro de requisição; {e}")
        return None

# Gera uma resposta com IA usando Hugging Face
def responder_com_ia(pergunta):
    try:
        pergunta_en = translator.translate(pergunta, src='pt', dest='en').text
        print(f"Pergunta em inglês: {pergunta_en}")
    except Exception as e:
        print(f"Erro na tradução da pergunta: {e}")
        return "Desculpe, não consegui traduzir sua pergunta."

    payload = {
        "inputs": f"<|user|>\n{pergunta_en}\n<|assistant|>\n",
        "parameters": {"max_new_tokens": 100, "temperature": 0.7}
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        resposta_en = response.json()
        texto_gerado = resposta_en[0]["generated_text"].split("<|assistant|>\n")[-1].strip() \
            if isinstance(resposta_en, list) else "Desculpe, não entendi."
        print(f"Resposta gerada em inglês: {texto_gerado}")
    except Exception as e:
        print(f"Erro ao gerar resposta: {e}")
        return "Desculpe, a IA não respondeu corretamente."

    try:
        resposta_pt = translator.translate(texto_gerado, src='en', dest='pt').text
        print(f"Resposta traduzida: {resposta_pt}")
    except Exception as e:
        print(f"Erro ao traduzir resposta: {e}")
        resposta_pt = "Desculpe, não consegui traduzir a resposta."

    return resposta_pt

# Loop principal
def main():
    falar("Olá, eu sou o Tibério. Como posso te ajudar?")
    while True:
        comando = escutar()
        if comando:
            if 'sair' in comando.lower():
                falar("Até mais! Foi bom conversar com você.")
                break
            else:
                resposta = responder_com_ia(comando)
                falar(f"Tibério respondeu: {resposta}")
        else:
            falar("Desculpe, não entendi.")

# Execução
if __name__ == "__main__":
    main()
