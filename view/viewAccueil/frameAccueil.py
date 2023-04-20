# Page Accueil
from tkinter import CENTER, RIDGE, Frame, BOTH, ttk, BOTTOM, Label
from model.constantes import CASE_BLANCHE, CASE_NOIRE, GRIS
import tkinter as tk
from PIL import ImageTk
import PIL.Image

class FrameAccueil(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

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

        # insérer le logo du jeu dans FramePrincipale
        # Ouvrir l'image avec PIL
        logo_image = PIL.Image.open('images/chessito_logo.png')

        # Convertir l'image dans un format compatible avec tkinter
        logo_photo = ImageTk.PhotoImage(logo_image)

        # Créer un widget d'image tkinter pour afficher l'image
        label = tk.Label(FramePrincipale, background=GRIS, highlightthickness=0, image=logo_photo)
        label.image = logo_photo  # Garder une référence à l'objet PhotoImage
        label.pack()

        # ajout d'un label pour le titre du menu.
        lblMenu = Label(FramePrincipale, text="Accueil", bg=GRIS, fg=CASE_BLANCHE, font=('Arial', 24))
        lblMenu.pack(padx=10, pady=10)

        # bouton pour quitter l'application.
        btnQuitter = ttk.Button(FramePrincipale, text='Quitter', command=self.quit)

        style = ttk.Style()

        # Configuration des couleurs pour les différents états du bouton quand le curseur passe au-dessus du bouton.
        style.map('TButton', foreground=[('active', 'red'), ('!active', 'black')],
                  background=[('active', 'black'), ('!active', 'SystemButtonFace')])

        # Définir la configuration de style une fois pour toutes
        style.configure('TButton', bordercolor="#fff", background=CASE_NOIRE, foreground=CASE_NOIRE,
                              font=("Calibri", 16, "bold"), padding=4)

        btnQuitter.pack(side=BOTTOM, pady=10)
        btnQuitter.configure(style='TButton')

        # frame Menu dans FramePrincipale
        FrameMenu = Frame(FramePrincipale, bg=GRIS)
        FrameMenu.pack(padx=50, pady=40)

        # boutons pour les modes de jeu.
        btnClassique = ttk.Button(FrameMenu, text='Classique', command=lambda: controller.show_frame("Classique"))
        btnTTD = ttk.Button(FrameMenu, text='Tactical TakeDown', command=lambda: controller.show_frame("TTD"))
        btnAtomic = ttk.Button(FrameMenu, text='Atomic', command=lambda: controller.show_frame("Atomic"))

        # ajout des boutons pour les modes de jeu dans la FrameMenu.
        btnClassique.pack(ipady=15, fill=BOTH, expand=True)
        btnClassique.configure(style='TButton')

        btnTTD.pack(ipady=15, pady=20, fill=BOTH, expand=True)
        btnTTD.configure(style='TButton')

        btnAtomic.pack(ipady=15, fill=BOTH, expand=True)
        btnAtomic.configure(style='TButton')