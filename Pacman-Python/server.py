import zmq
import sys
from collections import namedtuple


context = zmq.Context()
socket = context.socket(zmq.ROUTER)
socket.bind('tcp://*:5000')
print("Started server")

poll = zmq.Poller()
poll.register(socket, zmq.POLLIN)
dictSocket = {}
listIdent = []

while True:
    sockets = dict(poll.poll())
    if socket in sockets:
        if sockets[socket] == zmq.POLLIN:
            ident, *msg = socket.recv_multipart()
            
            if msg[0] == b"newPlayer":
                dictSocket[ident] = []
                listIdent.append(ident)
                print(ident)
                print(listIdent)
                
            if msg[0] == b"newPosition":
                dictSocket[ident] = [msg[1].decode('ascii'), msg[2].decode('ascii')]
                print(dictSocket)
            
            if msg[0] == b"Jugadores":
                socket.send_multipart(listIdent)
                # print("Envio lista jugadores")

            # for key in Socketdict:
            #     # print (key, ":", Socketdict[key])
            #     if ident == key:
            #         continue
            #     else:
            #         socket.send_multipart([key, msg])
                    
                