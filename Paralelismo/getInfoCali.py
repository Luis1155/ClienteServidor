import sys
import os

def main():
	diccionario={}

	archivo=open("USA-road-distance.NY.gr")

	lineas=archivo.readlines()
	for linea in lineas:
		datos=linea.split(" ")
		nOrigen=int(datos[1])
		nDestino=int(datos[2])
		costo=int(datos[3])

		if(not(nOrigen in diccionario)):
			diccionario[nOrigen] = {}
			diccionario[nOrigen][nDestino] = costo
		else:
			diccionario[nOrigen][nDestino] = costo

	for key in diccionario:
		asi = sorted(diccionario[key].items(), key = lambda t: t[0])
		diccionario[key] = asi
	
	dicc = sorted(diccionario.items(), key = lambda t: t[0])	

	resultado=open("roadNY.txt","w")
	for item in dicc:
		resultado.write(str(item[0]))
		resultado.write(" "+str(item[1]))
		resultado.write("\n")
	resultado.close()
	
	# print(diccionario)

if __name__ == '__main__':
	main()
