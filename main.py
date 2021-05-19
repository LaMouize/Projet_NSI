"""
Alessio CORTESE
Ethan
Lucas PETOVELLO
Raphaël GEORGET
"""
# ------------------------------------------------Imports---------------------------------------------------------------
from tkinter import *
from functools import partial
from threading import Thread
import re
import random

# ---------------------------------------------Variables globales-------------------------------------------------------
Largeur = 1280  # Largeur CANVAS
Hauteur = 720  # Hauteur CANVAS
Score = 0  # Score du jeu
meilleur_score = 0  # Variable de meilleur scores


# °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
# --------------------------------------------Ajouts/Fonctionalités-----------------------------------------------------
# °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
# Fenetre du formulaire :
def FenFormulaire():
    """
    Crée la Fenetre d'enregistrement des scores
    """
    global fenetre, Score
    Pop_up = Toplevel(fenetre)
    Pop_up.geometry("400x200")
    Pop_up.title('Enregistrer')
    Instructions = Label(Pop_up, text=f"Votre score actuel est {Score}")
    Instructions.grid(columnspan="2", row="0")
    Formulaire = Entry(Pop_up)
    Formulaire.grid(columnspan="2", row="1")
    Valider = Button(Pop_up, text="Valider", bg="green", command=partial(Sauv, Formulaire, Pop_up))
    Valider.grid(column="1", row="2")
    Annuler = Button(Pop_up, text="Annuler", bg="red", command=Pop_up.destroy)
    Annuler.grid(column="0", row="2")


# Sauvegarde des Scores :
def Sauv(Formulaire, Pop_up):
    """
    Permet d'enregistrer les données dans le document annexe
    :param Formulaire: Variable contenant la donnée saisie par l'utilisateur
    :param Pop_up: Variable contenant la fenetre
    :return: Nothing
    """
    global Score
    nom = Formulaire.get()
    score = Score
    fichier_score = open("scores.dat", "a")
    fichier_score.write(f"\n{nom}\n{score}")
    fichier_score.close()
    Pop_up.destroy()


# Lecture des meilleurs scores
def Records():
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
jeu.pack()


class Oiseau:
    """
    Classe qui regroupe les diférents paramètres de l'oiseau
    """
    Pause = True
    img = PhotoImage(file="bird.gif")

    def __init__(self):
        print("Création de l'oiseau")
        self.posX = Largeur / 6.5
        self.posY = Hauteur / 2
        self.image = jeu.create_image(self.posX, self.posY, image=Oiseau.img)
        self.velocity = 1
        self.multiplicateur = 1.0  # Simulation d'une gravitée
        self.framerate = 10  # Fréquence de raffraichissement 10ms
        self.saut = False
        self.Perdu = False

    def lancer(self):
        Oiseau.Pause = False

    lancement = classmethod(lancer)

    def Hitbox(self):
        """

        """
        if self.posY >= Hauteur - 30:
            print('Tombé !')
            self.multiplicateur = 1
            self.posY = Hauteur - 30
            self.Perdu = True
        if self.posY <= 42:
            self.posY = 41


    def Gravite(self):
        """
        Moteur de l'oiseau, cette fonction "infinnie" regroupe la gravitée et fait appel aux fonction Hitboxs et Saut
        """
        if not self.Perdu:
            self.Hitbox()
            jeu.bind("<Button-1>", self.Saut)
            if self.multiplicateur < 6:
                self.multiplicateur += 0.05
            self.posY += self.velocity * self.multiplicateur
            jeu.coords(self.image, self.posX, self.posY)
            fenetre.after(self.framerate, self.Gravite)
        else:
            print('Perdu !')

    def Saut(self, event=None):
        """
        Fait Sauter L'oiseau
        """
        self.multiplicateur = -3.2


class Tuyaux:
    """
    Classe qui regroupe les diférents paramètres des tuyaux
    """
    Pause = True

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

    def lancer(cls):
        Tuyaux.Pause = False

    def GenerationTuyaux(self):
        aleatoire = random.randint(50, Hauteur - 170)
        self.AY2 = aleatoire
        self.BY1 = aleatoire + 170

    def MouvementTuyaux(self):
        self.AX1 -= 1
        self.AX2 -= 1
        jeu.coords(self.Tuyau_haut, self.AX1, self.AY1, self.AX2, self.AY2)
        self.BX1 -= 1
        self.BX2 -= 1
        jeu.coords(self.Tuyau_bas, self.BX1, self.BY1, self.BX2, self.BY2)
        fenetre.after(5, self.MouvementTuyaux)


#  ------------------------------------Programmation Externe du Flappy Bird---------------------------------------------
def Jouer():
    """
    Démarre le Jeu
    :return:
    """
    if not Oiseau.Pause and not Tuyaux.Pause:
        print('Jeu déja lancé !')
    else:
        lancement_Oiseau = Oiseau()
        lancement_Tuyaux = Tuyaux()
        lancement_Oiseau.lancer()
        lancement_Tuyaux.lancer()
        lancement_Oiseau.Gravite()
        lancement_Oiseau.Hitbox()
        lancement_Tuyaux.MouvementTuyaux()


def Changediff():
    """
    Ouvre le fichier de Configuration du jeu afin de modifer la Velocity (Vitesse)
    Détail : Boite de dialogue avec Entry puis Button en dessous
    :return:
    """
    ...

def Relancer():
    """
    Relance le jeu
    """
    pass

# ---------------------------------------------Création du Menu---------------------------------------------------------
menu_bar = Menu(fenetre)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Quitter", command=fenetre.quit)
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
fenetre.mainloop()
