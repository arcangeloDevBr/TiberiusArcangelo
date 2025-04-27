#!/bin/bash

cd "$(dirname "$0")"  # Garante que está na pasta do script

if [ ! -d "venv" ]; then
  echo "Criando ambiente virtual..."
  python3 -m venv venv
  source venv/bin/activate
  pip install --upgrade pip
  pip install pyttsx3 SpeechRecognition googletrans==4.0.0rc1 llama-cpp-python pyaudio
else
  source venv/bin/activate
fi

echo "Iniciando Tibério..."
python3 main.py