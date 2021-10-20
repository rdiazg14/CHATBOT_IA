# importar la funcion de busqueda
from googlesearch import search
# la consulta de busqueda la vamos a obtener de la entrada por teclado
q = input("Ingrese su busqueda: ")

tld = "com" 
lang = "en" 
num=100  
start=0 
stop=num 
pause=2.0 
# ahora ejecutamos la busqueda con la funcion search y pasamos como parametro la consulta
# asignamos cada parametro de variable local con los parametros correspondiente de la funcion search
results = search(q, tld=tld, lang=lang, num=num, start=start, stop=stop, pause=pause)
# hacemos un recorrido de los resultados, cada resultado es una URL
for r in results:
	print(r) # la variable "r" contiene la url resultado