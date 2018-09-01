import pygame
import sys
from pygame.locals import *

# VariablesGlobales
ancho = 1000
alto = 630

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

    def dibujarJugador(self, ventana):
        imagenRotada = pygame.transform.rotate(self.imagenJugador, self.angulo)
        ventana.blit(imagenRotada, self.rect)
        # print("Rect de jugador: " + str(self.rect))

    # def movimientoJugador(self, listaBloques):
    #     if self.vida == True:
    #         if self.rect.left <= 0:
    #             self.rect.left = 0
    #         elif self.rect.right >= ancho:
    #             self.rect.right = ancho
    #         elif self.rect.top <= 0:
    #             self.rect.top = 0
    #         elif self.rect.bottom >= alto:
    #             self.rect.bottom = alto
                    
class Bloque(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagenBloque = pygame.image.load("muro.png")
        self.rect = self.imagenBloque.get_rect()
        self.rect.centerx
        self.rect.centery

class Moneda(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagenMoneda = pygame.image.load("moneda.png")
        self.rect = self.imagenMoneda.get_rect()
        self.rect.centerx
        self.rect.centery

class Laberinto(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.anchoMatriz = 27
        self.altoMatriz = 21
        self.listaBloques = []
        self.listaMonedas = []
        self.matriz = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0],
                       [0,0,1,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,1,0,0],
                       [0,1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,0],
                       [0,0,1,0,1,1,1,0,1,0,1,0,0,0,0,0,1,0,1,0,1,1,1,0,1,0,0],
                       [0,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,0,1,0,0],
                       [0,1,1,1,1,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1,1,1,1,0],
                       [0,0,0,0,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,0,0,0,0],
                       [0,1,1,1,1,1,1,1,0,1,0,0,1,1,1,0,0,1,0,1,1,1,1,1,1,1,0],
                       [0,1,0,1,0,1,0,0,0,1,0,1,1,0,1,1,0,1,0,0,0,1,0,1,0,1,0],
                       [0,1,0,0,0,1,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1,0,0,0,1,0],
                       [0,1,0,1,0,1,0,0,0,1,0,1,1,0,1,1,0,1,0,0,0,1,0,1,0,1,0],
                       [0,1,1,1,1,1,1,1,0,1,0,0,1,1,1,0,0,1,0,1,1,1,1,1,1,1,0],
                       [0,0,0,0,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,0,0,0,0],
                       [0,1,1,1,1,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1,1,1,1,0],
                       [0,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,0,1,0,0],
                       [0,0,1,0,1,1,1,0,1,0,1,0,0,0,0,0,1,0,1,0,1,1,1,0,1,0,0],
                       [0,1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,0],
                       [0,0,1,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,1,0,0],
                       [0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

    def cargarLaberinto(self):
        for i in range(self.altoMatriz):
            for j in range(self.anchoMatriz):
                if self.matriz[i][j] == 0:
                    bloque = Bloque()
                    bloque.rect.centerx, bloque.rect.centery = j*30, i*30
                    self.listaBloques.append(bloque)
                elif self.matriz[i][j] == 1:
                    moneda = Moneda()
                    moneda.rect.centerx, moneda.rect.centery = j*30, i*30
                    self.listaMonedas.append(moneda)

    def dibujarLaberinto(self, ventana):
        for i in self.listaBloques:
            ventana.blit(i.imagenBloque, i.rect)
    
    def dibujarMonedas(self, ventana):
        for j in self.listaMonedas:
            ventana.blit(j.imagenMoneda, j.rect)

def main():
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
                elif pacman.mover == False:
                    if even.key == K_LEFT:
                        pacman.angulo = 180
                        print(pacman.velocidad)
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

                for bloque in escenario.listaBloques:
                    if pacman.rect.colliderect(bloque.rect):
                        pacman.mover = False


        ventana.blit(fondo, (0, 0))

        if len(escenario.listaMonedas) > 0:
            for moneda in escenario.listaMonedas:
                if pacman.rect.colliderect(moneda.rect):
                    escenario.listaMonedas.remove(moneda)
                    # print("Rect de moneda: " + str(moneda.rect))
           

        escenario.dibujarMonedas(ventana)
        escenario.dibujarLaberinto(ventana)
       
        pacman.dibujarJugador(ventana)
        
        pygame.display.update()

if __name__ == '__main__':
    main()
