import pyttsx3

# Função para listar as vozes disponíveis
def listar_vozes():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        print(f"ID: {voice.id}, Name: {voice.name}, Languages: {voice.languages}")

# Chame listar_vozes() para ver as vozes disponíveis
listar_vozes()