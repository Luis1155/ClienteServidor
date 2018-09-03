import pygame
import sys
import zmq
from pygame.locals import *

# VariablesGlobales
ancho = 1000
alto = 630
Green = (0, 255, 0)
dictJugadores = {}

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagenJugador = pygame.image.load("pacman.png")
        self.rect = self.imagenJugador.get_rect()

        self.rect.centerx = 30
        self.rect.centery = 30
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
        self.listaMonedas = pygame.sprite.Group()
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
                    bloque.rect.centerx, bloque.rect.centery = j*30, i*30
                    self.listaBloques.add(bloque)
                elif self.matriz[i][j] == 1:
                    moneda = Moneda()
                    moneda.rect.centerx, moneda.rect.centery = j*30, i*30
                    self.listaMonedas.add(moneda)

    def dibujarLaberinto(self, ventana):
        self.listaBloques.draw(ventana)
    
    def dibujarMonedas(self, ventana):
        self.listaMonedas.draw(ventana)

def crearJugadores(listIdent):
    for i in listIdent:
        if i in dictJugadores:
            continue
        else:    
            jugExterno = Jugador()
            dictJugadores[i] = jugExterno
    

def main():

    ######################Cliente
    context = zmq.Context()
    server = context.socket(zmq.DEALER)
    server.connect('tcp://localhost:5000')
    poll = zmq.Poller()
    poll.register(server, zmq.POLLIN)
    ######################Cliente
    server.send_multipart([b"newPlayer"])
    
    pygame.init()
    ventana = pygame.display.set_mode((ancho, alto), RESIZABLE)
    pygame.display.set_caption("PacmanDistribuido")
    fondo = pygame.image.load("fondo.png")
    pacman = Jugador()
    escenario = Laberinto()
    escenario.cargarLaberinto()
    enJuego = True
    reloj = pygame.time.Clock()

    while True:
        reloj.tick(60)
        # pacman.movimientoJugador(escenario.listaBloques)
        
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
        newPos = [b"newPosition", bytes(str(x), 'ascii'), bytes(str(y), 'ascii')]
        if (x != w) or (y != z):
            server.send_multipart(newPos)
                
        # server.send_multipart([b"Jugadores"])
        # listJuga = server.recv_multipart()
        # print(listJuga)
        # if(len(listJuga) != 0):
        #     crearJugadores(listJuga)

        ventana.blit(fondo, (0, 0))

        #Colision con monedas???
        pygame.sprite.spritecollide(pacman, escenario.listaMonedas, True)
           
        escenario.dibujarLaberinto(ventana)
        escenario.dibujarMonedas(ventana)
        
        for jug in dictJugadores:
            aux = dictJugadores[jug]
            aux.dibujarJugador(ventana)

        pacman.dibujarJugador(ventana)
        
        pygame.display.update()

if __name__ == '__main__':
    main()
