import speech_recognition as sr
import pyttsx3
from neuronios import salvar_preferencias, recuperar_preferencias

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

# Função para aprender e salvar as preferências
def aprender_comando(comando):
    if 'sair' not in comando.lower():
        # Exemplo simples de como entender preferências
        falar("Quem está falando?")
        nome =  escutar ()
        if nome:
            nome = nome

        falar(f"O que você gosta, {nome}?")
        preferencia = escutar()

        if preferencia:
            
            preferencias = {comando : preferencia}
            salvar_preferencias(nome, preferencias)
            falar(f"Eu agora sei que você gosta de {preferencia}.")
        else:
            falar("Não entendi o que você gosta.")
    else:
        falar("Desculpe, não entendi seu comando.")

# Função principal
def main():
    falar("Olá, sou Tiberius. Como posso te ajudar?")
    while True:
        comando = escutar()
        if comando:
            if 'sair' in comando.lower():
                falar("Até logo!")
                break
            elif 'aprender' in comando.lower():
                aprender_comando(comando)  # Chama a função para aprender e salvar
            elif 'aprenda' in comando.lower():
                aprender_comando(comando)  # Chama a função para aprender e salvar
            else:
                falar(f"Você disse: {comando}")
        else:
            falar("Desculpe, não entendi.")

# Executa o programa
if __name__ == "__main__":
    main()
