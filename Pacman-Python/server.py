import zmq
import sys
import pygame
from collections import namedtuple


context = zmq.Context()
socket = context.socket(zmq.ROUTER)
socket.bind('tcp://*:5000')
print("Started server")

poll = zmq.Poller()
poll.register(socket, zmq.POLLIN)
dictSocket = {}
listIdent = []
listMonedas = pygame.sprite.Group()
a = [[60, 45], [60, 585], [750, 45], [750, 585]]


while True:
    sockets = dict(poll.poll(0))
    if socket in sockets:
        if sockets[socket] == zmq.POLLIN:
            ident, *msg = socket.recv_multipart()
            
            if msg[0] == b"newPlayer":
                if not(ident in dictSocket):
                    dictSocket[ident] = a.pop(0)
                    listIdent.append(ident)
                # print(ident)
                print(listIdent)
                print(dictSocket)
                
            if msg[0] == b"newPosition":
                dictSocket[ident] = [msg[1].decode('ascii'), msg[2].decode('ascii')]
                print(dictSocket)
            
            if msg[0] == b"Jugadores":
                for iden in listIdent:
                    socket.send_multipart([iden, str(dictSocket).encode('ascii')])
                # print("Respuesta a cliente solicitando jugadores")
                # print("Envio lista jugadores")

            if msg[0] == b"actPosiciones":
                for iden in listIdent:
                    socket.send_multipart([iden, str(dictSocket).encode('ascii')])
            # for key in Socketdict:
            #     # print (key, ":", Socketdict[key])
            #     if ident == key:
            #         continue
            #     else:
            #         socket.send_multipart([key, msg])
    
                    
                