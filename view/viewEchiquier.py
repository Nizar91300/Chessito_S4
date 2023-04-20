import os
import tkinter
from functools import partial
from tkinter import messagebox, Tk, Label, Frame, ttk

import PIL.Image
import PIL.ImageDraw
import PIL.ImageFilter
import PIL.ImageTk

from model.EchiquierAtomic import EchiquierAtomic
from model.constantes import *
from model.pieces.Vide import Vide


class ViewEchiquier:
    def __init__(self, controller, model, fenetre):
        self.frames_noirs = None
        self.frames_blancs = None
        self.imgs_mangees_haut = None
        self.imgs_mangees_bas = None
        self.controller = controller
        self.model = model
        # Cases de l'échiquier qui sont des labels
        self.cases = [[tkinter.Label for x in range(LIGNE_MAX + 1)] for y in range(COLONNE_MAX + 1)]
        self.images = {}  # Dictionnaire pour stocker les images
        self.canvas = None  # Canvas pour afficher la promotion d'un pion
        self.fenetre = fenetre  # Fenêtre principale
        self.load_images()

        self.fenetre.title("Partie Atomic" if isinstance(model, EchiquierAtomic)
                           else "Partie normale")


        # Charger les images des cases
        self.images["case_blanche"] = PIL.Image.new("RGB", (TAILLE_CASE, TAILLE_CASE), CASE_BLANCHE)
        self.images["case_noire"] = PIL.Image.new("RGB", (TAILLE_CASE, TAILLE_CASE), CASE_NOIRE)

        # Charger les images de l'affichage des déplacements possibles
        self.images["dep_poss"] = PIL.Image.open("images/dep_poss.png")

    # Charger les images des pieces
    def load_images(self):
        for nom_piece in ["pion", "tour", "cavalier", "fou", "dame", "roi"]:
            for couleur in ["blanc", "noir"]:
                nom_image = f"{nom_piece}_{couleur}"
                chemin_image = f"images/{nom_image}.png"
                img = PIL.Image.open(chemin_image)
                self.images[nom_image] = img

    # Initialiser la fenêtre avec tous ses composants
    def init_frame(self):
        # On récupère l'echiquier
        echiquier = self.model.echiquier
        self.fenetre.config(bg=BG_COLOR)

        # On génère les images de l'échiquier
        img_cases = self.generer_images_echiquier()

        # On place la bonne image sur le bon bouton
        for i in range(LIGNE_MAX + 1):
            for j in range(COLONNE_MAX + 1):
                # Création du label pour afficher l'image
                self.cases[i][j] = Label(self.fenetre, image=img_cases[i][j], height=TAILLE_CASE, bd=0,
                                         width=TAILLE_CASE)
                # Lorsqu'on clique sur une case, on appelle la fonction clic_btn_piece
                self.cases[i][j].bind("<Button-1>", partial(self.clic_btn_piece, echiquier[i][j]))
                # On conserve une reference vers l'image pour qu'elle ne soit pas supprimée
                self.cases[i][j].image = img_cases[i][j]
                # On place le bouton
                self.cases[i][j].grid(row=i + 1, column=j + 1)

                # Affichage des chiffres à gauche de l'échiquier
                if j == 0:
                    chiffre_label = Label(self.fenetre, text=str(LIGNE_MAX + 1 - i), font=("Helvetica", 12), fg="white")
                    chiffre_label.grid(row=i + 1, column=0, sticky="e")
                    chiffre_label.config(bg=self.fenetre.cget('bg'))

                # Affichage des lettres en bas de l'échiquier
                if i == LIGNE_MAX:
                    # 97 est le code ASCII pour 'a'
                    lettre_label = Label(self.fenetre, text=chr(97 + j), font=("Helvetica", 12), fg="white")
                    lettre_label.grid(row=LIGNE_MAX + 2, column=j + 1, sticky="n")
                    lettre_label.config(bg=self.fenetre.cget('bg'))

        # Les boutons pour naviguer dans l'historique
        bouton_retour = ttk.Button(self.fenetre, text="Retour", command=self.controller.retour_deplacement,
                                   style='styleButton.TButton', width=6)
        bouton_retour.grid(row=11, column=3, columnspan=2, sticky="WE", padx=5)

        bouton_avancer = ttk.Button(self.fenetre, text="Avancer", command=self.controller.avancer_deplacement,
                                    style='styleButton.TButton', width=6)
        bouton_avancer.grid(row=11, column=5, columnspan=2, sticky="WE", padx=5)

        for l in (0, 10):
            frame = Frame(self.fenetre, width=60, height=30, bg=BG_COLOR, bd=0)
            frame.grid(row=l, column=1)

            # Création d'une image vide
            img = PIL.ImageTk.PhotoImage(image=PIL.Image.new("RGB", (30, 30), BG_COLOR))
            lbl2 = Label(frame, image=img, bg=BG_COLOR, bd=0)
            lbl2.image = img
            lbl2.pack(side=tkinter.RIGHT)


        # les espaces qui sont autour de l'echiquier pour centrer l'echiquier
        self.fenetre.rowconfigure(0, weight=1)
        self.fenetre.rowconfigure(10, weight=1)
        self.fenetre.columnconfigure(0, weight=1)
        self.fenetre.columnconfigure(9, weight=1)

    # Clic sur une case
    def clic_btn_piece(self, piece, e):
        self.controller.selectionner_piece(piece)

    # Fonction qui génère les images à afficher sur l'échiquier en fonction du modèle
    def generer_images_echiquier(self):
        echiquier = self.model.echiquier
        img_cases = [[None for x in range(LIGNE_MAX + 1)] for y in range(COLONNE_MAX + 1)]
        for i in range(LIGNE_MAX + 1):
            for j in range(COLONNE_MAX + 1):
                # On récupère l'image de la couleur de la case
                case_img = self.images["case_blanche"].copy() if (i + j) % 2 == 0\
                    else self.images["case_noire"].copy()

                p = self.model.piece_selectionne
                # On met en surbrillance l'ancien déplacement
                if (self.model.dernier_coup is not None and (i, j) in self.model.dernier_coup ) or \
                        (p is not None and (i, j) == (p.ligne, p.colonne)):
                    # Appliquer le filtre de flou gaussien
                    blurred_image = case_img.filter(PIL.ImageFilter.GaussianBlur(radius=1))
                    # Ajouter une teinte jaune
                    blue_tint = PIL.Image.new("RGB", (TAILLE_CASE, TAILLE_CASE), CASE_ANC_DEP)
                    case_img = PIL.Image.blend(blurred_image, blue_tint, 0.3)

                # Si c'est une piece, on affiche la bonne image
                if not isinstance(echiquier[i][j], Vide):
                    nom_image = type(echiquier[i][j]).__name__.lower() + "_" + echiquier[i][j].couleur.name.lower()
                    case_img.paste(self.images[nom_image], (0, 0), mask=self.images[nom_image])

                # Si une piece est sélectionnée, et que la case est dans les déplacements possibles on l'affiche
                if self.model.piece_selectionne is not None and (i, j) in self.model.selected_piece_moves:
                        case_img.paste(self.images["dep_poss"], (0, 0), mask=self.images["dep_poss"])

                # Après avoir modifié l'image, on la convertit en image Tkinter
                img_cases[i][j] = PIL.ImageTk.PhotoImage(case_img)

        return img_cases

    # Met à jour l'affichage de l'échiquier selon le modèle
    def update_frame(self):
        echiquier = self.model.echiquier
        # On récupère les images à afficher
        img_cases = self.generer_images_echiquier()

        # On met à jour les images des labels
        for i in range(8):
            for j in range(8):
                self.cases[i][j].config(image=img_cases[i][j], width=TAILLE_CASE, heigh=TAILLE_CASE)
                self.cases[i][j].bind("<Button-1>", partial(self.clic_btn_piece, echiquier[i][j]))
                self.cases[i][j].image = img_cases[i][j]

                # Si les boutons sont désactivés, on les réactive
                if self.cases[i][j]['state'] == 'disabled':
                    self.cases[i][j].config(state='normal')

        p_mangees_haut = self.model.get_pieces_mangees_haut()
        self.imgs_mangees_haut = []

        for i in range(len(p_mangees_haut)):
            img = self.images[p_mangees_haut[i]].copy()
            img.thumbnail((30, 30), PIL.Image.ANTIALIAS)
            self.imgs_mangees_haut.append(PIL.ImageTk.PhotoImage( img))

        self.frames_blancs = []
        for i in range(0, len(p_mangees_haut), 2):
            frame = Frame(self.fenetre, width=60, height=30, bg=BG_COLOR, bd=0)
            frame.grid(row=0, column=int(i/2)+1, sticky="S")
            self.frames_blancs.append( frame )
            lbl1 = Label( frame, image= self.imgs_mangees_haut[i] , bg=BG_COLOR, bd=0)
            lbl1.pack(side=tkinter.LEFT)

            # Vérification s'il y a une deuxième image
            if i + 1 < len(p_mangees_haut):
                # Chargement de la deuxième image
                lbl2 = Label(frame, image=self.imgs_mangees_haut[i + 1], bg=BG_COLOR, bd=0)
                lbl2.pack(side=tkinter.RIGHT)
            else:
                # Création d'une image vide
                img = PIL.ImageTk.PhotoImage(image=PIL.Image.new("RGB", (30, 30), BG_COLOR))
                lbl2 = Label(frame, image=img, bg=BG_COLOR, bd=0)
                lbl2.pack(side=tkinter.RIGHT)

        # Affichage des pièces mangées blanches en bas de l'échiquier
        p_mangees_bas = self.model.get_pieces_mangees_bas()
        self.imgs_mangees_bas = []
        for i in range(len(p_mangees_bas)):
            img = self.images[p_mangees_bas[i]].copy()
            img.thumbnail((30, 30), PIL.Image.ANTIALIAS)
            self.imgs_mangees_bas.append(PIL.ImageTk.PhotoImage(img))

        self.frames_noirs = []
        for i in range(0, len(p_mangees_bas), 2):
            frame = Frame(self.fenetre, width=60, height=30, bg=BG_COLOR, bd=0)
            frame.grid(row=LIGNE_MAX+3, column=int(i / 2) + 1, sticky="N")
            self.frames_noirs.append(frame)
            lbl1 = Label(frame, image=self.imgs_mangees_bas[i], bg=BG_COLOR, bd=0)
            lbl1.pack(side=tkinter.LEFT)

            # Vérification s'il y a une deuxième image
            if i + 1 < len(p_mangees_bas):
                # Chargement de la deuxième image
                lbl2 = Label(frame, image=self.imgs_mangees_bas[i + 1], bg=BG_COLOR, bd=0)
                lbl2.pack(side=tkinter.RIGHT)
            else:
                # Création d'une image vide
                img = PIL.ImageTk.PhotoImage(image=PIL.Image.new("RGB", (30, 30), BG_COLOR))
                lbl2 = Label(frame, image=img, bg=BG_COLOR, bd=0)
                lbl2.pack(side=tkinter.RIGHT)

    # Affiche le choix de la pièce pour la promotion
    def afficher_promotion(self, piece):
        # On désactive les labels
        for i in range(8):
            for j in range(8):
                self.cases[i][j].config(state="disabled")
                self.cases[i][j].unbind('<Button-1>')

        # Création d'un canvas pour le choix de la pièce
        self.canvas = tkinter.Canvas(self.fenetre, bg="white", bd=0, highlightthickness=0, width=WIDTH_CANVAS,
                                     height=HEIGHT_CANVAS)
        self.canvas.place(relx=0.5, rely=0.5, anchor="center")

        # Affichage des images pour le choix dans le canvas
        nom = [Promotion.DAME, Promotion.FOU, Promotion.CAVALIER, Promotion.TOUR]
        couleur = piece.couleur.name.lower()
        coord = [(0, 0), (TAILLE_CASE, 0), (0, TAILLE_CASE), (TAILLE_CASE, TAILLE_CASE)]
        imgs = [PIL.ImageTk.PhotoImage for x in range(4)]

        # On charge les bonnes images
        for i in range(4):
            imgs[i] = PIL.ImageTk.PhotoImage(self.images[f"{nom[i].value}_{couleur}"])

        # on affiche les images
        for i in range(4):
            label = Label(self.canvas, image=imgs[i], height=TAILLE_CASE, width=TAILLE_CASE)
            label.image = imgs[i]
            label.place(x=coord[i][0], y=coord[i][1])
            label.bind("<Button-1>", partial(self.controller.promotion_pion, piece, nom[i]))

    # Après avoir choisi la piece, on cache le canvas
    def cacher_promotion(self):
        self.canvas.destroy()
        self.canvas = None

    # On affiche l'historique d'un coup déjà joué
    def afficher_historique(self):
        self.update_frame()
        # On désactive les labels
        for i in range(LIGNE_MAX + 1):
            for j in range(COLONNE_MAX + 1):
                self.cases[i][j].config(state="disabled")
                self.cases[i][j].unbind('<Button-1>')

    # On affiche la fin de partie selon le type de fin
    def afficher_fin_de_partie(self, couleur, type_fin):
        # Selon le type de fin, on affiche un message différent
        msg = ""
        match type_fin:
            case FinPartie.ECHEC_ET_MAT:
                msg = 'Les ' + couleur.name.lower() + 's ont gagné par échec et mat. Voulez-vous rejouer ?'
            case FinPartie.PAT:
                msg = 'Match nul par pat. Voulez-vous rejouer ?'
            case FinPartie.POSITION_MORTE:
                msg = 'Match nul par position morte. Voulez-vous rejouer ?'
            case FinPartie.REPETITION:
                msg = 'Match nul par répétition. Voulez-vous rejouer ?'

        # on demande si on veut rejouer
        msg_box = messagebox.askquestion("Fin de partie", msg, icon='question')
        if msg_box == 'yes':
            self.controller.rejouer()
        else:
            self.fenetre.destroy()
