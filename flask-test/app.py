from flask import Flask, request, jsonify
import nltk
from nltk import tag
from nltk.stem.api import StemmerI
from nltk.stem.lancaster import LancasterStemmer


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'This is my first API call!'

@app.route('/post', methods=["POST"])
def testpost():
     input_json = request.get_json(force=True) 
     dictToReturn = {'text':input_json['text']}
     return jsonify(dictToReturn)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8082, debug=True)