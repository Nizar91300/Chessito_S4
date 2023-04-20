import model.EchiquierAtomic
from model.Piece import Piece
from model.constantes import Color, FinPartie
from model.pieces.Pion import Pion
from model.pieces.Vide import Vide
from view.viewEchiquier import ViewEchiquier as View

class ControllerNormal:
    def __init__(self, model, fenetre):
        self.view = View(self, model, fenetre)
        self.model = model
        self.nb_coups_ia = 0

    # lancer l'application
    def run(self):
        self.view.init_frame()

    # affiche les deplacements de la piece selectionne
    def afficher_deplacements(self, piece):
        self.model.piece_selectionne = piece
        dep_poss = piece.get_deplacements_possibles(self.model)
        self.model.selected_piece_moves = dep_poss
        self.view.update_frame()

    # cache les deplacements possibles de la piece anciennement selectionnee
    def cacher_deplacement(self):
        # on reinitialise la piece selectionnee
        self.model.piece_selectionne = self.model.selected_piece_moves = None
        self.view.update_frame()

    def deplacer(self, l, c):
        piece = self.model.piece_selectionne
        self.cacher_deplacement()
        self.model.deplacer(piece.ligne, piece.colonne, l, c)
        # si le pion est arrivé au bout de l'echiquier on affiche la promotion
        if isinstance(piece, Pion) and piece.promotion_possible():
            self.view.afficher_promotion(piece)
        else:
            self.view.update_frame()  # on met a jour la vue

    def roquer(self, l, c):
        self.cacher_deplacement()
        self.model.roquer(l, c)
        self.view.update_frame()

    # gere le click sur une piece de l'echiquier
    def selectionner_piece(self, piece):
        if self.model.piece_selectionne is None:
            # si on clique sur une piece du joueur actuel on affiche ses deplacements
            if not isinstance(piece, Vide) and piece.couleur == self.model.couleur_joueur_actuel:
                self.afficher_deplacements(piece)
            return
        # si on reclique sur la meme piece on cache les deplacements
        if piece == self.model.piece_selectionne:
            self.cacher_deplacement()
            return

        # si on a cliqué sur une autre piece et que le deplacement est possible
        if (piece.ligne, piece.colonne) in self.model.selected_piece_moves:
            if (piece.ligne, piece.colonne) in self.model.get_deplacement_roque():
                self.roquer(piece.ligne, piece.colonne)
            else:
                # on deplace la piece
                self.deplacer(piece.ligne, piece.colonne)

            if self.model.isAi:
                self.verifier_fin_de_partie(Color.NOIR)
                self.deplacer_AI()
                self.view.update_frame()
                self.verifier_fin_de_partie(Color.BLANC)
            else:
                self.model.couleur_joueur_actuel = Color.NOIR if self.model.couleur_joueur_actuel == Color.BLANC else Color.BLANC
                # on verifie si c'est la fin de la partie
                self.verifier_fin_de_partie(self.model.couleur_joueur_actuel)
            if isinstance(self.model, model.EchiquierAtomic.EchiquierAtomic):
                self.verifier_fin_de_partie(Color.BLANC if self.model.couleur_joueur_actuel == Color.NOIR else Color.NOIR)
            return

        # si on clique sur une autre piece on cache les deplacements de l'ancienne piece
        self.cacher_deplacement()
        # si on clique sur une piece du joueur actuel on affiche ses deplacements
        if not isinstance(piece, Vide) and piece.couleur == self.model.couleur_joueur_actuel:
            self.afficher_deplacements(piece)

    # gerer la promotion d'un pion
    def promotion_pion(self, piece, type, e):
        self.model.promotion_pion(piece, type)
        self.view.update_frame()
        self.view.cacher_promotion()

    def verifier_fin_de_partie(self, couleur):
        # cas de l'echec et mat
        if self.model.verifier_echec_et_mat(couleur):
            coulGagnant = Color.NOIR if couleur == Color.BLANC else Color.BLANC
            self.view.afficher_fin_de_partie(coulGagnant, FinPartie.ECHEC_ET_MAT)
            return
        # cas du pat
        if self.model.verifier_pat(couleur):
            self.view.afficher_fin_de_partie(None, FinPartie.PAT)
            return
        # cas position morte
        if self.model.verifier_position_morte(couleur):
            self.view.afficher_fin_de_partie(None, FinPartie.POSITION_MORTE)
            return

        # cas de la repetition
        if self.model.verifier_repetition():
            self.view.afficher_fin_de_partie(None, FinPartie.REPETITION)
            return

    def rejouer(self):
        self.model.rejouer()
        self.view.update_frame()

    def retour_deplacement(self):
        # on verifie si il y a une promotion en cours
        if self.view.canvas is None:
            if self.model.retour_deplacement():
                self.view.update_frame()
            else:
                self.view.afficher_historique()

    def avancer_deplacement(self):
        # on verifie si il y a une promotion en cours
        if self.view.canvas is None:
            if self.model.avancer_deplacement():
                self.view.update_frame()
            else:
                self.view.afficher_historique()

    def deplacer_AI(self):
        # on recupere le meilleur deplacement selon la difficulte
        if self.model.difficulte == 0:
            piece, new_row, new_col = Piece.randomOrEat(self.model)
        if self.model.difficulte == 1 or self.model.difficulte == 2:
            if self.nb_coups_ia < 8:
                piece, new_row, new_col = Piece.randomOrEat(self.model)
                self.nb_coups_ia += 1
            else:
                piece, new_row, new_col = Piece.chercheMeilleurDp(self.model)

        # Move the piece to its new location on the board
        self.model.deplacer(piece.ligne, piece.colonne, new_row, new_col)