from flask import Flask, jsonify
from flask import request,redirect,url_for
app = Flask(__name__)

data = {}


@app.route("/")
def hello():
    return "Hello Worlds!"

@app.route("/submit_audio", methods=['POST'])
def submit_audio():
    if request.method == 'POST':
        uuid_value = request.args['uuid']
        blob_value = request.args['blob']
        data['uuid'] = str(uuid_value)
        data['contextual'] = ['sup','yi']
        return redirect(url_for('get_audio'))
        #link_to_audio = request.files['file'].audio

@app.route("/audio", methods=['GET'])
def get_audio():
    return jsonify({'data': data})
