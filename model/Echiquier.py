import copy

from model.pieces.Cavalier import Cavalier
from model.pieces.Dame import Dame
from model.pieces.Fou import Fou
from model.pieces.Pion import Pion
from model.pieces.Roi import Roi
from model.pieces.Tour import Tour
from model.pieces.Vide import Vide
from model.constantes import Color

class Echiquier:
    def __init__(self):
        self.echiquier = [
                [Tour(Color.NOIR, 0, 0),Cavalier(Color.NOIR, 0, 1),Fou(Color.NOIR, 0, 2),Dame(Color.NOIR, 0, 3),Roi(Color.NOIR, 0, 4),Fou(Color.NOIR, 0, 5),Cavalier(Color.NOIR, 0, 6),Tour(Color.NOIR, 0, 7)],
                [Pion(Color.NOIR, 1, 0),Pion(Color.NOIR, 1, 1),Pion(Color.NOIR, 1, 2),Pion(Color.NOIR, 1, 3),Pion(Color.NOIR, 1, 4),Pion(Color.NOIR, 1, 5),Pion(Color.NOIR, 1, 6),Pion(Color.NOIR, 1, 7)],
                [Vide(2, 0), Vide(2, 1), Vide(2, 2), Vide(2, 3), Vide(2, 4), Vide(2, 5), Vide(2, 6), Vide(2, 7)],
                [Vide(3, 0), Vide(3, 1), Vide(3, 2), Vide(3, 3), Vide(3, 4), Vide(3, 5), Vide(3, 6), Vide(3, 7)],
                [Vide(4, 0), Vide(4, 1), Vide(4, 2), Vide(4, 3), Vide(4, 4), Vide(4, 5), Vide(4, 6), Vide(4, 7)],
                [Vide(5, 0), Vide(5, 1), Vide(5, 2), Vide(5, 3), Vide(5, 4), Vide(5, 5), Vide(5, 6), Vide(5, 7)],
                [Pion(Color.BLANC, 6, 0),Pion(Color.BLANC, 6, 1),Pion(Color.BLANC, 6, 2),Pion(Color.BLANC, 6, 3),Pion(Color.BLANC, 6, 4),Pion(Color.BLANC, 6, 5),Pion(Color.BLANC, 6, 6),Pion(Color.BLANC, 6, 7)],
                [Tour(Color.BLANC, 7, 0),Cavalier(Color.BLANC, 7, 1),Fou(Color.BLANC, 7, 2),Dame(Color.BLANC, 7, 3),Roi(Color.BLANC, 7, 4),Fou(Color.BLANC, 7, 5),Cavalier(Color.BLANC, 7, 6),Tour(Color.BLANC, 7, 7)] ]

        self.historique = [copy.deepcopy(self.echiquier)]

    # deplacer une piece
    def deplacer(self, oldL, oldC, newL, newC):
        self.echiquier[newL][newC] = self.echiquier[oldL][oldC]
        self.echiquier[oldL][oldC] = Vide(oldL, oldC)
        # on met a jour la position de la piece deplace
        self.echiquier[newL][newC].ligne = newL
        self.echiquier[newL][newC].colonne = newC
        # on ajoute l'echiquier dans l'historique
        self.historique.append(copy.deepcopy(self.echiquier))

    # retourne le roi d'une couleur
    def get_roi(echiquier, couleur):
        for ligne in echiquier:
            for piece in ligne:
                if isinstance(piece, Roi) and piece.couleur == couleur:
                    return piece

    # simule un déplacement
    def simuler_deplacement(echiquier, oldL, oldC, newL, newC):
        echiquier_simulee = copy.deepcopy(echiquier)
        echiquier_simulee[newL][newC] = echiquier_simulee[oldL][oldC]
        echiquier_simulee[oldL][oldC] = Vide(oldL, oldC)

        # on met a jour la position de la piece deplace
        echiquier_simulee[newL][newC].ligne = newL
        echiquier_simulee[newL][newC].colonne = newC

        return echiquier_simulee

    def verifier_echec_et_mat(self, couleur):
        # pour un echec et mat, il faut que le roi soit en echec
        if not Echiquier.get_roi(self.echiquier, couleur).est_en_echec(self.echiquier):
            return False

        # et il faut il n'y ait aucun déplacement possible
        for ligne in self.echiquier:
            for piece in ligne:
                # on ne traite que les pieces de la couleur du joueur
                if isinstance(piece, Vide) or piece.couleur != couleur:
                    continue

                dep_poss = piece.get_deplacements_possibles(self.echiquier)

                # si la pièce peut se déplacer, ce n'est pas un échec et mat
                if dep_poss != []:
                    return False
        return True

    def verifier_pat(self, couleur):
           # pour un pat, il faut que le roi ne soit pas en echec
            if Echiquier.get_roi(self.echiquier, couleur).est_en_echec(self.echiquier):
                return False

            # et il faut il n'y ait aucun déplacement possible
            for ligne in self.echiquier:
                for piece in ligne:
                    # on ne traite que les pieces de la couleur du joueur
                    if isinstance(piece, Vide) or piece.couleur != couleur:
                        continue

                    dep_poss = piece.get_deplacements_possibles(self.echiquier)

                    # si la pièce peut se déplacer, ce n'est pas un pat
                    if dep_poss != []:
                        return False
            return True

    # verifier si la partie est nulle par position morte
    def verifier_position_morte(self, couleur):

        for ligne in self.echiquier:
            for piece in ligne:
                # s'il ne reste que 2 roi, c'est une position morte
                if isinstance(piece, Vide) or isinstance(piece, Roi):
                    continue

                # s'il ne reste que 2 roi et un cavalier ou un fou, c'est une position morte
                if piece.couleur == couleur and ( isinstance(piece, Cavalier) or isinstance(piece, Fou) ) :
                    continue

                # s'il y a une autre piece, ce n'est pas une position morte
                return False

        return True

    # verifier si la partie est nulle par repetition
    def verifier_repetition(self):
        if(len(self.historique) < 5):
            return False
        cpt = 0
        # on ne regarde que les 5 derniers coups
        for echiquier in self.historique[-5:]:
            if echiquier == copy.deepcopy(self.echiquier):
                cpt += 1

        if cpt >= 3:
            return True

        return False

    # retourne vrai si on est au dernier coup de l'historique, faux sinon
    def retour_deplacement(self):
        index = self.index_historique(self.echiquier)
        if(index is not None and index > 0):
            self.echiquier = self.historique[index-1]

        if self.index_historique(self.echiquier) == len(self.historique)-1:
            return True
        return False

    # retourne vrai si on est au dernier coup de l'historique, faux sinon
    def avancer_deplacement(self):
        index = self.index_historique(self.echiquier)
        if (index is not None and index < len(self.historique)-1):
            self.echiquier = self.historique[index + 1]

        if self.index_historique(self.echiquier) == len(self.historique)-1:
            return True
        return False

    def index_historique(self, e):
        for ind, hist in enumerate(self.historique):
            meme = True
            for i in range(len(hist)):
                for j in range(len(hist[i])):
                    if hist[i][j] != e[i][j]:
                        meme = False
                        break
            if meme:
                return ind
        return None