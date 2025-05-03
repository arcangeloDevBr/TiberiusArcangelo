# Tibério - Backend

Este projeto fornece o backend para o amigo virtual Tibério, voltado para crianças pequenas. Utiliza o modelo de linguagem Gemini do Google para responder a perguntas de forma amigável e apropriada.

**Versão Atual: 0.6**

## Visão Geral

Este é o componente backend do projeto Tibério, construído com Python e Flask. Ele se conecta ao modelo Gemini do Google para processar perguntas e gerar respostas em formato JSON. Este backend foi projetado para ser integrado com uma interface de usuário (atualmente em desenvolvimento/não incluído neste repositório) e futuramente com um robô físico (via Arduino).

**Licenças:**

* **Python:** Python é distribuído sob uma licença de código aberto permissiva. Você pode usá-lo e distribuí-lo gratuitamente, mesmo para projetos comerciais. Mais detalhes podem ser encontrados na [Python Software Foundation License](https://docs.python.org/3/license.html).
* **MySQL:** O MySQL possui uma versão Community (comunitária) que é gratuita e de código aberto, licenciada sob a GNU General Public License (GPL). Para uso em alguns cenários comerciais, licenças comerciais podem ser necessárias. Para este projeto, assumimos o uso da versão Community para aprendizado e desenvolvimento. Consulte a [licença do MySQL](https://www.mysql.com/about/legal/licensing/) para mais informações sobre os termos de licenciamento da versão que você está utilizando.
* **Google AI Gemini 1.5:** O acesso ao modelo Gemini 1.5 é atualmente oferecido gratuitamente para desenvolvedores através do Google AI Studio, com certas cotas e termos de uso. É importante revisar os [Termos de Serviço do Google AI Studio](https://makersuite.google.com/terms) para entender as condições de uso, incluindo quaisquer limitações em aplicações comerciais.

**Integração Futura:** Em breve, este projeto será integrado com o Arduino para dar vida ao Tibério como um robô físico, expandindo a interação para o mundo real.

## Funcionalidades

- **API para interação:** Fornece uma API HTTP (através da rota `/responder`) para receber perguntas via POST.
- **Respostas do Gemini:** Utiliza o poder do modelo Gemini para gerar respostas contextuais e informativas em português.
- **Focado em crianças:** As respostas são formatadas para serem curtas, simples, alegres e apropriadas para uma criança de 4 anos.
- **Personalidade amigável:** O prompt do Gemini define o Tibério como um amigo virtual gentil e atencioso.
- **Histórico de conversas:** Mantém um breve histórico das últimas conversas para fornecer contexto ao Gemini (implementação nos arquivos `neuronios2.py` e `memoria.py`).
- **Memória (funcionalidade parcial):** Inclui lógica para salvar informações importantes (implementação nos arquivos `neuronios2.py` e `memoria.py`), embora possa estar em desenvolvimento.
- **Preparado para integração com Arduino:** A arquitetura do projeto está sendo pensada para futura integração com uma plataforma Arduino, permitindo que o Tibério interaja com o mundo físico.

## Pré-requisitos

Antes de executar o projeto, você precisará ter instalado:

- **Python 3.6+:** A linguagem de programação para o backend.
- **pip:** O gerenciador de pacotes para Python (geralmente instalado com o Python).
- **Uma chave de API do Google AI:** Necessária para autenticar e usar o modelo Gemini. Você pode obtê-la no [Google AI Studio](https://makersuite.google.com/).
- **MySQL (opcional):** Se você estiver usando o sistema de memória e histórico de conversas que parecem estar nos arquivos `neuronios2.py` e `memoria.py`.
- **Ambiente de desenvolvimento Arduino (futuro):** Para a integração com o robô físico.

## Configuração

1.  **Clone o repositório:**
    ```bash
    git clone [https://[link do seu repositório]]
    cd [nome do seu repositório]
    ```
    *(Substitua `[https://[link do seu repositório]]` pelo link real do seu repositório no GitHub.)*

2.  **Crie um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Linux/macOS
    venv\Scripts\activate  # No Windows
    ```

3.  **Instale as dependências do backend:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Você precisará criar um arquivo `requirements.txt` listando as dependências do seu projeto, como `Flask`, `Flask-CORS`, `google-generativeai`, `mysql-connector-python` (se estiver usando). Você pode gerar este arquivo com `pip freeze > requirements.txt` após instalar as bibliotecas.)*

4.  **Configure a chave da API do Google AI:**
    Abra o arquivo `novo.py` e substitua `"SUA_API_AQUI"` pela sua chave de API real do Google AI. **Mantenha esta chave segura!**

5.  **Configure o banco de dados MySQL (se necessário):**
    Se você estiver usando o banco de dados MySQL para histórico e memória, certifique-se de que o banco de dados `cerebro` e a tabela `historico_conversa` estejam configurados corretamente (com charset `utf8mb4` para suporte a emojis, se necessário) e atualize as credenciais de acesso nos seus arquivos `neuronios2.py` e `memoria.py`.

6.  **Configuração do Arduino (futuro):** Detalhes sobre a configuração do Arduino serão adicionados conforme a integração progredir.

## Execução

1.  **Execute o servidor Flask (backend):**
    No seu terminal, dentro do diretório do projeto e com o ambiente virtual ativado (se você o usou), execute:
    ```bash
    python novo.py
    ```
    Você deverá ver uma mensagem indicando que o servidor Flask está rodando em `http://127.0.0.1:5000` e `http://[seu_ip_local]:5000` (substitua `[seu_ip_local]` pelo IP da sua máquina na rede, se aplicável).

## Estrutura de Arquivos
Tiberius Arcangelo/
├── novo.py           # O script principal do servidor Flask
├── neuronios2.py       # (Provavelmente contém lógica de histórico/memória)
├── memoria.py          # (Provavelmente contém lógica de histórico/memória)
└── README.md         # Este arquivo
└── requirements.txt  # (Opcional, lista as dependências do Python)


