from tkinter import Menu, BOTH, GROOVE, colorchooser

import tkinter as tk

# Classe Chessito, qui hérite de la classe tk.Tk
from controller.controllerNormal import ControllerNormal
from model import constantes
from model.EchiquierAtomic import EchiquierAtomic
from model.EchiquierNormal import EchiquierNormal
from view.viewAccueil.frameAccueil import FrameAccueil
from view.viewAccueil.frameNbJoueurs import FrameNbJoueur
from view.viewAccueil.frameNiveau import FrameNiveau
from view.viewAccueil.frameTimer import FrameTimer


class ViewAccueil(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.minsize(600, 700)
        self.geometry("900x700")

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
        parametre_menu.add_command(label="Revenir au menu principal", command=self.revenir_menu_principal)
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
        for nom in ("Classique", "Atomic", "TTD"):
            frame = FrameNbJoueur(container, self, nom)
            self.frames[nom] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        for nom in ("ClassiqueNiveau", "AtomicNiveau", "TTDNiveau"):
            frame = FrameNiveau(container, self, nom)
            self.frames[nom] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        for nom in ("ClassiqueNiveauTimer", "AtomicNiveauTimer", "TTDNiveauTimer", ):
            frame = FrameTimer(container, self, nom)
            self.frames[nom] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Accueil")

        self.deiconify()

    def revenir_menu_principal(self):
        self.destroy()
        self.__init__()

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
        print(color)
        if color:
            if color_type == "light":
                constantes.CASE_BLANCHE = color
            else:
                constantes.CASE_NOIRE = color

    # ajout de la fonction pour le label A Propos
    def alert_label_a_propos(self):
        self.labelBarMenu_alert("A Propos")

    def partie_bot(self, mode, difficulte):
        for widget in self.winfo_children():
            if not widget.winfo_class() == "Menu":
                widget.destroy()

        controller = None
        if mode == "Classique":
            if difficulte == "Facile":
                controller = ControllerNormal( EchiquierNormal(True, 0) , self)
            elif difficulte == "Intermediaire":
                controller = ControllerNormal( EchiquierNormal(True, 1), self )
            elif difficulte == "Difficile":
                controller = ControllerNormal( EchiquierNormal(True, 2), self)

        elif mode == "Atomic":
            if difficulte == "Facile":
                controller = ControllerNormal( EchiquierAtomic(True, 0), self )
            elif difficulte == "Intermediaire":
                controller = ControllerNormal( EchiquierAtomic(True, 1), self )
            elif difficulte == "Difficile":
                controller = ControllerNormal( EchiquierAtomic(True, 2), self )

        elif mode == "TTD":
            print("Pas encore implémenté")
            return

        controller.run()

    def partie_joueur(self, mode):
        for widget in self.winfo_children():
            if not widget.winfo_class() == "Menu":
                widget.destroy()

        controller = None
        if mode == "Classique":
            controller = ControllerNormal( EchiquierNormal(False, 0), self)

        elif mode == "Atomic":
            controller = ControllerNormal( EchiquierAtomic(False, 0), self )

        elif mode == "TTD":
            print("Pas encore implémenté")
            return

        controller.run()


