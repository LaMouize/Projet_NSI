"""
Alessio CORTESE
Ethan
Lucas PETOVELLO
Raphaël GEORGET
"""
# ------------------------------------------------Imports---------------------------------------------------------------
from tkinter import *
from functools import partial
import re
import random
import time

# ---------------------------------------------Variables globales-------------------------------------------------------
Largeur = 1280  # Largeur CANVAS
Hauteur = 720  # Hauteur CANVAS
Score = 0  # Score du jeu
meilleur_score = 0  # Variable de meilleur scores
Pause = True  # Pause


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
#  programmation Flappy
def Jouer():
    """
    Démarre le Jeu
    :return:
    """
    global Pause
    Pause = False
    print('test')
    return Pause


def Changediff():
    """
    Ouvre le fichier de Configuration du jeu afin de modifer la Velocity (Vitesse)
    Détail : Boite de dialogue avec Entry puis Button en dessous
    :return:
    """
    ...


# --------------------------------------------Création de la Fenetre----------------------------------------------------

fenetre = Tk()  # Stockée dans la variable "fenetre"
fenetre.title('Oiseau Fou')  # Titre de la fenêtre
fenetre.resizable(width=False, height=False)  # Empeche le changement de taille de la fenêtre
fenetre.geometry(str(Largeur) + "x" + str(Hauteur))
main_icon = PhotoImage(file="icon.ico")  # Icone de la fenetre
fenetre.iconphoto(False, main_icon)

# Le Menu
menu_bar = Menu(fenetre)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Quitter", command=fenetre.quit)
menu_bar.add_cascade(label="Fichier", menu=file_menu)

game_menu = Menu(menu_bar, tearoff=0)
game_menu.add_command(label="Lancer_Partie", command=Jouer)
game_menu.add_command(label="Changer_difficultée", command=Changediff)
menu_bar.add_cascade(label="Jeu", menu=game_menu)

score_menu = Menu(menu_bar, tearoff=0)
score_menu.add_command(label="Records", command=Records)
score_menu.add_command(label="Enregistrer", command=FenFormulaire)
menu_bar.add_cascade(label="Scores", menu=score_menu)

fenetre.config(menu=menu_bar)

# -------------------------------------------------Début du Flappy------------------------------------------------------
jeu = Canvas(fenetre, bg="#4EC0CA", width=Largeur, height=Hauteur)
jeu.pack()
# 1)    OISEAU
Oiseau_X = Largeur / 6.5
Oiseau_Y = Hauteur / 2
Imageoiseau = PhotoImage(file="bird.gif")
BIRD = jeu.create_image(Oiseau_X, Oiseau_Y, image=Imageoiseau)
Bird_Move_Down = 1  # Vitesse déplacement bas   ==> Plus tard modifiable dans Changediff()
YB = Oiseau_Y
Bird_Move_Up = 1.3  # Vitesse de montée

def MouvementBasOiseau():
    global Pause, Bird_Move_Down, Hauteur, YB, Oiseau_X
    #if not Pause:
    if YB >= Hauteur - 50:
        YB = Hauteur - 50
        Bird_Move_Down = 1
    jeu.coords(BIRD, Oiseau_X, YB)
    YB = YB + 1 * Bird_Move_Down
    fenetre.after(20, MouvementBasOiseau)
     # Limite du facteur de chute
    Bird_Move_Down += 0.40  # Semblant de Gravitée facteur 0.15   ==> Plus tard modifiable dans Changediff()



def MouvementHautOiseau(event=None):
    global Bird_Move_Up, YB, Oiseau_X, Bird_Move_Down
    #print('Hi')
    #print(Bird_Move_Up, " ", YB, " ", Oiseau_X, " ", Bird_Move_Down)
    Bird_Move_Down = -6 * Bird_Move_Up # Gravitée nulle




# 2)    TUYAUX
# A- Haut Tuyau
AX1 = 1100
AY1 = 0  # Angle rect haut gauche
AX2 = 1000
AY2 = 300  # Angle rect bas droit face au trou de l'oiseau
Tuyaux_bas = jeu.create_rectangle(AX1, AY1, AX2, AY2, fill="green", outline="red")

# B- Bas Tuyau
BX1 = 1100
BY1 = 500  # Angle rect haut gauche face au trou de l'oiseau
BX2 = 1000
BY2 = Hauteur  # Angle rect bas droit
Tuyaux_haut = jeu.create_rectangle(BX1, BY1, BX2, BY2, fill="green", outline="red")


def GenerationTuyaux():
    """
    Génère aléatoirement la hauteur des tuyaux avec espace de 200 entre Tuyaux_haut et Tuyaux_bas
    :return: Aucun Return
    """
    global AX1, AY1, AX2, AY2, BX1, BY1, BX2, BY2
    global Score
    global Hauteur

    Score += 1
    yalea = random.randint(210, Hauteur - 210)
    AY2 = yalea
    BY1 = yalea + 100
    # print(AX1, AY1, AX2, AY2, "\n", BX1, BY1, BX2, BY2, "\n", 'Voici le yalea :', yalea, "\n")  # DEBUG


def MouvementTuyaux():
    global Score
    ...


MouvementBasOiseau()
jeu.bind("<Button-1>", MouvementHautOiseau)

# **********************************************************************************************************************
# --------------------------------------------------FIN PROGRAMME-------------------------------------------------------
# **********************************************************************************************************************
fenetre.mainloop()
