from tkinter import Tk, Button, PanedWindow, HORIZONTAL, CENTER, messagebox, PhotoImage
from functools import partial
import os

from model.Echiquier import Echiquier
from model.pieces.Vide import Vide


class View:
    def __init__(self, controller):
        self.controller = controller
        self.buttons = [[0 for x in range(8)] for y in range(8)]
        self.images = {}  # dictionnaire pour stocker les images
        self.fenetre = Tk()
        self.fenetre.protocol("WM_DELETE_WINDOW", self.close_frame)

        # charger les images dans le dictionnaire
        for nom_piece in ["pion", "tour", "cavalier", "fou", "dame", "roi"]:
            for couleur in ["blanc", "noir"]:
                nom_image = nom_piece + "_" + couleur
                chemin_image = "../images/" + nom_image + ".png"
                # charger l'image

                photoimage = PhotoImage(file=chemin_image)
                self.images[nom_image] = photoimage

    def close_frame(self):
        self.fenetre.quit()
        self.fenetre.destroy()
        os._exit(0)


    def init_frame(self):
        # on recupere l'echiquier
        echiquier = Echiquier.echiquier
        self.fenetre.title("Echecs")
        width = 700
        height = 600
        xmax = self.fenetre.winfo_screenwidth()
        ymax = self.fenetre.winfo_screenheight()
        x0 = xmax / 2 - width / 2
        y0 = ymax / 2 - height / 2
        self.fenetre.geometry("%dx%d+%d+%d" % (width, height, x0, y0))
        self.fenetre.resizable(width=False, height=False)
        self.fenetre.configure(background='#e4edef')

        for i in range(8):
            panelModeDeJeu = PanedWindow(self.fenetre, orient=HORIZONTAL, background='#e4edef')
            for j in range(8):
                if (i + j) % 2 == 0:
                    couleur_case = "#CCB7AE"
                else:
                    couleur_case = "#706677"
                if isinstance(echiquier[i][j], Vide):
                    image_piece = ''
                    width_button = 4
                    height_button = 8
                else:
                    nom_piece = type(echiquier[i][j]).__name__.lower()
                    couleur = echiquier[i][j].couleur.name.lower()
                    nom_image = nom_piece + "_" + couleur
                    image_piece = self.images[nom_image]
                    width_button = height_button = int(min(width, height) / 10)

                button_size = 10  # 10% de la taille de la fenêtre
                self.buttons[i][j] = Button(panelModeDeJeu, image = image_piece, background=couleur_case, anchor=CENTER,
                                            command=partial(self.clic_btn_piece, echiquier[i][j]), height=width_button,
                                            width=height_button)

                self.buttons[i][j].image = image_piece
                panelModeDeJeu.add(self.buttons[i][j])

            panelModeDeJeu.pack()
        panel_historique = PanedWindow(self.fenetre, orient=HORIZONTAL, background='#e4edef')

        panel_historique.add(Button(panel_historique, text="Retour", command=self.controller.retour_deplacement, height=2, width=10))
        panel_historique.add(Button(panel_historique, text="Avancer", command=self.controller.avancer_deplacement, height=2, width=10))
        panel_historique.pack()

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

    def update_frame(self):
        echiquier = Echiquier.echiquier
        for i in range(8):
            for j in range(8):
                if isinstance(echiquier[i][j], Vide):
                    image_piece = ''
                else:
                    nom_piece = type(echiquier[i][j]).__name__.lower()
                    couleur = echiquier[i][j].couleur.name.lower()
                    nom_image = nom_piece + "_" + couleur
                    image_piece = self.images[nom_image]

                if (i + j) % 2 == 0:
                    couleur_case = "#CCB7AE"
                else:
                    couleur_case = "#706677"

                self.buttons[i][j].config(background = couleur_case, image = image_piece,
                                          command=partial(self.clic_btn_piece, echiquier[i][j]))

                # si les boutons sont désactivés, on les réactive
                if self.buttons[i][j]['state'] == 'disabled':
                    self.buttons[i][j].config(state='normal')

        # on met en evidence l'ancien deplacement
        if Echiquier.dernier_coup is not None:
            (oldL, oldC), (newL, newC) = Echiquier.dernier_coup
            self.buttons[oldL][oldC].config(background="#B0E0E6")
            self.buttons[newL][newC].config(background="#B0E0E6")

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