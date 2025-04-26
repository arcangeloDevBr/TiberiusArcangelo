import os
import pyttsx3
import speech_recognition as sr
from googletrans import Translator
from llama_cpp import Llama

# Configurações
CAMINHO_MODELO = "modelos/phi3/Phi-3-mini-4k-instruct-q4.gguf"

# Inicializa o modelo
llm = Llama(model_path=CAMINHO_MODELO, n_ctx=2048, n_threads=4)

# Inicializa o tradutor
translator = Translator()

# Inicializa o motor de voz fora das funções para não reiniciar toda hora
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    if 'portuguese' in voice.languages or 'pt' in voice.id.lower():
        engine.setProperty('voice', voice.id)
        break

# Função para falar
def falar(texto):
    print(f"Tibério: {texto}")
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
    except:
        return "Desculpe, não consegui entender a pergunta."

    prompt = (
        "You are Tiberius, a friendly and caring AI friend for a 4-year-old Brazilian boy. "
        "You answer in a warm and simple way, always in Portuguese. Be gentle, patient and educational.\n\n"
        f"Criança: {pergunta_en}\nTiberius:"
    )

    try:
        resposta_en = llm(prompt, max_tokens=150, temperature=0.6)['choices'][0]['text'].strip().split("\n")[0]
    except:
        return "Desculpe, tive um probleminha para pensar na resposta."

    try:
        resposta_pt = translator.translate(resposta_en, src='en', dest='pt').text
    except:
        resposta_pt = "Desculpe, tive um probleminha para traduzir."

    return resposta_pt

# Loop principal
def main():
    falar("Oi! Eu sou o Tibério. Vamos brincar e aprender juntos?")
    while True:
        comando = escutar()
        if comando:
            if 'sair' in comando.lower():
                falar("Tchauzinho! Até a próxima brincadeira!")
                break
            else:
                resposta = responder(comando)
                falar(resposta)
        else:
            falar("Desculpe, não entendi. Pode repetir?")

if __name__ == "__main__":
    main()
