import os
import requests
import uuid
from dotenv import load_dotenv

load_dotenv()
from flask import Flask, redirect, url_for, request, render_template, session

template_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
template_dir = os.path.join(template_dir, 'templates')


app = Flask(__name__, template_folder=template_dir)


@app.route('/', methods=['GET'])
def index():
    return  print("SHOW")


@app.route('/', methods=['POST'])
def index_post():
    # LÊ os valores do formulário
    original_text = request.form['text']
    target_language = request.form['language']

    # Carregar os valores de .env
    key = os.environ['KEY']
    endpoint = os.environ['ENDPOINT']
    location = os.environ['LOCATION']

    # Indique O que queremos traduzir e a versão da API (3.0) e o idioma de destino
    path = '/translate?api-version=3.0'
    # Adicione o parâmetro de idioma de destino
    target_language_parameter = '&to=' + target_language
    # Crie o URL completo
    constructed_url = endpoint + path + target_language_parameter

    # Configure as informações do cabeçalho, que incluem nossa chave de assinatura
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # Crie o corpo da solicitação com o texto a ser traduzido
    body = [{'text': original_text}]

    # Faça a chamada usando post
    translator_request = requests.post(constructed_url, headers=headers, json=body)
    # Recupere a resposta JSON
    translator_response = translator_request.json()
    # Recupere a tradução
    translated_text = translator_response[0]['translations'][0]['text']

    # Chama o render template, passando o texto traduzido,
    # texto original e idioma de destino para o modelo
    return render_template(
        'results.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )


app.run()
