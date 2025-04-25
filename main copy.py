# main.py

import speech_recognition as sr
import pyttsx3

# Função para iniciar a fala
def falar(texto):
    engine = pyttsx3.init()
    
    # Obtém todas as vozes disponíveis
    voices = engine.getProperty('voices')

    # Escolher a voz em português
    for voice in voices:
        if 'portuguese' in voice.languages:
            engine.setProperty('voice', voice.id)
            break

    engine.say(texto)
    engine.runAndWait()

# Função para escutar a fala
def escutar():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Diga algo...")
        r.adjust_for_ambient_noise(source)  # Ajusta para o ruído ambiente
        audio = r.listen(source)  # Captura o áudio
    try:
        texto = r.recognize_google(audio, language="pt-BR")  # Reconhecimento de fala em português
        print("Você disse: " + texto)
        return texto
    except sr.UnknownValueError:
        print("Não entendi o que você disse.")
        return None
    except sr.RequestError as e:
        print(f"Erro de requisição; {e}")
        return None

# Função principal
def main():
    falar("Olá, sou Tiberius. Como posso te ajudar?")
    while True:
        comando = escutar()
        if comando:
            if 'sair' in comando.lower():
                falar("Até logo!")
                break
            else:
                falar(f"Você disse: {comando}")
        else:
            falar("Desculpe, não entendi.")

# Executa o programa
if __name__ == "__main__":
    main()
