#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 13:37:24 2022

@author: Maximilien Remillieux et Jean-Crhistophe Burnot
(code crestaurant voir chez Jean-christophe)
"""

import multiprocessing as mp
import random, time, sys

CLEARSCR="\x1B[2J\x1B[;H" 
CURSOFF  = "\x1B[?25l"
CL_RED="\033[22;31m"                    #  Rouge
CL_BLUE="\033[22;34m"                   #  Bleu   

# Définition de qq fonctions de gestion de l'écran
def effacer_ecran() : print(CLEARSCR,end='')
def erase_line_from_beg_to_curs() : print("\033[1K",end='')
def curseur_invisible() : print(CURSOFF,end='')
def move_too(lig, col) : print("\033[" + str(lig) + ";" + str(col) + "f",end='')  


class GameOfLive():
    
    def __init__(self):
        '''Cette fonction permet d'initialiser toute les paramètres'''
        self.t = []     #Tableau de cellule
        self.dim = 15       #dimension du tableau
        self.nb_cel = 30        #nombre de cellule initiale
        self.coord_cel = []         #coordonné des cellule initiale
        self.voisins = [[0 for i in range(self.dim)] for j in range (self.dim)]     #Tableu des cellules voisines initialisés à 0
        
        #Permet de générer les positions des premières cellules alèatoirement
        for i in range(self.nb_cel):
            coord = [random.randint(1, self.dim - 1),random.randint(1, self.dim - 1)]
            self.coord_cel.append(coord)
    
    def grille(self):
        '''Cette fonction permet de créé un tableu de cellule morte (à l'état False) '''
        
        ##Permet de remplir un tableu avec que des False losque l'ontravaille en sequentiel
        # self.t = [[False for i in range(self.dim)] for j in range (self.dim)]  
        
        #Permet de remplir un tableu avec que des False losque l'ontravaille en multiprocess  
        self.t = mp.Array('b',self.dim * self.dim)
        for i in range(self.dim) :
            for j in range(self.dim) :
                self.t[i * self.dim + j] = True
        jeu.place_cel()

    def place_cel(self):
        ''' Cette fonction permet de positionner aléatoirement des cellules vivantes (à l'état True)' dans le tebleau 'self.t'.'''
        
        ##Permet de placer des cellule vivante dans le tableau de cellule losque l'ontravaille en sequentiel
        # for k in self.coord_cel:
        #     l = k[0]
        #     c = k[1]
        #     self.t[l][c] = True

        #Permet de placer des cellule vivante dans le tableau de cellule losque l'ontravaille en multiprocess            
        lock.acquire()
        for i in range(self.dim):
            for j in range(self.dim):
                cel = random.randint(0,1)
                move_too(20, 1)
                if cel == 0 :
                    self.t[i * self.dim + j] = False
                else :
                    self.t[i * self.dim + j] = True
        jeu.affichage()
        lock.release()

    def Voisins(self):
        ''' Cette fonction à pour but de remplir un tableau 'self.voisin' en placent sur chaque lignes et chaques collones le nombre 
        de cellule en vie de chaques casse du tableau de cellule 'self.t' 
        '''
        
        #Permet de compter le nombre de voisin autour de chaque cellule losque l'ontravaille en multiprocess
        lock.acquire()
        for i in range(self.dim):
            for j in range(self.dim):
                delta=[(-1,0), (-1,+1), (0,+1), (+1,+1), (+1,0), (+1,-1), (0,-1), (-1,-1)]
                self.voisins[i][j] = 0
                for (dx,dy) in delta :
                    if self.dim >i+dx>=0 and self.dim >j+dy>=0  and self.t[i+dx * self.dim + j + dy] : # on est dedans
                        self.voisins[i][j] += 1

        
        ##Permet de compter le nombre de voisin autour de chaque cellule losque l'ontravaille en sequentiel
        # photo = self.t
        # self.voisins = [[0 for i in range(self.dim)] for j in range (self.dim)] 
        # for i,l in enumerate(photo): #ligne
        #     for j,c in enumerate(l): #colonne
        #         if i != 0 and j != 0:
        #             try:
        #                 if photo[i-1][j-1] == True:
        #                     self.voisins[i][j] += 1
        #             except IndexError:
        #                 pass
        #             try:
        #                 if photo[i-1][j] == True:
        #                     self.voisins[i][j] +=  1
        #             except IndexError:
        #                 pass
        #             try:
        #                 if photo[i-1][j+1] == True:
        #                     self.voisins[i][j] += 1
        #             except IndexError:
        #                 pass
        #             try:
        #                 if photo[i][j+1] == True:
        #                     self.voisins[i][j] += 1
        #             except IndexError:
        #                 pass
        #             try:
        #                 if photo[i+1][j+1] == True:
        #                     self.voisins[i][j] += 1
        #             except IndexError:
        #                 pass
        #             try:
        #                 if photo[i+1][j] == True:
        #                     self.voisins[i][j] += 1
        #             except IndexError:
        #                 pass
        #             try:
        #                 if photo[i+1][j-1] == True:
        #                     self.voisins[i][j] += 1
        #             except IndexError:
        #                 pass
        #             try:
        #                 if photo[i][j-1] == True:
        #                     self.voisins[i][j] += 1
        #             except IndexError:
        #                 pass           
        jeu.survivre(lock)
        lock.release()
        return self.voisins
    
    def survivre(self,lock):
        ''' Cette fonction permet d'appliquer les règles du jeu de la vie. Nous vérifions les conditions et changeons
        en conséquence l'état de notre cellule. 
        '''
        #Permet de tuer une cellule ou de la faire vivre losque l'ontravaille en multiprocess
        for i in range(self.dim):
            for j in range(self.dim):
                if self.t[i * self.dim + j] == False and self.voisins[i][j] > 2:
                    self.t[i * self.dim + j] = True
                elif self.t[i * self.dim + j] == True and self.voisins[i][j] < 2:
                    self.t[i * self.dim + j] = False
                elif self.t[i * self.dim + j] == True and self.voisins[i][j] > 3:
                    self.t[i * self.dim + j] = False
        
        ##Permet de tuer une cellule ou de la faire vivre losque l'ontravaille en sequentiel
        # for i,l in enumerate(self.t): #ligne
        #     for j,c in enumerate(l): #colonne            
        #         if self.t[i][j] == False and self.voisins[i][j] > 2:
        #             self.t[i][j] = True
        #         elif self.t[i][j] == True and self.voisins[i][j] < 2:
        #             self.t[i][j] = False
        #         elif self.t[i][j] == True and self.voisins[i][j] > 3:
        #             self.t[i][j] = False
        jeu.affichage()


    def affichage(self):
        ''' Cette fonction a pour objectif d'afficher la grille dans le terminal et de la modifier '''
        
        # Permet dafficher le tableau des cellules losque l'ontravaille en multiprocess
        effacer_ecran()
        print("Tableau Cellule")
        for i in range(self.dim):
            cel = ''
            for j in range(self.dim):
                if self.t[i * self.dim + j]:
                    cel = cel +  f"{CL_BLUE}O "
                else:
                    cel = cel + f"{CL_RED}X "
            move_too(i+2,1)
            erase_line_from_beg_to_curs()
            print(cel)
        
        ## Permet dafficher le tableau des cellules losque l'on travaille en sequentiel
        # effacer_ecran()
        # print("Tableau Cellule")
        # for i,l in enumerate(self.t): #ligne
        #     cel = ''
        #     for j,c in enumerate(l): #colonne
        #         if self.t[i][j]:
        #             cel = cel +  f"{CL_BLUE}O "
        #         else:
        #             cel = cel + f"{CL_RED}X "
        #     move_too(i+2,1)
        #     erase_line_from_beg_to_curs()
        #     print(cel)

        ## permetd'afficher le tableau des voisins         
        # colonne =1
        # ligne = 15
        # for i in self.voisins :
        #     move_too(ligne,colonne) 
        #     erase_line_from_beg_to_curs()
        #     print(i)
        #     ligne +=1 
 
'''Création de la grille de cellule '''
if __name__ == "__main__" :

    jeu = GameOfLive()
    
    ## Permet de lancer la simulation losque l'on travaille en multirocess
    lock = mp.Lock()
    tableau = jeu.grille()
    grille = mp.Process(target= jeu.grille, args= (tableau, lock))
    grille.start()
    grille.join()
    evolution = mp.Process(target= jeu.Voisins(), args= (tableau, lock))
    evolution.start()
    evolution.join()
    
    #Permet de lancer la simulation losque l'on travaille en msequentiel
    # jeu.grille()
    for i in range(100):
        jeu.Voisins()
        time.sleep(0.5)
