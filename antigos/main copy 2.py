import os
import pyttsx3
import speech_recognition as sr
from googletrans import Translator
from llama_cpp import Llama

# Configurações
CAMINHO_MODELO = "modelos/phi3/phi-3-mini-4k-instruct.Q4_K_M.gguf"

# Inicializa o modelo
llm = Llama(model_path=CAMINHO_MODELO, n_ctx=4096, n_threads=4)

# Inicializa o tradutor
translator = Translator()

# Função para falar
def falar(texto):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'portuguese' in voice.languages or 'pt' in voice.id.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.say(texto)
    engine.runAndWait()

# Função para escutar
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
        print(f"Erro de requisição: {e}")
        return None

# Função para gerar resposta
def responder(pergunta):
    try:
        pergunta_en = translator.translate(pergunta, src='pt', dest='en').text
    except Exception as e:
        return "Desculpe, não consegui traduzir sua pergunta."

    prompt = f"User: {pergunta_en}\nAssistant:"
    try:
        resposta_en = llm(prompt, max_tokens=200, temperature=0.7)['choices'][0]['text'].strip()
    except Exception as e:
        return "Desculpe, ocorreu um erro ao gerar a resposta."

    try:
        resposta_pt = translator.translate(resposta_en, src='en', dest='pt').text
    except Exception as e:
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
                resposta = responder(comando)
                falar(f"Tibério respondeu: {resposta}")
        else:
            falar("Desculpe, não entendi.")

if __name__ == "__main__":
    main()
