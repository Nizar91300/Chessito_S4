from model.Echiquier import Echiquier
from model.constantes import Color
from model.pieces.Vide import Vide
from view.view import View


class Controller:
    def __init__(self):
        self.view = View(self)
        # pour retrouver la piece selectionnee
        self.piece_selectionne = self.selected_piece_moves = None
        self.couleur_joueur_actuel = Color.BLANC

    # lancer l'application
    def run(self):
        self.view.init_frame()

    # affiche les deplacements de la piece selectionne
    def afficher_deplacements(self, piece):
        self.piece_selectionne = piece
        dep_poss = piece.get_deplacements_possibles(Echiquier.echiquier)
        self.selected_piece_moves = dep_poss
        self.view.affiche_deplacements(dep_poss)

    # cache les deplacements possibles de la piece anciennement selectionnee
    def cacher_deplacement(self):
        self.view.cacher_deplacements(self.selected_piece_moves)
        # on reinitialise la piece selectionnee
        self.piece_selectionne = self.selected_piece_moves = None

    def deplacer(self, l, c):
        piece_selectionne = self.piece_selectionne
        self.cacher_deplacement()
        Echiquier.deplacer(piece_selectionne.ligne, piece_selectionne.colonne, l, c)
        self.view.update_frame()  # on met a jour la vue

    # gere le click sur une piece de l'echiquier
    def selectionner_piece(self, piece):
        if self.piece_selectionne is None:
            # si on clique sur une piece du joueur actuel on affiche ses deplacements
            if not isinstance(piece, Vide) and piece.couleur == self.couleur_joueur_actuel:
                self.afficher_deplacements(piece)
            return
        # si on reclique sur la meme piece on cache les deplacements
        if piece == self.piece_selectionne:
            self.cacher_deplacement()
            return

        # si on a cliqué sur une autre piece et que le deplacement ou l'attaque est possible

        if (piece.ligne, piece.colonne) in self.selected_piece_moves:
            # on deplace la piece
            self.deplacer(piece.ligne, piece.colonne)
            # on change de joueur
            self.couleur_joueur_actuel = Color.NOIR if self.couleur_joueur_actuel == Color.BLANC else Color.BLANC
            # on verifie si c'est la fin de la partie
            self.verifier_fin_de_partie()
            return

        # si on clique sur une autre piece on cache les deplacements de l'ancienne piece
        self.cacher_deplacement()
        # si on clique sur une piece du joueur actuel on affiche ses deplacements
        if not isinstance(piece, Vide) and piece.couleur == self.couleur_joueur_actuel:
            self.afficher_deplacements(piece)

    def verifier_fin_de_partie(self):
        # cas de l'echec et mat
        if Echiquier.verifier_echec_et_mat(self.couleur_joueur_actuel):
            coulGagnant = Color.NOIR if self.couleur_joueur_actuel == Color.BLANC else Color.BLANC
            self.view.afficher_fin_de_partie(coulGagnant, 0)
            return
        # cas du pat
        if Echiquier.verifier_pat(self.couleur_joueur_actuel):
            self.view.afficher_fin_de_partie(None, 1)
            return
        # cas position morte
        if Echiquier.verifier_position_morte(self.couleur_joueur_actuel):
            self.view.afficher_fin_de_partie(None, 2)
            return

        # cas de la repetition
        if Echiquier.verifier_repetition():
            self.view.afficher_fin_de_partie(None, 3)
            return

    def rejouer(self):
        Echiquier.init()
        self.couleur_joueur_actuel = Color.BLANC
        self.view.update_frame()

    def retour_deplacement(self):
        if (Echiquier.retour_deplacement()):
            self.view.update_frame()
        else:
            self.view.afficher_historique()


    def avancer_deplacement(self):
        if(Echiquier.avancer_deplacement()):
            self.view.update_frame()
        else:
            self.view.afficher_historique()
