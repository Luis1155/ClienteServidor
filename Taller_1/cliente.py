import zmq
import sys
import os
import math
import time


def main():
    if len(sys.argv) != 4:
        print("Error!!!")
        exit()
    ip = sys.argv[1] #Server's ip
    port = sys.argv[2] #Server's port
    operation = sys.argv[3] #Operation to Server

    context = zmq.Context()
    s = context.socket(zmq.REQ)
    s.connect("tcp://{}:{}".format(ip, port))

    if operation == "list":
        s.send_json({"op":"list"})
        files = s.recv_json()
        print(files)
    elif operation == "download":
        name = input("¿Que archivo quieres descargar?\n-> ")
        s.send_json({"op":"download", "file": name})
        size = s.recv()
        size = str(size,'utf-8')
        start = time.time()
        for parte in range(0, int(size)):
            s.send_json({"op":"descargaParte","file": name,"part":parte})
            file = s.recv()
            with open("{}".format(name), "ab") as output:
                output.write(file)

        end = time.time()
        tiempo = end - start
        print("El tiempo de descarga fue: {} seg".format(tiempo))
        

       
        '''else:
            print("\n")
            print("El numero de partes de tu archivo es: {}\n".format(size))'''

        
    else:
        print("Error!!! unsupported operation\n")

    print("Connecting to server {} at {}".format(ip, port))

if __name__ == '__main__':
    main()
