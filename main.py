import os

import ffmpy
from flask import Flask, jsonify
from flask import request, redirect, url_for
from flask_cors import CORS

from processing.speech_parser import get_json_analysis_results,audio_duration

from pydub import AudioSegment

from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

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
        saveWEBM(uuid_value)
        convertToWAV(uuid_value)
        # Dan here is where your methods are going to be called
        # The WAV file is going to be called audio_wav.wav
        # Make sure that all of your methods are done within one overarching methods
        # Make sure that all of your calculations are also added to the json object called data
        # you can do this by doing the following:
        #       data['key'] = value
        data['analysis'] = processedData(uuid_value)
        # endProcesses()
        return redirect(url_for('get_audio'))
        # link_to_audio = request.files['file'].audio


@app.route("/audio", methods=['GET'])
def get_audio():
    return jsonify({'data': data})


def saveWEBM(uuid):
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
    name = 'processing/'+str(uuid)+'_webm.webm'
    with open(name, "w") as webm:
        webm.write(webm_decoded)

def convertToWAV(uuid):
    nameOLD = 'processing/'+str(uuid)+'_webm.webm'
    nameNew = 'processing/'+str(uuid)+'_wav.wav'
    ff = ffmpy.FFmpeg(inputs={nameOLD: None}, outputs={nameNew: None})
    ff.run()

def endProcesses(uuid):
    nameOLD = 'processing/'+str(uuid)+'_webm.webm'
    nameNew = 'processing/'+str(uuid)+'_wav.wav'
    os.remove(nameNew)
    os.remove(nameOLD)

def processedData(uuid):
    fileNames = []
    nameNew = 'processing/'+str(uuid)+'_wav.wav'
    for i in range(0,int(audio_duration(nameNew)),15):
        t1 = i * 1000;
        t2 = (i + 5) * 1000;
        newAudio = AudioSegment.from_wav(nameNew)
        try:
            newAudio = newAudio[t1:t2]
        except:
            print('it actually failed probably at i=' + str(i))
            newAudio = newAudio[t1:audio_duration(nameNew)]
        fileName = str(uuid)+'_'+str(t1)+'_'+str(t2)+'_wav.wav'
        saveAs = 'processing/'+fileName
        fileNames.append(fileName)
        print(fileName)
        newAudio.export(saveAs, format="wav")
        print(fileName)
    print(fileNames)
    pool = ThreadPool()
    results = pool.map(get_json_analysis_results,fileNames)
    print(results)
    return results
