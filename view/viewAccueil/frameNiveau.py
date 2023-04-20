from tkinter import Image, CENTER, Frame, RIDGE, Label, ttk, BOTTOM, BOTH

import tkinter as tk
from PIL import ImageTk
import PIL.Image
from model.constantes import CASE_BLANCHE, CASE_NOIRE, GRIS

# Page de choix du niveau de la partie Classique
class FrameNiveau(tk.Frame):
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

        # frame FrameChoixJoueur dans FramePrincipale.
        FrameChoixJoueur = Frame(FramePrincipale, bg=GRIS)
        FrameChoixJoueur.pack(padx=83, pady=40)

        # boutons pour les modes de jeu.
        btnFacile = ttk.Button(FrameChoixJoueur, text='Facile', command=lambda: controller.show_frame(ClassiqueFacile))
        btnIntermediaire = ttk.Button(FrameChoixJoueur, text='Intermédiaire', command=lambda: controller.show_frame(ClassiqueMoyen))
        btnDifficile = ttk.Button(FrameChoixJoueur, text='Difficile', command=lambda: controller.show_frame(ClassiqueDifficile))

        # ajout des boutons pour les modes de jeu dans la FrameChoixJoueur.
        btnFacile.pack(ipady=15, fill=BOTH, expand=True)
        btnFacile.configure(style='TButton')

        btnIntermediaire.pack(ipady=15, pady=20, fill=BOTH, expand=True)
        btnIntermediaire.configure(style='TButton')

        btnDifficile.pack(ipady=15, fill=BOTH, expand=True)
        btnDifficile.configure(style='TButton')

