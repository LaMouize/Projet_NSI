"""
Alessio CORTESE
Ethan TILLIER
Lucas PETOVELLO
Raphaël GEORGET
"""
# --------------------------------------------------Imports-------------------------------------------------------------
from tkinter import *
from functools import partial

import re
import random

# ---------------------------------------------Variables globales-------------------------------------------------------
Largeur = 1280  # Largeur CANVAS
Hauteur = 720  # Hauteur CANVAS


# °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
# --------------------------------------------Ajouts/Fonctionalités-----------------------------------------------------
# °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
# Fenetre du formulaire :
def FenFormulaire():
    """
    Crée la Fenetre d'enregistrement des scores
    Partial est une variante plus simple à utiliser que lambda et plus facilement lisible
    """
    global fenetre
    Pop_up = Toplevel(fenetre)
    Pop_up.geometry("400x200")
    Pop_up.title('Enregistrer')
    Instructions = Label(Pop_up, text=f"Votre score actuel est {Jeu.Score}")
    Instructions.grid(columnspan="2", row="0")
    Formulaire = Entry(Pop_up)
    Formulaire.grid(columnspan="2", row="1")
    Valider = Button(Pop_up, text="Valider", bg="green", command=partial(Sauv, Formulaire, Pop_up))
    Valider.grid(column="1", row="2")
    Annuler = Button(Pop_up, text="Annuler", bg="red", command=Pop_up.destroy)
    Annuler.grid(column="0", row="2")


# command = lambda : f(1,2,3)
# Sauvegarde des Scores :
def Sauv(Formulaire, Pop_up):
    """
    Permet d'enregistrer les données dans le document annexe
    :param Formulaire: Variable contenant la donnée saisie par l'utilisateur
    :param Pop_up: Variable contenant la fenetre
    """
    nom = Formulaire.get()
    score = Jeu.Score
    fichier_score = open("scores.dat", "a")
    fichier_score.write(f"\n{nom}\n{score}")
    fichier_score.close()
    Pop_up.destroy()


# Lecture des meilleurs scores
def Records():
    """
    Enregistre le score dans le document scores.dat
    """
    Nouvelle_fen = Toplevel(fenetre)
    Nouvelle_fen.geometry("500x700")
    Nouvelle_fen.resizable(width=False, height=False)
    Nouvelle_fen.title("Records")
    fichier_score = open("scores.dat", "r")
    liste_score = fichier_score.readlines()
    fichier_score.close()
    liste_claire = []
    for k in liste_score:
        regex = re.compile(r'[\n]')
        k = regex.sub("", k)
        liste_claire.append(k)
    liste_Tuples = []
    for test in range(1, len(liste_claire), 2):
        A = (liste_claire[test - 1], liste_claire[test])
        liste_Tuples.append(tuple(A))
    #  Tri par ordre Décroissant:
    ScoreTri = sorted(liste_Tuples, key=lambda student: student[1], reverse=True)
    #  Affichage des Meilleurs Scores dans la fenetre
    p = 0
    for k in range(len(ScoreTri)):
        p += 1
        for l in range(2):
            Scores_ecrit = Label(Nouvelle_fen, text=ScoreTri[k][l])
            Scores_ecrit.grid(row=p, column=l)


# **********************************************************************************************************************
# --------------------------------------------Programme principal-------------------------------------------------------
# **********************************************************************************************************************

# --------------------------------------------Création de la Fenetre----------------------------------------------------

fenetre = Tk()  # Stockée dans la variable "fenetre"
fenetre.title('Oiseau Fou')  # Titre de la fenêtre
fenetre.resizable(width=False, height=False)  # Empeche le changement de taille de la fenêtre
fenetre.geometry(str(Largeur) + "x" + str(Hauteur))
main_icon = PhotoImage(file="icon.ico")  # Icone de la fenetre
fenetre.iconphoto(False, main_icon)

# -------------------------------------------------Début du Flappy------------------------------------------------------
jeu = Canvas(fenetre, bg="#4EC0CA", width=Largeur, height=Hauteur)
jeu.pack()  # Alternative Tkinter à la fonction Grid, très utile ici car la fenetre contient uniquement le Canevas


class Oiseau:
    """
    Classe qui regroupe les diférents paramètres de l'oiseau
    """

    img = PhotoImage(file="bird.gif")  # Permet d'enregistrer une image dans une variable. ici celle de l'oiseau

    def __init__(self):
        print("Création de l'oiseau")
        self.posX = Largeur / 6.5  # Positionne l'oiseau sur le canevas en fonction de sa taille ici la Largeur
        self.posY = Hauteur / 2  # Positionne l'oiseau sur le canevas en fonction de sa taille ici la Hauteur
        self.image = jeu.create_image(self.posX, self.posY, image=Oiseau.img)
        self.coordsOiseau = jeu.bbox(self.image)  # Enregistre X1 X2 et le Y1 Y2 de l'image OISEAU
        self.velocity = 1  # Velocity = Vitesse en anglais
        self.multiplicateur = 1.0  # Simulation d'une gravitée

    def Gravite(self):
        """
        Moteur de l'oiseau, cette fonction "infinnie" regroupe la gravitée et fait appel aux fonction Hitboxs et Saut
        """
        if self.multiplicateur < 6:
            self.multiplicateur += 0.05
        self.posY += self.velocity * self.multiplicateur
        jeu.coords(self.image, self.posX, self.posY)

    def Saut(self, event=None):
        """
        event=None, Obligatoire car contenant self en premier param et étant actioné par un BIND
        Fait Sauter L'oiseau
        """
        self.multiplicateur = -3


class Tuyaux:
    """
    Classe qui regroupe les diférents paramètres des tuyaux
    """

    def __init__(self):
        self.AX1 = 1100
        self.AY1 = 0
        self.AX2 = 1000
        self.AY2 = 300
        self.BX1 = 1100
        self.BY1 = 500
        self.BX2 = 1000
        self.BY2 = Hauteur
        self.Tuyau_haut = jeu.create_rectangle(self.AX1, self.AY1, self.AX2, self.AY2, fill="green", outline="red")
        self.Tuyau_bas = jeu.create_rectangle(self.BX1, self.BY1, self.BX2, self.BY2, fill="green", outline="red")

    def GenerationTuyaux(self):
        aleatoire = random.randint(50, Hauteur - 185)
        self.AY2 = aleatoire
        self.BY1 = aleatoire + 185

    def MouvementTuyaux(self):
        self.AX1 -= 1
        self.AX2 -= 1
        jeu.coords(self.Tuyau_haut, self.AX1, self.AY1, self.AX2, self.AY2)
        self.BX1 -= 1
        self.BX2 -= 1
        jeu.coords(self.Tuyau_bas, self.BX1, self.BY1, self.BX2, self.BY2)
        if self.AX1 == 0:
            self.AX1 = 1100
            self.AY1 = 0
            self.AX2 = 1000
            self.BX1 = 1100
            self.BX2 = 1000
            self.BY2 = Hauteur
            self.GenerationTuyaux()

        # print(Tuyaux.Perdu)


class Jeu(Oiseau, Tuyaux):
    """
    Classe maitresse qui utilise les données des classe Tuyaux et Oiseau afin de créer le jeu
    Cette classe s'initialise avec en mémoire l'ensemble des fonctions et varaibles __init() des classes Oiseau Tuyaux
    ce qui permet le d'accèder, de modifier, de lire ce que l'on veut des deux classes.
    Pour résumer, nous avons vu cette année les fonctions avec le mot clé : "global ..." qui permetait de récupérer des
    variables exterieures. Ici pour des raisons de simplifications et de lisibilités de ce code nous avons choisit les
    classes
    L’héritage dans la programmation permet de faire plus avec moins de code et de répétition.
    l'héritage garantie l’efficacité et la clarté du code.
    """
    Score = 0

    def __init__(self):
        self.pause = False  # Comme son nom l'indique ^^
        self.perdu = False  # Comme son nom l'indique ^^
        self.Latence_Oiseau = 10  # latence en milisecondes de l'oiseau, Correspond au délai avant la prochaine --->
        self.Latence_Tuyaux = 4  # éxécution. Se rapproche d'une boucle infinnie. VARIABLE UTILISEE PLUS TARD
        Oiseau.__init__(self)  # Récupère les variables globales de la classe Oiseau comme ses coordonnées etc ...
        Tuyaux.__init__(self)  # Récupère les variables globales de la classe Tuyaux comme ses coordonnées etc ...

    def Lancement_Jeu(self):
        if not self.pause and not self.perdu:
            self.Boucle_Oiseau()
            self.Boucle_Tuyaux()
            jeu.bind("<Button-1>", self.Saut)
        else:
            print('Jeu déja lancé !')

    def Boucle_Oiseau(self):
        if not self.perdu:
            self.Gravite()
            self.Verif_Hitbox()
            self.coordsOiseau = jeu.bbox(self.image)  # Met à jour la variable
            jeu.after(self.Latence_Oiseau, self.Boucle_Oiseau)

    def Boucle_Tuyaux(self):
        if not self.perdu:
            self.MouvementTuyaux()
            if self.AX1 == 0:
                Jeu.Score += 1
            jeu.after(self.Latence_Tuyaux, self.Boucle_Tuyaux)

    def Verif_Hitbox(self):
        """
        Canalise l'oiseau dans la fenêtre
        Arrête le jeu en cas de contact avec un Tuyau
        """
        # Arrete le jeu si l'oiseau touche le sol
        if self.posY >= Hauteur - 30:
            self.multiplicateur = 1
            self.posY = Hauteur - 30
            self.perdu = True
        # Empeche l'oiseau de sortir vers le haut
        if self.posY <= 42:
            self.posY = 41
        # Arrete le jeu si collision
        Haut = jeu.find_overlapping(self.AX1, self.AY1, self.AX2, self.AY2)
        Bas = jeu.find_overlapping(self.BX1, self.BY1, self.BX2, self.BY2)
        if len(Haut) == 2 or len(Bas) == 2:
            self.perdu = True


#  --------------------------------------------Programmation Externe du Flappy Bird-------------------------------------
def Jouer():
    """
    Démarre le Jeu
    Empeche le jeu de se relancer. find.all renvoie une liste d'ID présent, si > 0, le jeu à déjà été lancé
    """
    if not len(jeu.find_all()) > 0:
        lancer = Jeu()
        lancer.Lancement_Jeu()


def Changediff():
    """
    Ouvre le fichier de Configuration du jeu afin de modifer la Velocity (Vitesse)
    Détail : Boite de dialogue avec Entry puis Button en dessous
     /!\ Disponible dans la prochaine mise à jour, dans une nouvelle classe esclave de Jeu() dédiée /!\
    """
    pass


def Relancer():
    """
    Supprime toutes les ID/ entitées du Canevas jeu
    Réinitialise le Score
    Relance le jeu
    """
    jeu.delete(ALL)
    Jeu.Score = 0
    Jouer()


# ---------------------------------------------------Création du Menu---------------------------------------------------
menu_bar = Menu(fenetre)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Quitter", command=fenetre.destroy)
menu_bar.add_cascade(label="Fichier", menu=file_menu)

game_menu = Menu(menu_bar, tearoff=0)
game_menu.add_command(label="Lancer_Partie", command=Jouer)
game_menu.add_command(label="Changer_difficultée", command=Changediff)
game_menu.add_command(label="Relancer_Partie", command=Relancer)
menu_bar.add_cascade(label="Jeu", menu=game_menu)

score_menu = Menu(menu_bar, tearoff=0)
score_menu.add_command(label="Records", command=Records)
score_menu.add_command(label="Enregistrer", command=FenFormulaire)
menu_bar.add_cascade(label="Scores", menu=score_menu)

fenetre.config(menu=menu_bar)

# **********************************************************************************************************************
# --------------------------------------------------FIN PROGRAMME-------------------------------------------------------
# **********************************************************************************************************************
fenetre.mainloop()  # Boucle de répétition
