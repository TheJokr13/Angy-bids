### travaux pratiques Gtech Méca

import matplotlib.pyplot as plt
import numpy as np

### CONSTANTES
m = 0.8 # masse de l'oiseau (kg)
g = 9.81 # constante gravitationnelle (m/s²)
k = 10 # constante de raideur du ressort (N/m)
f2 = 0.2 / m #coeff de frottement divisé par la masse

### FONCTIONS
## Etape 1.1 : Calcul de la vitesse d'ejection v0
def vitesse_initiale(alpha, l1):
    v_eject = l1*np.sqrt(k/m)*np.sqrt(1-(m*g*np.sin(alpha)/(k*l1))**2)
    return v_eject

## Etape 2.1 : trajectoire d'un oiseau lancé avec angle alpha et longueur l1 
def lancer_oiseau(alpha, l1):
    v0 = vitesse_initiale(alpha, l1) #vitesse initiale de l'oiseau
    t_max = 2*v0*np.sin(alpha)/g #temps d'impact avec le sol
    liste_t = np.linspace(0, t_max, 100) #génère une liste de 100 valeurs de temps entre 0 et t_max
    x = v0*np.cos(alpha)*liste_t #position horizontale de l'oiseau en fonction du temps
    y = v0*np.sin(alpha)*liste_t - 0.5*g*liste_t**2 #position verticale de l'oiseau en fonction du temps
    return x, y

## Etape 2.2 : affichage de la trajectoire d'un oiseau  
def afficher_oiseau(alpha, l1, lancer_fonction):
    x, y = lancer_fonction(alpha, l1)
    plt.plot(x, y, label="Trajectoire de l'oiseau")
    plt.axis('equal')
    plt.tight_layout()
    plt.legend()
    plt.show()
    
## Etape 3.1 : affichage des trajectoires pour plusieurs angles    
def afficher_oiseaux_multiples(l1):
    alpha_max = np.pi/2
    for alpha in np.linspace(0, alpha_max, 11):
            x, y = lancer_oiseau(alpha, l1)
            plt.plot(x, y,)
    plt.axis('equal')
    plt.tight_layout()  
    plt.show()

## Etape 4.1 : trajectoire d'un oiseau avec frottement de l'air
def lancer_oiseau_frottement(alpha, l1):
    v0 = vitesse_initiale(alpha, l1)
    t_max = 2*v0*np.sin(alpha)/g 
    lambda_x = v0*np.cos(alpha) 
    lambda_y = v0*np.sin(alpha)+g/f2
    liste_t = np.linspace(0, t_max, 100)
    x = (lambda_x/f2)*(1 - np.exp(-f2*liste_t))
    y = (lambda_y/f2)*(1-np.exp(-f2*liste_t)) - g/f2*liste_t
    return x, y

## Etape 4.2 : affichage de la trajectoire avec et sans frottement
def afficher_oiseau_frottement(alpha, l1, lancer_fonction, lancer_fonction_frottement):
    x, y = lancer_fonction_frottement(alpha, l1)
    plt.plot(x, y,'b', label="avec frottement")
    x, y = lancer_fonction(alpha, l1)
    plt.plot(x, y,'r', label="sans frottement")
    plt.axis('equal')
    plt.legend()
    plt.tight_layout()
    plt.show()

## Etape 5.1 : trajectoire d'un oiseau - récurrence 
def lancer_oiseau_recurrence(alpha, l1):
    v0 = vitesse_initiale(alpha, l1)
    dt = 0.01  # Pas de temps (plus petit = plus précis)
    x, y = 0, 0 # Position initiale
    liste_x = [0] # Liste des positions horizontales
    liste_y = [0] # Liste des positions verticales
    vx = v0*np.cos(alpha) # Vitesse initiale - coordonnée x
    vy = v0*np.sin(alpha) # Vitesse initiale - coordonnée y
    while liste_y[-1] >= 0:  # Tant que l'oiseau n'a pas touché le sol
        x = x + vx*dt # Mise à jour de la position horizontale
        y = y + vy*dt # Mise à jour de la position verticale
        liste_x.append(x) #stockage des positions
        liste_y.append(y)
        vy += -g*dt
    return liste_x, liste_y

### Etape 5.4 : trajectoire d'un oiseau avec frottement - récurrence
def lancer_oiseau_frottement_recurrence (alpha, l1):
    v0 = vitesse_initiale(alpha, l1)
    dt = 0.01 # Pas de temps (plus petit = plus précis)
    x, y = 0, 0 # Position initiale
    list_x = [0] # Liste des positions horizontales
    list_y = [0] # Liste des positions verticales
    vx = v0*np.cos(alpha) # Vitesse initiale - coordonnée x
    vy = v0*np.sin(alpha) # Vitesse initiale - coordonnée y
    while list_y[-1] >= 0: # Tant que l'oiseau n'a pas touché le sol
        x = x + vx*dt # Mise à jour de la position horizontale
        y = y + vy*dt # Mise à jour de la position verticale
        list_x.append(x) #stockage des positions
        list_y.append(y)
        vx += - f2 * vx * dt # Mise à jour de la vitesse horizontale
        vy += - (g + f2 * vy) * dt # Mise à jour de la vitesse verticale
    return list_x, list_y

### INTERFACE JOUEUR
## Etape 1.2 : calcul de v0
alpha_joueur_degres = float(input("Choisissez la valeur de l'angle alpha (en degrés) : "))
l1_joueur = float(input("Choisissez la longueur d'étirement du ressort (en cm) : "))
print(f"Vous avez choisi alpha = {alpha_joueur_degres}° et l1 = {l1_joueur} cm")
alpha_joueur = 2*np.pi*alpha_joueur_degres/360 #conversion en radians (python utilise les radians)
print(f"La vitesse initiale de l'oiseau est donc de = {vitesse_initiale(alpha_joueur, l1_joueur)} cm/s")

## Etape 2.3 : Afficher la trajectoire de l'oiseau
# afficher_oiseau(alpha_joueur, l1_joueur, lancer_oiseau) 

## Etape 3.2 : Afficher la trajectoire de l'oiseau pour plusieurs angles
# afficher_oiseaux_multiples(l1_joueur)

## Etape 4.3 : Afficher la trajectoire de l'oiseau avec frottement
# afficher_oiseau_frottement(alpha_joueur, l1_joueur, lancer_oiseau, lancer_oiseau_frottement) 

## Etape 5.3 : Afficher la trajectoire de l'oiseau par recurrence
afficher_oiseau(alpha_joueur, l1_joueur,lancer_oiseau_recurrence) 

## Etape 5.6 : Afficher la trajectoire de l'oiseau avec frottement par recurrence
## afficher_oiseau_frottement(alpha_joueur, l1_joueur,lancer_oiseau_recurrence,lancer_oiseau_frottement_recurrence) 
