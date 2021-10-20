#!/usr/bin/env python

import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_ngrok import run_with_ngrok

import nltk
from nltk import tag
from nltk.stem.api import StemmerI
from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow
import json
import random
import pickle

#nltk.download('punkt')

with open("contenido.json",encoding='utf-8') as archivo:
    datos = json.load(archivo)

try:
    with open("variables.pickle","rb") as archivoPickle:
        palabras, tags,entrenamiento, salida = pickle.load(archivoPickle)
except:

    print (datos)


    palabras=[]
    tags=[]
    auxX=[]
    auxY=[]

    for contenido in datos ["contenido"]:
        for patrones in contenido["patrones"]:
            auxPalabra = nltk.word_tokenize(patrones)
            palabras.extend(auxPalabra)
            auxX.append(auxPalabra)
            auxY.append(contenido["tag"])

            if contenido["tag"] not in tags:
                tags.append(contenido["tag"])

    print("-------------------------")
    print(palabras)
    print("-------------------------")
    print(auxX)
    print("-------------------------")
    print(auxY)
    print("-------------------------")
    print(tags)            
    print("-------------------------")


    palabras = [stemmer.stem(w.lower()) for w in palabras if w!="?"]

    palabras = sorted(list(set(palabras)))

    tags= sorted(tags)

    entrenamiento = []
    salida=[]
    salidaVacia=[0 for _ in range(len(tags))]

    for x, documento in enumerate (auxX):
        cubeta =[]
        auxPalabra = [stemmer.stem(w.lower()) for w in documento]
        for w in palabras:
            if w in auxPalabra:
                cubeta.append(1)
            else:
                cubeta.append(0)
        filaSalida = salidaVacia[:]
        filaSalida[tags.index(auxY[x])]=1
        entrenamiento.append(cubeta)
        salida.append(filaSalida)

    print(entrenamiento)
    print("-------------------------")
    print(salida)    
    print("-------------------------")


    entrenamiento = numpy.array(entrenamiento)
    salida = numpy.array(salida)
    with open("variables.pickle","wb") as archivoPickle:
        pickle.dump((palabras,tags,entrenamiento,salida),archivoPickle)


#tensorflow.reset_default_graph()
tensorflow.compat.v1.reset_default_graph()

red = tflearn.input_data(shape=[None,len(entrenamiento[0])])
red= tflearn.fully_connected(red,10)
red = tflearn.fully_connected(red,10)
red = tflearn.fully_connected(red,len(salida[0]),activation="softmax")

red = tflearn.regression(red)

modelo = tflearn.DNN(red)

try:
    modelo.load("modelo.tflearn")
except:    
    modelo.fit(entrenamiento,salida,n_epoch=1000,batch_size=10,show_metric=True)
    modelo.save("modelo.tflearn")

print("-------------------------")


app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logging.getLogger('flask_cors').level = logging.DEBUG
CORS(app)
run_with_ngrok(app)


@app.route("/", methods=["GET"])
def index():
    return jsonify({'msg': 'success'})

@app.route('/post', methods=["POST"])
def testpost():
    input_json = request.get_json(force=True) 
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print(input_json)    
    entrada = input_json['text']
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print(entrada)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    cubeta = [0 for _ in range(len(palabras))]
    entradaProcesada = nltk.word_tokenize(entrada)
    entradaProcesada = [stemmer.stem(palabra.lower()) for palabra in entradaProcesada]
    for palabraIndividual in entradaProcesada:
        for i,palabra in enumerate(palabras):
            if palabra == palabraIndividual:
                cubeta[i] = 1

    resultados = modelo.predict([numpy.array(cubeta)])
    print(resultados)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ - los resultados estan arriba")
    resultadosIndices = numpy.argmax(resultados)
    tag = tags[resultadosIndices]

    for tagAux in datos["contenido"]:
        if tagAux["tag"] == tag:
            respuesta = tagAux["respuestas"]
            print(respuesta)
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ - Dentro del if linea 155")
    
    dictToReturn = {'text':random.choice(respuesta)+'rolando'}
    return jsonify(dictToReturn)

#if __name__ == '__main__':
#    app.run(host="0.0.0.0", port=32000, debug=True)     

if __name__ == '__main__':
    app.run()    