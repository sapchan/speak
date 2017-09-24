import os

import ffmpy
from flask import Flask, jsonify
from flask import request, redirect, url_for
from flask_cors import CORS

from processing.speech_parser import get_json_analysis_results

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})

data = {}

test = {}


@app.route("/")
def hello():
    test['id'] = 'Hello World'
    return jsonify({'test': test})


@app.route("/submit_audio", methods=['POST'])
def submit_audio():
    if request.method == 'POST':
        json = request.get_json()
        uuid_value = json.get('uuid')
        audio = json.get('file')
        data['uuid'] = str(uuid_value)
        data['file'] = str(audio)
        saveWEBM()
        convertToWAV()
        # Dan here is where your methods are going to be called
        # The WAV file is going to be called audio_wav.wav
        # Make sure that all of your methods are done within one overarching methods
        # Make sure that all of your calculations are also added to the json object called data
        # you can do this by doing the following:
        #       data['key'] = value
        data['analysis'] = get_json_analysis_results()
        endProcesses()
        return redirect(url_for('get_audio'))
        # link_to_audio = request.files['file'].audio


@app.route("/audio", methods=['GET'])
def get_audio():
    return jsonify({'data': data})


def saveWEBM():
    # the file comes in base64 format into data
    # decoding the base64 gives you the arrayBuffer values in a webm file
    # the ffmpeg library can help transform the webm file to a wav file
    # the webm file can be deleted past this point
    # steps:
    # decode base64, write to file with extension webm
    # use ffmpeg to convert webm to wav
    # pass it to dan
    encoded_webm = str(data['file'])
    webm_decoded = encoded_webm.decode('base64')
    with open("audio_webm.webm", "w") as webm:
        webm.write(webm_decoded)


def convertToWAV():
    ff = ffmpy.FFmpeg(inputs={'audio_webm.webm': None}, outputs={'audio_wav.wav': None})
    ff.run()


def endProcesses():
    os.remove('audio_wav.wav')
    os.remove('audio_webm.webm')
