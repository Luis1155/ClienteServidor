import zmq
import sys
import os
import math


def loadFiles(path):
    files = {}
    dataDir = os.fsencode(path)
    for file in os.listdir(dataDir):
        filename = os.fsdecode(file)
        print("Loadding {}".format(filename))
        files[filename] = file
    return files

def getSize(filename):
    filename.seek(0,2)
    size = filename.tell()
    return size

def getParts(filename): #cuantas partes tiene el archivo
    size = getSize(filename)
    return int(math.ceil(size/(1024*1024)))

def bytesPart(filename, part): #Los bytes de una parte específica del archivo
    puntero = filename.seek(1024*1024*(part-1))
    descarga = filename.read(1024*1024)    
    return descarga


#comando op split(archivo y un tamaño )

def main():
    if len(sys.argv) != 3:
        print("Error!!!!")
        exit()

    directory = sys.argv[2]
    port = sys.argv [1]

    context = zmq.Context()
    s = context.socket(zmq.REP)
    s.bind("tcp://*:{}".format(port))

    files = loadFiles(directory)

    while True:
        msg = s.recv_json()
        if msg["op"] == "list":
            s.send_json({"files": list(files.keys())})
        elif msg["op"] == "download":
            filename = msg["file"]
            if filename in files:
                with open(directory + filename, "rb") as input:
                    size = getParts(input)
                    s.send_json(size)
        elif msg["op"] == "descargaParte":
            filename = msg["file"]
            filepart = msg["part"]
            if filename in files:
                with open(directory + filename, "rb") as input:
                    input.seek(1024*1024*filepart)
                    data = input.read(1024*1024)
                    s.send(data)



            else:
                print("\n")
                print(" << Cliente Conectado >>\n\n")
                print("Debido a que el archivo [{}] pedido por el cliente no existe se cerro la conexion con el cliente...\n".format(filename))
                print("El cliente cerro la conexion con el servidor...\n")
                print("<< Esperando conexion de un nuevo cliente >>\n\n")
                s.send_string("El archivo no existe")
        else:
            print("Unsupported activation!!")

if __name__ == '__main__':
    main()

#input.seek(1024+1024 * p)
#data = input.read(1024+1024)
#s.send(data)



def partes(file, parte):
    puntoReferencia = file.seek(1024*1024)
    #¿que parte quiere descagar?
    #6
    descarga = file.seek(1024*1024,(1024*1024*parte))

    return descarga

   























