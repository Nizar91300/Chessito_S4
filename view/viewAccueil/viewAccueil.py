from tkinter import Menu, BOTH, GROOVE, colorchooser

import tkinter as tk


# Classe Chessito, qui hérite de la classe tk.Tk
from view.viewAccueil.frameAccueil import FrameAccueil
from view.viewAccueil.frameNbJoueurs import FrameNbJoueur
from view.viewAccueil.frameNiveau import FrameNiveau


class ViewAccueil(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.minsize(600, 700)

        self.withdraw()

        # ajout du titre de la fenêtre
        self.title('Chessito')

        # ajout du logo sur la fenêtre
        self.iconbitmap('images/chessito_logo.ico')

        # création d'une barre de menu
        menubar = Menu(self)

        # création de parametre_menu
        parametre_menu = Menu(menubar, tearoff=0)

        # création d'un sous-menu preference_menu
        preference_menu = Menu(parametre_menu, tearoff=0)

        # création d'un sous-menu change_couleur_menu
        change_couleur_menu = Menu(preference_menu, tearoff=0)

        # ajout du sous-menu Préférence dans le menu Paramètre
        change_couleur_menu.add_command(label="Cases claires", command=lambda: self.alert_label_preference("light"))
        change_couleur_menu.add_command(label="Cases foncées", command=lambda: self.alert_label_preference("dark"))

        # ajout des items du sous-menu dans le menu Préférence
        preference_menu.add_cascade(label="Changer couleur des cases", menu=change_couleur_menu)

        # ajout du sous-menu Préférence dans le menu Paramètre
        parametre_menu.add_cascade(label="Préférences", menu=preference_menu)

        # ajout des items du menu dans le menu Paramètre
        parametre_menu.add_command(label="A propos", command=self.alert_label_a_propos)
        parametre_menu.add_separator()
        parametre_menu.add_command(label="Quitter", command=self.quit)

        # ajout du menu Paramètre dans le menubar
        menubar.add_cascade(label="Paramètre", menu=parametre_menu)

        self.config(menu=menubar)

        container = tk.Frame(self, borderwidth=5, relief=GROOVE)
        container.pack(side="top", fill=BOTH, expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        # créées et stockées les pages dans un dictionnaire
        frame = FrameAccueil(container, self)
        self.frames["Accueil"] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        for nom in ("Classique", "TTD", "Atomic"):
            frame = FrameNbJoueur(container, self, nom)
            self.frames[nom] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        for nom in ("ClassiqueNiveau", "AtomicNiveau", "TTDNiveau"):
            frame = FrameNiveau(container, self, nom)
            self.frames[nom] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Accueil")

        self.deiconify()

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    # alerte pour signaler quand un label de la barre de menu est activé.
    def labelBarMenu_alert(self,label_barmenu):
        print(f"Vous avez cliqué sur le label {label_barmenu}")

    # ajout de la fonction pour le label Préférence
    def alert_label_preference(self, color_type):
        self.labelBarMenu_alert("Préférences")

        color = colorchooser.askcolor()[1]  # ouvre une fenêtre de sélection de couleur
        if color:
            if color_type == "light":
                # Changer la couleur des cases claires
                print("La couleur des cases claires est " + color)
            else:
                # Changer la couleur des cases foncées
                print("La couleur des cases claires est " + color)

    # ajout de la fonction pour le label A Propos
    def alert_label_a_propos(self):
        self.labelBarMenu_alert("A Propos")


