#!flask/bin/python
from flask import Flask, jsonify
from flask import request
from datetime import datetime
import os
import file_process

app = Flask(__name__)

valid_mimetypes = ['text/plain']
app.config['UPLOAD_FOLDER'] = 'tmp'
app.config['JSON_FOLDER'] = 'json'

#получение json файла по txt файлу
@app.route('/get_json_by_file', methods=['GET'])
def get_json_by_file():
    if request.method == 'GET':
            json_struct = file_process.request_to_json(request, valid_mimetypes, app.config['UPLOAD_FOLDER'])
            return json_struct

#получение json файла по id
@app.route('/get_json_by_id', methods=['GET'])
def get_json_by_id():
    if request.method == 'GET':
        if request.json and 'id' in request.json:      
            return file_process.id_to_json(request.json['id'], app.config['JSON_FOLDER'])
        else:
            return jsonify({'error': 'no id'}), 400


#получение id по txt файлу
@app.route('/send_file', methods=['POST'])
def get_id():
    if request.method == 'POST':
        json_struct = file_process.request_to_json(request, valid_mimetypes, app.config['UPLOAD_FOLDER'])[0]
        if not os.path.exists(app.config['JSON_FOLDER']):
            os.mkdir(app.config['JSON_FOLDER'])
        id = len(os.listdir(app.config['JSON_FOLDER']))
        json_path = os.path.join(app.config['JSON_FOLDER'], f'{id}.json')
        #сохраняем json
        with open(json_path, 'w') as f:
            f.write(json_struct)
        return jsonify({'id':id}), 201



if __name__ == '__main__':
    app.run(debug=True)