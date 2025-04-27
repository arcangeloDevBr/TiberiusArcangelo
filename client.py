# cliente_tiberius.py
import requests

print("=== Cliente do Tiberius ===")
#servidor = input("Digite o IP do servidor (ex: 192.168.1.100:5000): ")
servidor = "192.168.127.10:5000"

while True:
    pergunta = input("Você: ")
    if not pergunta.strip():
        break

    try:
        resposta = requests.post(f"http://{servidor}/responder", json={"pergunta": pergunta}, timeout=20)
        if resposta.status_code == 200:
            dados = resposta.json()
            print(f"Tiberius: {dados['resposta']}\n")
        else:
            print(f"Erro na resposta do servidor: {resposta.status_code}")
    except Exception as e:
        print(f"Erro na conexão: {e}")
