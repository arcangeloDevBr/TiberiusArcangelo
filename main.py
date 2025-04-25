import speech_recognition as sr
import pyttsx3
from transformers import AutoModelForCausalLM, AutoTokenizer
from googletrans import Translator
import torch

# Inicializa tradutor
translator = Translator()

# Carrega modelo e tokenizer da IA
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# Histórico de conversa
chat_history_ids = None

# Função para falar usando voz em português
def falar(texto):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'portuguese' in voice.languages or 'pt' in voice.id.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.say(texto)
    engine.runAndWait()

# Função para escutar o usuário
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

# Função de resposta inteligente com contexto
def responder_com_ia(pergunta):
    global chat_history_ids

    # Traduz a pergunta para inglês
    pergunta_en = translator.translate(pergunta, src='pt', dest='en').text
    print(f"Pergunta em inglês: {pergunta_en}")

    # Tokeniza a pergunta
    nova_entrada_ids = tokenizer.encode(pergunta_en + tokenizer.eos_token, return_tensors='pt')

    # Concatena com histórico, se houver
    bot_input_ids = torch.cat([chat_history_ids, nova_entrada_ids], dim=-1) if chat_history_ids is not None else nova_entrada_ids

    # Gera resposta
    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

    # Extrai a nova resposta
    resposta_en = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    print(f"Resposta gerada em inglês: {resposta_en}")

    # Traduz para português
    resposta_pt = translator.translate(resposta_en, src='en', dest='pt').text
    print(f"Resposta traduzida: {resposta_pt}")

    return resposta_pt

# Função principal do Tiberius
def main():
    falar("Olá, sou Tiberius. Como posso te ajudar?")
    while True:
        comando = escutar()
        if comando:
            comando_limpo = comando.lower().strip().replace('.', '').replace('!', '').replace('?', '')
            if 'sair' in comando_limpo:
                falar("Até logo!")
                break
            else:
                resposta = responder_com_ia(comando)
                falar(f"Tiberius respondeu: {resposta}")
        else:
            falar("Desculpe, não entendi.")

# Executa o programa
if __name__ == "__main__":
    main()
