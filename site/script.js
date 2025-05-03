async function enviarPergunta() {
    const perguntaInput = document.getElementById("pergunta");
    const respostaDiv = document.getElementById("resposta");
    const rostoImg = document.getElementById("rosto");

    const pergunta = perguntaInput.value.trim();
    if (pergunta === "") {
        respostaDiv.innerText = "Por favor, escreva uma pergunta!";
        return;
    }

    respostaDiv.innerText = "Tiberius está pensando... 🤔";

    try {
        const response = await fetch('/responder', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ pergunta })
        });

        const data = await response.json();
        const resposta = data.resposta;

        respostaDiv.innerText = resposta;
        escolherRosto(resposta);

    } catch (error) {
        console.error('Erro ao enviar pergunta:', error);
        respostaDiv.innerText = "Tive um probleminha! 😢";
    }

    perguntaInput.value = "";
}

function escolherRosto(texto) {
    texto = texto.toLowerCase();

    if (texto.includes("amor") || texto.includes("gosto") || texto.includes("lindo") || texto.includes("querido")) {
        mudarImagem('apaixonado.png');
    } else if (texto.includes("feliz") || texto.includes("alegre") || texto.includes("legal") || texto.includes("bom")) {
        mudarImagem('feliz.png');
    } else if (texto.includes("triste") || texto.includes("chato") || texto.includes("pena")) {
        mudarImagem('triste.png');
    } else if (texto.includes("bravo") || texto.includes("chateado") || texto.includes("raiva")) {
        mudarImagem('bravo.png');
    } else if (texto.includes("curioso") || texto.includes("perguntar") || texto.includes("saber")) {
        mudarImagem('curioso.png');
    } else if (texto.includes("surpreso") || texto.includes("uau") || texto.includes("nossa")) {
        mudarImagem('surpreso.png');
    } else {
        mudarImagem('feliz.png'); // padrão
    }
}

function mudarImagem(nomeArquivo) {
    const rostoImg = document.getElementById("rosto");
    rostoImg.src = "imagens/" + nomeArquivo;
}