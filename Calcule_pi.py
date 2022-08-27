#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 30 13:44:09 2022

@author: Maximilien Remillieux et Jean-christophe Burnot
(code couresc Hippique voir chez Jean-christophe)
"""

import random, time, sys
import multiprocessing as mp
# calculer le nombres de hits dans un cercle unitaire (utilisé par les différentes méthodes)

def frequence_de_hits_pour_n_essais(s,nb_iteration,nb_hits):
    '''cette fonction sert à placée des points dans le carré unitaire de coordonnée [0,Ø] [1,1]  et de compter le nombre de point qui ont attéri
    dans le premier quart de cecle du cercle unité
    '''
    count = 0
    for i in range(nb_iteration):
        x = random.random() 
        y = random.random()
# si le point est dans l’unit circle
        if x * x + y * y <= 1: 
            count += 1
    s.acquire()
    nb_hits.value += count
    s.release()
    return 


if __name__ == "__main__":
    # Nombre d’essai pour l’estimation
    nb_total_iteration = 10000000
    # Innitialisation du nombre de hits, variable partager par les process
    nb_hits = mp.Value('f', 0.0)
    # Nombre de processeur
    nb_pros = 8
    #Permet de compter le temps de calcule
    debut = time.time()
    #cr&ation d'un semaphore
    sem = mp.Semaphore(1)
    #initialisation de la liste partager
    list_pros = []
    #création des process et appele de la fonction frequence_de_hits_pour_n_essais
    for i in range(nb_pros):
        pros = mp.Process(target = frequence_de_hits_pour_n_essais, args = (sem, nb_total_iteration // nb_pros, nb_hits,))
        list_pros.append(pros)
        pros.start()
    for p in list_pros:
        p.join()
    fin = time.time()
  
    #calcule de pi avec 8 process
    print("Valeur estimée Pi par la méthode Mono−Processus et 8 Processus : ", "valeur estimer de Pi =",4 * nb_hits.value / nb_total_iteration,
          "temps avec 8 procesus:", fin - debut)

    #calcule de pi avec 1 process
    debut = time.time()
    frequence_de_hits_pour_n_essais(sem, nb_total_iteration, nb_hits)
    fin = time.time()
    print( "temps avec 1 processus:", fin - debut)
    sys.exit()

