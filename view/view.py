import os
import tkinter
from functools import partial
from tkinter import messagebox, Tk, Button, Label
import PIL.Image, PIL.ImageTk, PIL.ImageFilter, PIL.ImageDraw

from model.Echiquier import Echiquier
from model.pieces.Vide import Vide


class View:
    def __init__(self, controller):
        self.controller = controller
        self.cases = [[tkinter.Button for x in range(8)] for y in range(8)]
        self.images = {}  # dictionnaire pour stocker les images
        self.fenetre = Tk()
        self.fenetre.protocol("WM_DELETE_WINDOW", self.close_frame)

        # charger les images des pions
        for nom_piece in ["pion", "tour", "cavalier", "fou", "dame", "roi"]:
            for couleur in ["blanc", "noir"]:
                nom_image = f"{nom_piece}_{couleur}"
                chemin_image = f"images/{nom_image}.png"
                # charger l'image
                img = PIL.Image.open(chemin_image)
                self.images[nom_image] = img

        self.images["case_blanche"] = PIL.Image.new("RGB", (60, 60), "#e4edef")
        self.images["case_noire"] = PIL.Image.new("RGB", (60, 60), "#5b5b68")

        self.images["dep_poss"] = PIL.Image.open("images/dep_poss.png")


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
        width, height = 700, 600
        xmax, ymax = self.fenetre.winfo_screenwidth(), self.fenetre.winfo_screenheight()
        x0, y0 = int(xmax / 2 - width / 2), int(ymax / 2 - height / 2)
        self.fenetre.geometry(f"{width}x{height}+{x0}+{y0}")
        self.fenetre.resizable(width=False, height=False)
        self.fenetre.configure(background='#e4edef')

        # on cree d'abord les bonnes images à afficher
        img_cases = self.generer_images_echiquier()

        # on place la bonne image sur le bon bouton
        for i in range(8):
            for j in range(8):
                self.cases[i][j] = Label(self.fenetre, image = img_cases[i][j], height=60, bd=0,
                                         width=60)
                self.cases[i][j].bind("<Button-1>", partial(self.clic_btn_piece, echiquier[i][j]))
                self.cases[i][j].image = img_cases[i][j]
                self.cases[i][j].grid(row=i + 1, column=j + 1)

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

    def clic_btn_piece(self, piece, e):
        self.controller.selectionner_piece(piece)

    def generer_images_echiquier(self):
        echiquier = Echiquier.echiquier
        img_cases = [[None for x in range(8)] for y in range(8)]
        for i in range(8):
            for j in range(8):
                case_img = self.images["case_blanche"].copy() if (i + j) % 2 == 0\
                    else self.images["case_noire"].copy()

                p = Echiquier.piece_selectionne
                # on met en evidence l'ancien deplacement
                if ( Echiquier.dernier_coup is not None and (i, j) in Echiquier.dernier_coup ) or \
                        ( p is not None and (i, j) == (p.ligne, p.colonne) ):
                    # Appliquer le filtre de flou gaussien
                    blurred_image = case_img.filter(PIL.ImageFilter.GaussianBlur(radius=1))
                    # Ajouter une teinte bleue
                    blue_tint = PIL.Image.new("RGB", case_img.size, (255, 255, 0))
                    case_img = PIL.Image.blend(blurred_image, blue_tint, 0.3)

                if not isinstance(echiquier[i][j], Vide):
                    nom_image = type(echiquier[i][j]).__name__.lower() + "_" + echiquier[i][j].couleur.name.lower()
                    case_img.paste(self.images[nom_image], (0, 0), mask=self.images[nom_image])

                if Echiquier.piece_selectionne is not None and (i, j) in Echiquier.selected_piece_moves:
                        case_img.paste(self.images["dep_poss"], (0, 0), mask=self.images["dep_poss"])

                img_cases[i][j] = PIL.ImageTk.PhotoImage(case_img)

        return img_cases

    def update_frame(self):
        echiquier = Echiquier.echiquier
        img_cases = self.generer_images_echiquier()

        for i in range(8):
            for j in range(8):
                self.cases[i][j].config(image=img_cases[i][j], width=60, heigh=60)
                self.cases[i][j].bind("<Button-1>", partial(self.clic_btn_piece, echiquier[i][j]))
                self.cases[i][j].image = img_cases[i][j]

                # si les boutons sont désactivés, on les réactive
                if self.cases[i][j]['state'] == 'disabled':
                    self.cases[i][j].config(state='normal')

    def afficher_promotion(self, piece):
        for i in range(8):
            for j in range(8):
                self.cases[i][j].config(state="disabled")
                self.cases[i][j].unbind('<Button-1>')

        # création d'un canvas pour le chox de la pièce
        self.canvas = tkinter.Canvas(self.fenetre, bg="white", bd=0, highlightthickness=0, width=120, height=120)
        self.canvas.place(relx=0.5, rely=0.5, anchor="center")

        nom = ["Dame", "Fou", "Cavalier", "Tour"]
        couleur = piece.couleur.name.lower()
        imgs = [PIL.ImageTk.PhotoImage for x in range(4)]
        for i in range(4) :
            imgs[i] = PIL.ImageTk.PhotoImage(self.images[f"{nom[i].lower()}_{couleur}"])
        coord = [(0, 0), (60, 0), (0, 60), (60, 60)]
        for i in range(4):
            label = Label(self.canvas, text=nom[i], image=imgs[i], height=60, width=60)
            label.image = imgs[i]
            label.place(x=coord[i][0], y=coord[i][1])
            label.bind("<Button-1>", partial(self.controller.promotion_pion, piece, nom[i]))



    def cacher_promotion(self):
        self.canvas.destroy()

    # on affiche l'historique d'un coup deja joue
    def afficher_historique(self):
        self.update_frame()
        for i in range(8):
            for j in range(8):
                self.cases[i][j].config(state="disabled")
                self.cases[i][j].unbind('<Button-1>')

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