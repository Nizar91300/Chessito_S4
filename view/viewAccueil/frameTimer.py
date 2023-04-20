from tkinter import Image, CENTER, Frame, RIDGE, Label, ttk, BOTTOM, BOTH

import tkinter as tk
from PIL import ImageTk
import PIL.Image
from model.constantes import CASE_BLANCHE, CASE_NOIRE, GRIS

# Page de choix du temps de la partie Classique
class FrameTimer(tk.Frame):
    def __init__(self, parent, controller, titre):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.titre = titre

        # ajout d'une image de fond pour la fenêtre.
        # Ouvrir l'image avec PIL
        bg_Image = PIL.Image.open('images/bg_chessboard.png')

        # Convertir l'image dans un format compatible avec tkinter
        bg_Photo = ImageTk.PhotoImage(bg_Image)

        # Créer un widget d'image tkinter pour afficher l'image
        bg_label = tk.Label(self, image=bg_Photo)
        bg_label.image = bg_Photo  # Garder une référence à l'objet PhotoImage
        bg_label.place(relx=0.5, rely=0.5, anchor=CENTER)
        bg_label.pack()

        # frame principale
        FramePrincipale = Frame(self, borderwidth=5, relief=RIDGE, bg=GRIS)

        # centrer FramePrincipale au milieu de la fenêtre principale.
        FramePrincipale.place(relx=0.5, rely=0.5, anchor=CENTER)

        # insérer le logo du jeu dans FramePrincipale.
        # Ouvrir l'image avec PIL
        logo_image = PIL.Image.open('images/chessito_logo.png')

        # Convertir l'image dans un format compatible avec tkinter
        logo_photo = ImageTk.PhotoImage(logo_image)

        # Créer un widget d'image tkinter pour afficher l'image
        label = tk.Label(FramePrincipale, background=GRIS, highlightthickness=0, image=logo_photo)
        label.image = logo_photo  # Garder une référence à l'objet PhotoImage
        label.pack()

        # ajout d'un label pour le titre du FrameChoixJoueur.
        lblMenu = Label(FramePrincipale, text=self.titre.split('N')[0], bg=GRIS, fg=CASE_BLANCHE, font=('Arial', 24))
        lblMenu.pack(padx=10, pady=10)

        # bouton pour revenir à la page précédente.
        btnRetour = ttk.Button(FramePrincipale, text='Retour', command=lambda: controller.show_frame("Classique"))
        btnRetour.pack(side=BOTTOM, pady=10)
        btnRetour.configure(style='TButton')

        # frame FrameChoixTemps dans FramePrincipale.
        FrameChoixTemps = Frame(FramePrincipale, bg=GRIS)
        FrameChoixTemps.pack(padx=83, pady=40)

        # Durée de temps initiale
        self.temps_restant = 0

        # Créer les temps prédéfinis
        self.temps = [
            ('3 min', 3, 180),
            ('5 min', 5, 300),
            ('10 min', 10, 600),
            ('20 min', 20, 1200),
            ('30 min', 30, 1800),
            ('60 min', 60, 3600)
        ]

        # Ajouter les boutons de choix de temps
        for i, (temps_label, temps_minutes, temps_secondes) in enumerate(self.temps):
            bouton_temps = ttk.Button(FrameChoixTemps, text=temps_label, command=lambda: controller.show_frame(ClassiqueGame))
            bouton_temps.grid(row=i // 2, column=i % 2, padx=5, pady=5)
            bouton_temps.configure(style='TButton')