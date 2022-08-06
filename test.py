

#--------------------------------------------------------------------------
#------- Importamos los paquetes necesarios -------------------------------
#--------------------------------------------------------------------------

import cv2
import numpy as np
import pygame
import tkinter as tk
import sys
from functools import partial

#--------------------------------------------------------------------------
#-------- Iniciacion de colores y variables -------------------------------
#--------------------------------------------------------------------------

BLACK  = (   0,   0,   0)
WHITE  = ( 255, 255, 255)
BLUE   = (   0,   0, 255)
GREEN  = (   0, 255,   0)
GREENL  = (181, 230,  29)
RED    = ( 255,   0,   0)
PURPLE = ( 255,   0, 255)

#Seting up the coordinates and constants
x = 0
y = 0
run = True

lower_red = np.array ([110, 50, 50],np.uint8) # Color minimo del rango
higher_red = np.array([130,255, 255],np.uint8) # Color maximo del rango

#--------------------------------------------------------------------------
#-------- Clase para crear muros del juego ------------------------------
#--------------------------------------------------------------------------

class Wall(pygame.sprite.Sprite):
    """This class represents the bar at the bottom that the player controls """

    def __init__(self, x, y, width, height, color):
        """ Constructor function """

        # Llamada del constructor
        super().__init__()

        # Dibujar el muro
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Hacerle la ubicacion a los muros.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

#--------------------------------------------------------------------------
#-------- Clase para crear el personaje ---------------------------------
#--------------------------------------------------------------------------

class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player controls """

    # Verifica cambios de posicion.
    change_x = 0
    change_y = 0

    def __init__(self, x, y):
        """ Constructor function """

        # Llamada al constructor
        super().__init__()

        # Tamaño y color del personaje
        self.image = pygame.Surface([15, 15])
        self.image.fill(RED)

        # Asignamos la posicion inicial
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

    # Funcion que verifica cada movimiento si hubo un choque y resta vidas.
    def move(self, walls,vidas):
        """ Find a new position for the player """


        # Verifica choques de izquierda a derecha
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:

            if self.change_x > 0:
                self.rect.right = block.rect.left
                vidas -= 1
            else:
                self.rect.left = block.rect.right
                vidas -= 1


        # Verifica choques de arriba a abajo
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:

            if self.change_y > 0:
                self.rect.bottom = block.rect.top
                vidas -= 1
            else:
                self.rect.top = block.rect.bottom
                vidas -= 1
        return vidas

#--------------------------------------------------------------------------
#-------- Clase para crear los niveles ------------------------------------
#--------------------------------------------------------------------------

class Room(object):
    """ Base class for all rooms. """

    """ Each room has a list of walls, and of enemy sprites. """
    wall_list = None
    enemy_sprites = None

    def __init__(self):
        """ Constructor, create our lists. """
        self.wall_list = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

#--------------------------------------------------------------------------
#-------- Clase con caracteristicas nivel 1, 2 y 3-------------------------
#--------------------------------------------------------------------------

class Room1(Room):
    """This creates all the walls in room 1"""
    def __init__(self):
        Room.__init__(self)

        # Esta es una lista de los muros lo cual recibe [x, y, width, height, color]
        walls = [[30, 30, 20, 170, WHITE],
                 [30, 280, 20, 170, WHITE],
                 [590, 30, 20, 170, WHITE],
                 [590, 280, 20, 170, WHITE],
                 [50, 30, 540, 20, WHITE],
                 [50, 430, 540, 20, WHITE],
                 [310, 90, 20, 290, BLUE]
                ]

        # crea el conjunto de muros
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

class Room2(Room):
    """This creates all the walls in room 2"""
    def __init__(self):
        Room.__init__(self)

        walls = [[30, 30, 20, 170, RED],
                 [30, 280, 20, 170, RED],
                 [590, 30, 20, 170, RED],
                 [590, 280, 20, 170, RED],
                 [50, 30, 540, 20, RED],
                 [50, 430, 540, 20, RED],
                 [200, 90, 20, 290, GREEN],
                 [420, 90, 20, 290, GREEN]
                ]

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)


class Room3(Room):
    """This creates all the walls in room 3"""
    def __init__(self):
        Room.__init__(self)

        walls = [[30, 30, 20, 170, PURPLE],
                 [30, 280, 20, 170, PURPLE],
                 [590, 30, 20, 170, PURPLE],
                 [590, 280, 20, 170, PURPLE],
                 [50, 30, 540, 20, PURPLE],
                 [50, 430, 540, 20, PURPLE],
                ]

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

        for x in range(100, 500, 180):
            for y in range(80, 480, 200):
                wall = Wall(x, y, 20, 120, RED)
                self.wall_list.add(wall)

        for x in range(170, 600, 180):
            wall = Wall(x, 180, 20, 150, WHITE)
            self.wall_list.add(wall)

#--------------------------------------------------------------------------
#-------- Funcion que captura el color de la camara -----------------------
#--------------------------------------------------------------------------

def color_capture(cap, higher_color, lower_color, x,y):
    ret, frame = cap.read() 
    if ret==True:
        # We use the the HSV (Hue, Saturation, Value) format because is used to separate image luminance 
        # from color information. This makes it easier when we are working on or need luminance of the image/frame.
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #Converting from RGB to HSV
        mask = cv2.inRange(frame_hsv, lower_color, higher_color) #Creating the mask with the range of colors on the frame
        #Descomente la siguiente linea en caso de que use portatil y comente la siguiente.
        #_,contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Catching the red/blue contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Catching the red/blue contours 
        for c in contours: # Mapping all the found contours
            area = cv2.contourArea(c) #Catching the contour area
            if area > 3000:
                M = cv2.moments(c)
                if (M["m00"] == 0): M["m00"]=1
                x = int(M["m10"]/M["m00"]) #Getting the x coordinate
                y = int((M["m01"] / M["m00"])) 
                cv2.circle(frame, (x,y), 7, (0,255,0), -1) 
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, '{},{}'.format(x,y),(x+10,y), font, 0.75,(0,255,0),1,cv2.LINE_AA)
                nuevoContorno = cv2.convexHull(c)
                cv2.drawContours(frame, [nuevoContorno], 0, (255,0,0), 3) #Drawing the found contours
        res = cv2.bitwise_and(frame,frame, mask= mask)
        cv2.imshow('frame',frame) # Displaying the frame with the contours and the coordinates
        #cv2.imshow('mask',mask)
        #cv2.imshow('res',res)
    return x, y


#--------------------------------------------------------------------------
#-------- Funciones que generan mensajes de la app ------------------------
#------------- respectivas funciones de salida ....------------------------
#--------------------------------------------------------------------------

def mensaje(color, vidas, mensaje):
    ventana=tk.Tk()
    ventana.title("MAZE EXPLORER")
    #AnchoAlto
    ventana.geometry('280x300')
    ventana.configure(background='white smoke')

    etiqueta1=tk.Label(ventana,text="Resultado del juego:",bg="dark green",fg="white")
    etiqueta1.pack(padx=10,pady=10,side=tk.TOP,fill=tk.X,ipadx=5,ipady=10)

    etiqueta2=tk.Label(ventana,text=mensaje,bg=color,fg="black")
    etiqueta2.pack(padx=10,pady=5,ipadx=30,ipady=30,side=tk.TOP,fill=tk.X)

    etiqueta3=tk.Label(ventana,text="Vidas: "+str(vidas),bg="gold",fg="black")
    etiqueta3.pack(ipadx=20,ipady=5, fill=tk.X, padx=50)

    tk.Button(ventana, text="Salir", bg = "dim gray", fg = "white", command=partial(salir,ventana)).pack(ipadx=20,ipady=5, fill=tk.X, padx=100,pady=20)

    ventana.mainloop()

def bienvenidos():
    ventana2=tk.Tk()
    ventana2.title("MAZE EXPLORER")
    ventana2.geometry('300x400')
    ventana2.configure(background='white smoke')

    etiqueta1=tk.Label(ventana2,text="Bienvenido a MAZE EXPLORER\n Aventurate en el mejor juego de PDI\n\n Recuerda un objeto azul debes utilizar",bg="dark green",fg="white")
    etiqueta1.pack(padx=10,pady=10,side=tk.TOP,fill=tk.X,ipadx=5,ipady=10)


    tk.Button(ventana2, text="Ingresar", bg = "dim gray", fg = "white", command=partial(salir2,ventana2)).pack(ipadx=20,ipady=5, fill=tk.X, padx=100,pady=20)

    ventana2.mainloop()

def show_webcam(mirror=False):
    cap = cv2.VideoCapture(0)
     # inicializar el juego con la libreria pygame
    pygame.init()
    # Crear una 640x480 tamaño de pantalla
    screen = pygame.display.set_mode([640, 480])
    while True:
        ret_val, img = cap.read()
        #img = pygame.image.load(cap.read())
        if mirror: 
            #img = cv2.flip(img, 1)
            img = pygame.transform.flip(img, False, True)
        cv2.imshow('my webcam', img)
        game(cap,screen, img)
        if cv2.waitKey(1) == 27: 
            break  # esc to quit
    #Cierra el juego y sus ventanas.
    pygame.quit()
    cap.release()
    cv2.destroyAllWindows()

def game(cap, screen, img):
    screen.blit(img, (50 + 1 * 120, 100))

    # titulo de la ventana
    pygame.display.set_caption('MAZE EXPLORER')

    # Creacion y llamada del jugador
    player = Player(60, 233)
    movingsprites = pygame.sprite.Group()
    movingsprites.add(player)

    # posicion de la grafica
    background_position = [0, 0]

    #Cantidad de vidas
    vidas = 3

    # Cargar imagenes
    background_image1 = pygame.image.load("Ground_1.png").convert()
    background_image2 = pygame.image.load("Ground_2.png").convert()
    background_image3 = pygame.image.load("Ground_3.png").convert()

    #Texto para vidas
    font = pygame.font.SysFont("monospace", 24) 
    text = font.render("Vidas: "+ str(vidas), True, (0, 255, 0))

    #--------------------------------------------------------------------------
    #------- Correr el juego --------------------------------------------------
    #--------------------------------------------------------------------------

    while run:
        """ Main Program """
        #Arranca el juego.
        rooms = []

        room = Room1()
        rooms.append(room)

        room = Room2()
        rooms.append(room)

        room = Room3()
        rooms.append(room)

        current_room_no = 0
        current_room = rooms[current_room_no]

        clock = pygame.time.Clock()

        done = False
        play = False

        while not done:
            
            # Lee la posicion del color a mostrar
            red_validation_x, red_validation_y = color_capture(cap, higher_red, lower_red, 0,0) # Detecting the red object

            #Da inicio de arranque en cada nivel (Mi objeto debe estar en esas posiciones para iniciar)
            if(red_validation_x>55 and red_validation_x<85 and red_validation_y>80 and red_validation_y<280): play = True

            if(play):
                player.rect.x = red_validation_x
                player.rect.y = red_validation_y

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True


            # Logica del juego, verifica las vidas
            copy = vidas
            vidas = player.move(current_room.wall_list,vidas)
            if(vidas < copy):
                player.rect.x = 65
                player.rect.y = 233
                play = False
                if(vidas == 0):
                    mensaje("firebrick4",vidas,"Perdiste :(")
            text = font.render("Vidas: "+ str(vidas), True, (0, 255, 0))

            #Si la persona intenta devolverse.
            if player.rect.x < 45:
                vidas -= 1;
                if(vidas == 0):
                    mensaje("firebrick4",vidas,"Perdiste :(")
                player.rect.x = 65
                player.rect.y = 233
                play = False
                text = font.render("Vidas: "+ str(vidas), True, (0, 150, 0))

            #Verificar si pasara de nivel
            if player.rect.x > 600:
                if current_room_no == 0:
                    current_room_no = 1
                    current_room = rooms[current_room_no]
                    player.rect.x = 65
                    player.rect.y = 233
                    play = False
                elif current_room_no == 1:
                    current_room_no = 2
                    current_room = rooms[current_room_no]
                    player.rect.x = 65
                    player.rect.y = 233
                    play = False
                else:
                    mensaje("chartreuse3",vidas,"¡Ganaste!")
                    current_room_no = 0
                    current_room = rooms[current_room_no]
                    player.rect.x = 65
                    player.rect.y = 233
                    play = False

            # Dibuja la pantalla dependiendo del nivel
            if(current_room_no == 0):
                screen.blit(background_image1, background_position)
            elif(current_room_no == 1):
                screen.blit(background_image2, background_position)
            elif(current_room_no == 2):
                screen.blit(background_image3, background_position)

            # Dibuja posicion inicial y final.
            pygame.draw.rect(screen, GREENL, pygame.Rect(55, 200, 30, 80))
            pygame.draw.rect(screen, GREENL, pygame.Rect(555, 200, 30, 80))

            movingsprites.draw(screen)
            current_room.wall_list.draw(screen)

            screen.blit(text, (230, 28))

            pygame.display.flip()

            clock.tick(60)
        break

    
def salir(ventana):
    ventana.destroy()
    pygame.quit()
    cap.release()
    cv2.destroyAllWindows()

def salir2(ventana2):
    ventana2.destroy()



#--------------------------------------------------------------------------
#------- Inicio del juego, aqui iniciamos las pantallas, titulos ----------
#------- y tamaños para el funcionamiento del videojuego ------------------
#--------------------------------------------------------------------------

bienvenidos()
# Inicializar camara
show_webcam(mirror=True)
