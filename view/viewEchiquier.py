import os
import tkinter
from functools import partial
from tkinter import messagebox, Tk, Button, Label
import PIL.Image, PIL.ImageTk, PIL.ImageFilter, PIL.ImageDraw

from model.EchiquierNormal import EchiquierNormal as Echiquier
from model.pieces.Vide import Vide
from model.constantes import *


class ViewEchiquier:
    def __init__(self, controller):
        self.controller = controller
        # les cases de l'echiquier qui sont des labels
        self.cases = [[tkinter.Label for x in range(LIGNE_MAX + 1)] for y in range(COLONNE_MAX + 1)]
        self.images = {}  # dictionnaire pour stocker les images
        # canvas pour afficher la promotion d'un pion
        self.canvas = None
        self.fenetre = Tk() # fenetre principale
        self.fenetre.protocol("WM_DELETE_WINDOW", self.close_frame) # fermer la fenetre

        # charger les images des pieces
        for nom_piece in ["pion", "tour", "cavalier", "fou", "dame", "roi"]:
            for couleur in ["blanc", "noir"]:
                nom_image = f"{nom_piece}_{couleur}"
                chemin_image = f"images/{nom_image}.png"
                # charger l'image
                img = PIL.Image.open(chemin_image)
                self.images[nom_image] = img

        # charger les images des cases
        self.images["case_blanche"] = PIL.Image.new("RGB", (TAILLE_CASE, TAILLE_CASE), CASE_BLANCHE)
        self.images["case_noire"] = PIL.Image.new("RGB", (TAILLE_CASE, TAILLE_CASE), CASE_NOIRE)

        # charger les images de l'afficage des deplacements possibles
        self.images["dep_poss"] = PIL.Image.open("images/dep_poss.png")

    # fermer la fenetre
    def close_frame(self):
        self.fenetre.quit()
        self.fenetre.destroy()
        os._exit(0)

    # initialiser la fenetre avec tous ses composants
    def init_frame(self):
        # on recupere l'echiquier
        echiquier = Echiquier.echiquier
        # ajout du titre et du logo
        self.fenetre.title("Chessito")
        logo = tkinter.PhotoImage(file="images/logo.png")
        self.fenetre.iconphoto(False, logo)

        # on centre la fenetre
        xmax, ymax = self.fenetre.winfo_screenwidth(), self.fenetre.winfo_screenheight()
        x0, y0 = int(xmax / 2 - WIDTH_WINDOW / 2), int(ymax / 2 - HEIGHT_WINDOW / 2)
        self.fenetre.geometry( f"{WIDTH_WINDOW}x{HEIGHT_WINDOW}+{x0}+{y0}" )

        # on ne peut pas redimensionner la fenetre et on change la couleur de fond
        self.fenetre.resizable(width=False, height=False)
        self.fenetre.configure(background = BG_COLOR)

        # on cree d'abord les bonnes images à afficher
        img_cases = self.generer_images_echiquier()

        # on place la bonne image sur le bon bouton
        for i in range( LIGNE_MAX + 1 ):
            for j in range( COLONNE_MAX + 1):
                self.cases[i][j] = Label(self.fenetre, image = img_cases[i][j], height=TAILLE_CASE, bd=0,
                                         width=TAILLE_CASE)
                # lorsqu'on clique sur une case, on appelle la fonction clic_btn_piece
                self.cases[i][j].bind("<Button-1>", partial(self.clic_btn_piece, echiquier[i][j]))
                # on conserve une reference vers l'image pour ne pas qu'elle soit supprimee
                self.cases[i][j].image = img_cases[i][j]
                # on place le bouton
                self.cases[i][j].grid(row=i + 1, column=j + 1)

        # les boutons pour naviguer dans l'historique
        Button(self.fenetre, text="Retour", command=self.controller.retour_deplacement,
               height=2, width=10).grid(row=9, column=3, columnspan=2, sticky="WE")
        Button(self.fenetre, text="Avancer", command=self.controller.avancer_deplacement,
               height=2, width=10).grid(row=9, column=5, columnspan=2, sticky="WE")

        # les espaces qui sont autour de l'echiquier pour centrer l'echiquier
        self.fenetre.rowconfigure(0, weight=1)
        self.fenetre.rowconfigure(10, weight=1)
        self.fenetre.columnconfigure(0, weight=1)
        self.fenetre.columnconfigure(9, weight=1)

        # pour que la fenetre soit toujours active et que le programme ne se bloque pas
        while True:
            self.fenetre.update()
            self.fenetre.update_idletasks()

    # clic sur une case
    def clic_btn_piece(self, piece, e):
        self.controller.selectionner_piece(piece)

    # fonction qui genere les images a afficher sur l'echiquier en fonction du modele
    def generer_images_echiquier(self):
        echiquier = Echiquier.echiquier
        img_cases = [[None for x in range(LIGNE_MAX + 1)] for y in range(COLONNE_MAX + 1)]
        for i in range(LIGNE_MAX + 1):
            for j in range(COLONNE_MAX + 1):
                # on recupere l'image de la couleur de la case
                case_img = self.images["case_blanche"].copy() if (i + j) % 2 == 0\
                    else self.images["case_noire"].copy()

                p = Echiquier.piece_selectionne
                # on met en evidence l'ancien deplacement
                if ( Echiquier.dernier_coup is not None and (i, j) in Echiquier.dernier_coup ) or \
                        ( p is not None and (i, j) == (p.ligne, p.colonne) ):
                    # Appliquer le filtre de flou gaussien
                    blurred_image = case_img.filter(PIL.ImageFilter.GaussianBlur(radius=1))
                    # Ajouter une teinte jaune
                    blue_tint = PIL.Image.new("RGB", (TAILLE_CASE, TAILLE_CASE), CASE_ANC_DEP)
                    case_img = PIL.Image.blend(blurred_image, blue_tint, 0.3)

                # si c'est une piece, on affiche la bonne image
                if not isinstance(echiquier[i][j], Vide):
                    nom_image = type(echiquier[i][j]).__name__.lower() + "_" + echiquier[i][j].couleur.name.lower()
                    case_img.paste(self.images[nom_image], (0, 0), mask=self.images[nom_image])

                # si une piece est selectionnee, et que la case est dans les deplacements possibles on l'affiche
                if Echiquier.piece_selectionne is not None and (i, j) in Echiquier.selected_piece_moves:
                        case_img.paste(self.images["dep_poss"], (0, 0), mask=self.images["dep_poss"])

                # apres avoir modifie l'image, on la convertit en image tkinter
                img_cases[i][j] = PIL.ImageTk.PhotoImage(case_img)

        return img_cases

    # met a jour l'affichage de l'echiquier selon le modele
    def update_frame(self):
        echiquier = Echiquier.echiquier
        # on recupere les images a afficher
        img_cases = self.generer_images_echiquier()

        # on met a jour les images des labels
        for i in range(8):
            for j in range(8):
                self.cases[i][j].config(image=img_cases[i][j], width=TAILLE_CASE, heigh=TAILLE_CASE)
                self.cases[i][j].bind("<Button-1>", partial(self.clic_btn_piece, echiquier[i][j]))
                self.cases[i][j].image = img_cases[i][j]

                # si les boutons sont désactivés, on les réactive
                if self.cases[i][j]['state'] == 'disabled':
                    self.cases[i][j].config(state='normal')

    # affichage le choix de la piece pour la promotion
    def afficher_promotion(self, piece):
        # on desactive les labels
        for i in range(8):
            for j in range(8):
                self.cases[i][j].config(state="disabled")
                self.cases[i][j].unbind('<Button-1>')

        # création d'un canvas pour le chox de la pièce
        self.canvas = tkinter.Canvas(self.fenetre, bg="white", bd=0, highlightthickness=0, width=WIDTH_CANVAS,
                                     height=HEIGHT_CANVAS)
        self.canvas.place(relx=0.5, rely=0.5, anchor="center")

        # affichage des images pour le choix dans le canvas
        nom = [Promotion.DAME, Promotion.FOU, Promotion.CAVALIER, Promotion.TOUR]
        couleur = piece.couleur.name.lower()
        coord = [(0, 0), (TAILLE_CASE, 0), (0, TAILLE_CASE), (TAILLE_CASE, TAILLE_CASE)]
        imgs = [PIL.ImageTk.PhotoImage for x in range(4)]

        # on charge les bonnes images
        for i in range(4) :
            imgs[i] = PIL.ImageTk.PhotoImage(self.images[f"{nom[i].value}_{couleur}"])

        # on affiche les images
        for i in range(4):
            label = Label(self.canvas, image=imgs[i], height=TAILLE_CASE, width=TAILLE_CASE)
            label.image = imgs[i]
            label.place(x=coord[i][0], y=coord[i][1])
            label.bind("<Button-1>", partial(self.controller.promotion_pion, piece, nom[i]))

    # apres avoir choisi la piece, on cache le canvas
    def cacher_promotion(self):
        self.canvas.destroy()
        self.canvas = None

    # on affiche l'historique d'un coup deja joue
    def afficher_historique(self):
        self.update_frame()
        # on desactive les labels
        for i in range(LIGNE_MAX + 1):
            for j in range(COLONNE_MAX + 1):
                self.cases[i][j].config(state="disabled")
                self.cases[i][j].unbind('<Button-1>')

    # on affiche la fin de partie selon le type de fin
    def afficher_fin_de_partie(self, couleur, type_fin):
        # selon le type de fin, on affiche un message different
        msg = ""
        match type_fin:
            case FinPartie.ECHEC_ET_MAT:
                msg = 'Les ' + couleur.name.lower() + 's ont gagné par echec et mat. Voulez-vous rejouer ?'
            case FinPartie.PAT:
                msg = 'Match nul par pat. Voulez-vous rejouer ?'
            case FinPartie.POSITION_MORTE:
                msg = 'Match nul par position morte. Voulez-vous rejouer ?'
            case FinPartie.REPETITION:
                msg = 'Match nul par répétition. Voulez-vous rejouer ?'

        # on demande si on veut rejouer
        msg_box = messagebox.askquestion("Fin de partion", msg, icon='question')
        if msg_box == 'yes':
            self.controller.rejouer()
        else:
            self.close_frame()