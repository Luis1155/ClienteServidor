import zmq
import sys
import pygame
from collections import namedtuple


context = zmq.Context()
socket = context.socket(zmq.ROUTER)
socket.bind('tcp://*:5000')
print("Servidor iniciado")

poll = zmq.Poller()
poll.register(socket, zmq.POLLIN)
dictSocket = {}
listIdent = []
listMonedas = pygame.sprite.Group()
a = [[60, 45], [60, 585], [750, 45], [750, 585], [405, 45], [405, 585]]


while True:
    sockets = dict(poll.poll(0))
    if socket in sockets:
        if sockets[socket] == zmq.POLLIN:
            ident, *msg = socket.recv_multipart()
            
            if msg[0] == b"newPlayer":
                if not(ident in dictSocket):
                    dictSocket[ident] = a.pop(0)
                    listIdent.append(ident)
                    if len(listIdent) != 0:
                        for iden in listIdent:
                            socket.send_multipart([iden, b"Players", str(dictSocket).encode('ascii')])
                # print(dictSocket[ident])

            if msg[0] == b"newPosition":
                dictSocket[ident] = [msg[1].decode('ascii'), msg[2].decode('ascii')]
                print(msg)
                for iden in listIdent:
                    if ident == iden:
                        continue
                    else:
                        print
                        socket.send_multipart([iden, b"Position", ident, msg[1], msg[2], msg[3]])
                  