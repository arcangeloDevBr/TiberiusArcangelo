import pyttsx3
import speech_recognition as sr
import requests

# Configura o motor de voz
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    if 'portuguese' in voice.languages or 'pt' in voice.id.lower():
        engine.setProperty('voice', voice.id)
        break

def falar(texto):
    print(f"Tibério: {texto}")
    engine.say(texto)
    engine.runAndWait()

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
    except:
        print("Não entendi.")
        return None

def main():
    falar("Oi! Eu sou o Tibério. Vamos brincar e aprender juntos?")
    while True:
        comando = escutar()
        if comando and 'sair' in comando.lower():
            falar("Tchauzinho! Até a próxima brincadeira!")
            break

        if comando:
            try:
                resposta = requests.post("http://<IP_DO_SERVIDOR>:5000/responder", json={"pergunta": comando})
                falar(resposta.json().get("resposta", "Não entendi."))
            except:
                falar("Não consegui falar com o servidor.")

if __name__ == "__main__":
    main()
