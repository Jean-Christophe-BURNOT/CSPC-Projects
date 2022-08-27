# -*- coding: utf-8 -*-
"""
@author: Jean-Christophe BURNOT, réalisé avec l'aide d'Axel François
Code qui simule le service d'un restaurant
"""
import time,random,random
import multiprocessing as mp

semTampon = mp.Semaphore(1)
semServeur = mp.Semaphore(1)
mutex = mp.Lock()

"""
clients: Fonction créatrice de commandes
"""
def clients(ptampon, pTamponSize):
    while True:
        with semTampon:
            index = dernierNonNul(ptampon[1])
            if index <= pTamponSize-1:
                lettreCommande = random.randint(1,26)
                numeroClient = random.randint(1,10)
                ptampon[0][index] = lettreCommande
                ptampon[1][index] = numeroClient
        time.sleep(1)

"""
serveur: Fonction qui traite les commandes
"""
def serveur(pNumero, ptampon, petatServeur, pService):
    while True:
        with semTampon:
            mutex.acquire()
            numeroClient = ptampon[1][0]
            lettreCommande = ptampon[0][0]
            if numeroClient != 0:
                #décale le tampon si il y a une commande
                ptampon[1] = fDecaleurListe(ptampon[1])
                ptampon[0] = fDecaleurListe(ptampon[0])
            mutex.release()
        if numeroClient == 0 :
            time.sleep(1)
        else:
            semServeur.acquire()
            petatServeur[0][pNumero] = lettreCommande
            petatServeur[1][pNumero] = numeroClient
            semServeur.release()
            time.sleep(random.randint(3,6))
            semServeur.acquire()
            petatServeur[0][pNumero] = 0
            petatServeur[1][pNumero] = 0
            pService[pNumero] = 1 
            semServeur.release()

"""
Patron: Fonction d'affichage
"""
def patron(pNombreProcServeur, ptampon,pServeur, pService):
    while True:
        semTampon.acquire()
        semServeur.acquire()
        mutex.acquire()
        ptamponLettre = fIntListToAlphabet(fArrayToList(ptampon[0]))
        ptamponNumero = fArrayToList(ptampon[1])
        pServeurLettre = fIntListToAlphabet(fArrayToList(pServeur[0]))
        pServeurNumero = fArrayToList(pServeur[1])
        pEnService = fArrayToList(pService)
        pService = fResetList(pService)
        mutex.release()
        semServeur.release()
        semTampon.release()
        print("\x1B[2J\x1B[;H",end='')
        for i in range(pNombreProcServeur):
            if pServeurNumero[i] == 0:
                print(f"Le serveur {i+1} traite la commande")
            else:
                print(f"Le serveur {i+1} traite la commande {(pServeurNumero[i],pServeurLettre[i])}")
        tailleListeCommande = dernierNonNul(ptamponNumero)
        ListeCommande = []
        for i in range(tailleListeCommande):
            ListeCommande.append((ptamponNumero[i],ptamponLettre[i]))
        print(f"Les commandes clients en attentes : {ListeCommande}")
        print(f"Nombre de commandes en attente : {tailleListeCommande}")
        for i,element in enumerate(pEnService):
            if element == 1:
                print(f"Le serveur {i+1} à fini sa préparation et l'a servi au client")
        time.sleep(1)

# %% Fonctions de gestion des listes

def dernierNonNul(pListe):
    valren = len(pListe)
    for i,element in enumerate(pListe):
        if element == 0:
            valren = i
            break
    return valren

def fArrayToList(pArray):
    valren = []
    for i,element in enumerate(pArray):
        valren.append(element)
    return valren

def fIntListToAlphabet(pListe):
    alphabet = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    valren = []
    for i,element in enumerate(pListe):
        valren.append(alphabet[element])
    return valren

def fIntToAlphabet(pEntier):
    alphabet = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return alphabet[pEntier]

def fDecaleurListe(pListe):
    for i in range(len(pListe)-1):
        pListe[i] = pListe[i+1]
    pListe[len(pListe)-1] = 0
    return pListe

def fResetList(pListe):
    for i in range(len(pListe)):
        pListe[i] = 0
    return pListe

NombreProcServeur = 4
EquipeServeur =  [0 for i in range(NombreProcServeur)]
TamponSize = 20

#Création des Arrays
tamponLettre = mp.Array('i',TamponSize)
tamponNumero = mp.Array('i',TamponSize)
ServeurLettre =  mp.Array('i',NombreProcServeur)
ServeurNumero =  mp.Array('i',NombreProcServeur)
EnService = mp.Array('i',NombreProcServeur)
#Création de matrices avec les arrays
tampon = [tamponLettre, tamponNumero]
etatServeur = [ServeurLettre, ServeurNumero]

#lancement des processus
PClient = mp.Process(target=clients, args= (tampon, TamponSize))
patron = mp.Process(target = patron, args= (NombreProcServeur, tampon, etatServeur, EnService))
#Crée les processus serveur utilisation des for car on a plusieurs serveurs
for i in range(NombreProcServeur):
    EquipeServeur[i] = mp.Process(target=serveur, args= (i, tampon, etatServeur, EnService))
PClient.start()
patron.start()
for i in range(NombreProcServeur):
    EquipeServeur[i].start()
PClient.join()
patron.join()
for i in range(NombreProcServeur):
    EquipeServeur[i].join()
