from ast import arg
import tkinter as tk
import random as random
import multiprocessing as mp
import time
import os

#définition des variables

def robot(master):
    canvas = tk.Canvas(master,width=500,height=500)
    canvas.pack()
    taille_robot = 25
    x0,y0 = 250,500-taille_robot
    robot = canvas.create_oval(x0,y0,x0+taille_robot,y0+taille_robot,fill='black')
    vitesse = {'x':2, 'y':0}
    nombre_rectangle = 10
    taille_rectangle = 25
    listeObstacle=[]
    for i in range(nombre_rectangle):
        x0r,y0r = random.randint(1,500),random.randint(1,500)
        obstacle = canvas.create_rectangle(x0r,y0r,x0r+taille_rectangle,y0r+taille_rectangle,fill='red')
        listeObstacle.append(obstacle)
        print(listeObstacle)
    capt_bumper = mp.Process(target=bumper,args=(canvas,vitesse,robot,listeObstacle))
    capt_bumper.start()
    capt_bumper.join()
    canvas.after(50,deplacement,canvas,vitesse,robot)
    return canvas
    
def deplacement(canvas,vitesse,robot):
    coords = canvas.coords(robot)
    coords[1] -= vitesse['x']
    coords[3] -= vitesse['x']
    canvas.coords(robot, coords[0], coords[1], coords[2], coords[3])
    canvas.after(50, deplacement, canvas, vitesse,robot)

"""
bumper: fonction qui se répète toute les n sesondes. En cas de contact avec l'avant le robot recule
entrées: canvas, vitesse, robot
sorties:
"""
def bumper(canvas,vitesse,robot,listeObstacle):
    for i in listeObstacle:
        coords=canvas.coords(i)
        print(canvas.coords(robot))
        if canvas.coords(robot)[0] == coords[0]:
            vitesse["y"]*(-1)
    canvas.after(50, bumper)


      
# %% lancement de l'interface graphique    
screen = tk.Tk()
screen.title('Irobot')
Frame = robot(screen)
screen.mainloop()
while True:
    os.fork()
