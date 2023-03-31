from model.Echiquier import Echiquier
from model.constantes import Color
from model.pieces.Pion import Pion
from model.pieces.Vide import Vide
from view.view import View


class Controller:
    def __init__(self):
        self.view = View(self)

    # lancer l'application
    def run(self):
        self.view.init_frame()

    # affiche les deplacements de la piece selectionne
    def afficher_deplacements(self, piece):
        Echiquier.piece_selectionne = piece
        dep_poss = piece.get_deplacements_possibles(Echiquier.echiquier)
        Echiquier.selected_piece_moves = dep_poss
        self.view.update_frame()

    # cache les deplacements possibles de la piece anciennement selectionnee
    def cacher_deplacement(self):
        # on reinitialise la piece selectionnee
        Echiquier.piece_selectionne = Echiquier.selected_piece_moves = None
        self.view.update_frame()

    def deplacer(self, l, c):
        piece = Echiquier.piece_selectionne
        self.cacher_deplacement()
        Echiquier.deplacer(piece.ligne, piece.colonne, l, c)
        # si le pion est arrivé au bout de l'echiquier on affiche la promotion
        if isinstance(piece, Pion) and piece.promotion_possible():
            self.view.afficher_promotion(piece)
        else:
            self.view.update_frame()  # on met a jour la vue

    def roquer(self, l, c):
        piece = Echiquier.piece_selectionne
        self.cacher_deplacement()
        Echiquier.roquer(l, c)
        self.view.update_frame()

    # gere le click sur une piece de l'echiquier
    def selectionner_piece(self, piece):
        if Echiquier.piece_selectionne is None:
            # si on clique sur une piece du joueur actuel on affiche ses deplacements
            if not isinstance(piece, Vide) and piece.couleur == Echiquier.couleur_joueur_actuel:
                self.afficher_deplacements(piece)
            return
        # si on reclique sur la meme piece on cache les deplacements
        if piece == Echiquier.piece_selectionne:
            self.cacher_deplacement()
            return

        # si on a cliqué sur une autre piece et que le deplacement est possible
        if (piece.ligne, piece.colonne) in Echiquier.selected_piece_moves:
            if (piece.ligne, piece.colonne) in Echiquier.get_deplacement_roque():
                self.roquer(piece.ligne, piece.colonne)
            else:
                # on deplace la piece
                self.deplacer(piece.ligne, piece.colonne)
            # on change de joueur
            Echiquier.couleur_joueur_actuel = Color.NOIR if Echiquier.couleur_joueur_actuel == Color.BLANC else Color.BLANC
            # on verifie si c'est la fin de la partie
            self.verifier_fin_de_partie()
            return

        # si on clique sur une autre piece on cache les deplacements de l'ancienne piece
        self.cacher_deplacement()
        # si on clique sur une piece du joueur actuel on affiche ses deplacements
        if not isinstance(piece, Vide) and piece.couleur == Echiquier.couleur_joueur_actuel:
            self.afficher_deplacements(piece)

    # gerer la promotion d'un pion
    def promotion_pion(self, piece, type, e):
        Echiquier.promotion_pion(piece, type)
        self.view.update_frame()
        self.view.cacher_promotion()

    def verifier_fin_de_partie(self):
        # cas de l'echec et mat
        if Echiquier.verifier_echec_et_mat(Echiquier.couleur_joueur_actuel):
            coulGagnant = Color.NOIR if Echiquier.couleur_joueur_actuel == Color.BLANC else Color.BLANC
            self.view.afficher_fin_de_partie(coulGagnant, 0)
            return
        # cas du pat
        if Echiquier.verifier_pat(Echiquier.couleur_joueur_actuel):
            self.view.afficher_fin_de_partie(None, 1)
            return
        # cas position morte
        if Echiquier.verifier_position_morte(Echiquier.couleur_joueur_actuel):
            self.view.afficher_fin_de_partie(None, 2)
            return

        # cas de la repetition
        if Echiquier.verifier_repetition():
            self.view.afficher_fin_de_partie(None, 3)
            return

    def rejouer(self):
        Echiquier.init()
        Echiquier.couleur_joueur_actuel = Color.BLANC
        self.view.update_frame()

    def retour_deplacement(self):
        # on verifie si il y a une promotion en cours
        if self.view.canvas is None:
            if Echiquier.retour_deplacement():
                self.view.update_frame()
            else:
                self.view.afficher_historique()

    def avancer_deplacement(self):
        # on verifie si il y a une promotion en cours
        if self.view.canvas is None:
            if Echiquier.avancer_deplacement():
                self.view.update_frame()
            else:
                self.view.afficher_historique()
