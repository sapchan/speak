from flask import Flask, jsonify
from flask import request,redirect,url_for
from flask_cors import CORS

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
        #audio = request.files['file']
        data['uuid'] = str(uuid_value)
        #data['file_name'] = str(audio.filename)
        return redirect(url_for('get_audio'))
        #link_to_audio = request.files['file'].audio

@app.route("/audio", methods=['GET'])
def get_audio():
    return jsonify({'data': data})
