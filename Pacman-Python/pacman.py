import pygame
import sys
import zmq
import ast
from collections import namedtuple
from pygame.locals import *

# VariablesGlobales
ancho = 810
alto = 630
dictJugadores = {}
listaJugadores = pygame.sprite.Group()
listaMonedas = pygame.sprite.Group()

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagenJugador = pygame.image.load("pacman.png")
        
        self.rect = self.imagenJugador.get_rect()
        self.rect.centerx
        self.rect.centery
        self.vida = True
        self.velocidad = 15
        self.angulo = 0
        self.mover = True

    def getPosition(self):
        return (self.rect.centerx, self.rect.centery)

    def dibujarJugador(self, ventana):
        imagenRotada = pygame.transform.rotate(self.imagenJugador, self.angulo)
        ventana.blit(imagenRotada, self.rect)

class Bloque(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("muro.png")
        self.rect = self.image.get_rect()
        self.rect.centerx
        self.rect.centery

class Moneda(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("moneda.png")
        self.rect = self.image.get_rect()
        self.rect.centerx
        self.rect.centery

class Laberinto(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.anchoMatriz = 27
        self.altoMatriz = 21
        self.listaBloques = pygame.sprite.Group()
        # self.listaMonedas = pygame.sprite.Group()
        self.matriz = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0],
                       [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0],
                       [0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
                       [0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0],
                       [0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0],
                       [0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0],
                       [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
                       [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
                       [0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0],
                       [0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0],
                       [0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0],
                       [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
                       [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
                       [0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0],
                       [0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0],
                       [0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0],
                       [0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
                       [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0],
                       [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    def cargarLaberinto(self):
        for i in range(self.altoMatriz):
            for j in range(self.anchoMatriz):
                if self.matriz[i][j] == 0:
                    bloque = Bloque()
                    bloque.rect.x, bloque.rect.y = (j)*30, (i)*30
                    self.listaBloques.add(bloque)
                elif self.matriz[i][j] == 1:
                    moneda = Moneda()
                    moneda.rect.x, moneda.rect.y = 30*j+11, 30*i+11
                    listaMonedas.add(moneda)

    def dibujarLaberinto(self, ventana):
        self.listaBloques.draw(ventana)
    
    def dibujarMonedas(self, ventana):
        listaMonedas.draw(ventana)

def crearJugadores(dictJugs, identity):
    # print("DICTJUG {}".format(dictJugs))
    for i in dictJugs:
        if i in dictJugadores or i == identity:
            continue
        else:    
            jugExterno = Jugador()
            jugExterno.rect.centerx = int(dictJugs[i][0])
            jugExterno.rect.centery = int(dictJugs[i][1])
            listaJugadores.add(jugExterno)
            dictJugadores[i] = jugExterno
    # print(dictJugadores)

def main():

    Ini = True

    if len(sys.argv) != 2:
        print("Ingresar identidad")
        exit()
        
    identity = sys.argv[1].encode('ascii')

    ######################Cliente
    context = zmq.Context()
    server = context.socket(zmq.DEALER)
    server.identity = identity
    server.connect('tcp://localhost:5000')
    
    poller = zmq.Poller()
    poller.register(server, zmq.POLLIN)
    ######################Cliente
    
    pygame.init()
    ventana = pygame.display.set_mode((ancho, alto), RESIZABLE)
    pygame.display.set_caption("PacmanDistribuido")
    fondo = pygame.image.load("fondo.png")
    pacman = Jugador()
    escenario = Laberinto()
    escenario.cargarLaberinto()
    enJuego = True
    reloj = pygame.time.Clock()

    server.send_multipart([b"newPlayer"])

    while True:
        reloj.tick(60)
        
        if len(listaJugadores) < 1:
            enJuego = False
        else:
            enJuego = True

        w, z = pacman.getPosition()
        for even in pygame.event.get():
            if even.type == QUIT:
                pygame.quit()
                sys.exit()

            if enJuego == True:               
                if even.type == KEYDOWN and pacman.mover == True:
                    if even.key == K_LEFT:
                        pacman.angulo = 180
                        pacman.rect.left -= pacman.velocidad

                    elif even.key == K_RIGHT:
                        pacman.angulo = 0
                        pacman.rect.right += pacman.velocidad

                    elif even.key == K_UP:
                        pacman.angulo = 90
                        pacman.rect.top -= pacman.velocidad

                    elif even.key == K_DOWN:
                        pacman.angulo = 270
                        pacman.rect.top += pacman.velocidad
                elif even.type == KEYUP and pacman.mover == False:
                    if even.key == K_LEFT:
                        pacman.angulo = 180
                        pacman.rect.left += pacman.velocidad

                    elif even.key == K_RIGHT:
                        pacman.angulo = 0
                        pacman.rect.right -= pacman.velocidad

                    elif even.key == K_UP:
                        pacman.angulo = 90
                        pacman.rect.top += pacman.velocidad

                    elif even.key == K_DOWN:
                        pacman.angulo = 270
                        pacman.rect.top -= pacman.velocidad
                    pacman.mover = True

                #Colision con laberinto???
                listBlock = pygame.sprite.spritecollide(pacman, escenario.listaBloques, False)
                if listBlock:
                    pacman.mover = False

        x, y = pacman.getPosition()
        ang = pacman.angulo
        newPos = [b"newPosition", bytes(str(x), 'ascii'), bytes(str(y), 'ascii'), bytes(str(ang), 'ascii')]
        if (x != w) or (y != z):
            server.send_multipart(newPos)
            
        socks = dict(poller.poll(0))  
        if server in socks:
            mesServer = server.recv_multipart()
            if mesServer[0] == b"Players":
                diccionarioDecodificado = ast.literal_eval(mesServer[1].decode())
                if Ini == True:
                    posicion = diccionarioDecodificado[identity]    
                    print(posicion)
                    pacman.rect.centerx = int(posicion[0])
                    pacman.rect.centery = int(posicion[1])
                    Ini = False
                if(len(mesServer) != 0):
                    crearJugadores(diccionarioDecodificado, identity)
                    
            if mesServer[0] == b"Position":
                dictJugadores[mesServer[1]].angulo = int(mesServer[4].decode('ascii'))
                dictJugadores[mesServer[1]].rect.centerx = int(mesServer[2].decode('ascii'))
                dictJugadores[mesServer[1]].rect.centery = int(mesServer[3].decode('ascii'))

        ventana.blit(fondo, (0, 0))

        #Colision con monedas???
        pygame.sprite.spritecollide(pacman, listaMonedas, True)
        pygame.sprite.pygame.sprite.groupcollide(listaJugadores, listaMonedas, False, True)
           
        escenario.dibujarLaberinto(ventana)
        escenario.dibujarMonedas(ventana)
        
        for jug in dictJugadores:
            aux = dictJugadores[jug]
            aux.dibujarJugador(ventana)

        pacman.dibujarJugador(ventana)
        
        pygame.display.update()

if __name__ == '__main__':
    main()
