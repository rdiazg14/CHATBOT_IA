#!/usr/bin/env python


import logging
from flask import Flask, jsonify
from flask_cors import CORS
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logging.getLogger('flask_cors').level = logging.DEBUG
CORS(app)
run_with_ngrok(app)


@app.route("/return_json", methods=["POST"])
def returnJson():
    return jsonify({
        'folder_id': 'yoyo',
        'img': 'adad',
        'imgname': 'bibi',
        'imguniquename': 'kaka'
    })


@app.route("/", methods=["GET"])
def index():
    return jsonify({'msg': 'success'})


if __name__ == '__main__':
    app.run()