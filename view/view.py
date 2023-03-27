import tkinter
import copy
from tkinter import messagebox, Tk, Button
import customtkinter
import PIL.Image, PIL.ImageTk, PIL.ImageFilter

from functools import partial
import os

import PIL.Image

from model.Echiquier import Echiquier
from model.pieces.Vide import Vide


class View:
    def __init__(self, controller):
        self.controller = controller
        self.buttons = [[None for x in range(8)] for y in range(8)]
        self.images = {}  # dictionnaire pour stocker les images
        self.fenetre = Tk()
        self.fenetre.protocol("WM_DELETE_WINDOW", self.close_frame)

        # charger les images des pions
        for nom_piece in ["pion", "tour", "cavalier", "fou", "dame", "roi"]:
            for couleur in ["blanc", "noir"]:
                nom_image = nom_piece + "_" + couleur
                chemin_image = "images/" + nom_image + ".png"
                # charger l'image
                img = PIL.Image.open(chemin_image)
                self.images[nom_image] = img

        self.images["case_blanche"] = PIL.Image.open("images/case_blanche.png")



    def close_frame(self):
        self.fenetre.quit()
        self.fenetre.destroy()
        os._exit(0)


    def init_frame(self):
        # on recupere l'echiquier
        echiquier = Echiquier.echiquier
        self.fenetre.title("Chessito")
        #logo = ImageTk.PhotoImage("images/logo.png")
        #self.fenetre.iconphoto(False, logo)
        width = 700
        height = 600
        xmax = self.fenetre.winfo_screenwidth()
        ymax = self.fenetre.winfo_screenheight()
        x0 = xmax / 2 - width / 2
        y0 = ymax / 2 - height / 2
        self.fenetre.geometry("%dx%d+%d+%d" % (width, height, x0, y0))
        self.fenetre.resizable(width=False, height=False)
        self.fenetre.configure(background='#e4edef')

        # on cree d'abord les bonnes images à afficher
        img_cases = self.images_echiquier()

        # on place la bonne image sur le bon bouton
        for i in range(8):
            for j in range(8):
                self.buttons[i][j] = Button(self.fenetre, image = img_cases[i][j], border=0,
                                            command=partial(self.clic_btn_piece, echiquier[i][j]), height=60,
                                            width=60)

                self.buttons[i][j].grid(row=i+1, column=j+1)

        Button(self.fenetre, text="Retour", command=self.controller.retour_deplacement,
               height=2, width=10).grid(row=9, column=3, columnspan=2, sticky="WE")
        Button(self.fenetre, text="Avancer", command=self.controller.avancer_deplacement,
               height=2, width=10).grid(row=9, column=5, columnspan=2, sticky="WE")

        self.fenetre.rowconfigure(0, weight=1)
        self.fenetre.rowconfigure(10, weight=1)
        self.fenetre.columnconfigure(0, weight=1)
        self.fenetre.columnconfigure(9, weight=1)

        # pour que la fentre soit toujours active et que le programme ne se bloque pas
        while True:
            self.fenetre.update()
            self.fenetre.update_idletasks()

    def clic_btn_vide(self, l, c):
        self.controller.selectionner_case_vide(l, c)

    def clic_btn_piece(self, piece):
        if not isinstance(piece, Vide):
            print(type(piece).__name__[0] + piece.couleur.name[0])
        self.controller.selectionner_piece(piece)

    def images_echiquier(self):
        echiquier = Echiquier.echiquier
        img_cases = [[None for x in range(8)] for y in range(8)]
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    case_img = self.images["case_blanche"].copy()
                else:
                    case_img = self.images["case_blanche"].copy()

                # on met en evidence l'ancien deplacement
                if Echiquier.dernier_coup is not None and (i, j) in Echiquier.dernier_coup:
                    case_img = case_img.filter(PIL.ImageFilter.GaussianBlur(radius=5))
                if not isinstance(echiquier[i][j], Vide):
                    nom_image = type(echiquier[i][j]).__name__.lower() + "_" + echiquier[i][j].couleur.name.lower()
                    case_img.paste(self.images[nom_image].copy(), (0, 0), mask=self.images[nom_image].copy())
                img_cases[i][j] = PIL.ImageTk.PhotoImage(case_img.resize((60, 60), PIL.Image.ANTIALIAS))
        return img_cases

    def update_frame(self):
        echiquier = Echiquier.echiquier
        img_cases = self.images_echiquier()
        for i in range(8):
            for j in range(8):
                self.buttons[i][j].config(image = img_cases[i][j], command=partial(self.clic_btn_piece, echiquier[i][j]))

                # si les boutons sont désactivés, on les réactive
                if self.buttons[i][j]['state'] == 'disabled':
                    self.buttons[i][j].config(state='normal')

    def affiche_deplacements(self, depPossible):
        for x, y in depPossible:
            self.buttons[x][y].config(background="#769656")

    def cacher_deplacements(self, depPossible):
        for x, y in depPossible:
            if (x + y) % 2 == 0:
                couleur_case = "#CCB7AE"
            else:
                couleur_case = "#706677"
            if Echiquier.dernier_coup is not None:
                (oldL, oldC), (newL, newC) = Echiquier.dernier_coup
                if (x, y) == (oldL, oldC) or (x, y) == (newL, newC):
                    couleur_case = "#B0E0E6"

            self.buttons[x][y].config(background=couleur_case)

    def afficher_fin_de_partie(self, couleur, type_fin):
        match type_fin:
            case 0:
                msg = 'Les ' + couleur.name.lower() + 's ont gagné par echec et mat. Voulez-vous rejouer ?'
            case 1:
                msg = 'Match nul par pat. Voulez-vous rejouer ?'
            case 2:
                msg = 'Match nul par position morte. Voulez-vous rejouer ?'
            case 3:
                msg = 'Match nul par répétition. Voulez-vous rejouer ?'

        msg_box = messagebox.askquestion("Fin de partion", msg, icon='question')
        if msg_box == 'yes':
            self.controller.rejouer()
        else:
            self.close_frame()

    # on affiche l'historique d'un coup deja joue
    def afficher_historique(self):
        self.update_frame()
        for i in range(8):
            for j in range(8):
                self.buttons[i][j].config(state="disabled")