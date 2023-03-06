from flask import Flask, redirect, url_for, request, render_template, session
import requests, os, uuid, json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('/index.html')


@app.route('/', methods=['POST'])
def index_post():
    # read form
    original_text = request.form['text']
    target_language = request.form['language']

    # load values from .env
    key = os.environ['KEY']
    endpoint = os.environ['ENDPOINT']
    location = os.environ['LOCATION']

    ## create URL
    # set translate mode & api version
    path = 'translate?api-version=3.0'
    # add target languager parameter
    target_language_parameter = '&to=' + target_language
    # full URL
    constructed_url = endpoint + path + target_language_parameter

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # create body for the body being translated
    body = [{ 'text': original_text }]

    # request using POST
    translator_request = requests.post(constructed_url, headers=headers, json=body)
    # retrieve JSON response
    translator_response = translator_request.json()
    # retrieve translation
    translated_text = translator_response[0]['translations'][0]['text']
    
    return render_template(
        'results.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )