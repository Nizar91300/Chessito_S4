import copy

from model.pieces.Cavalier import Cavalier
from model.pieces.Dame import Dame
from model.pieces.Fou import Fou
from model.pieces.Pion import Pion
from model.pieces.Roi import Roi
from model.pieces.Tour import Tour
from model.pieces.Vide import Vide
from model.constantes import Color, Promotion


# classe qui contine les attributs statiques du modele
class EchiquierNormal:
    def __init__(self, isAI, *args):
        # si on donne un echiquier en parametre on l'utilise sinon on cree un echiquier normal
        if len(args) == 0:
            self.echiquier = [
                [Tour(Color.NOIR, 0, 0), Cavalier(Color.NOIR, 0, 1), Fou(Color.NOIR, 0, 2), Dame(Color.NOIR, 0, 3),
                 Roi(Color.NOIR, 0, 4), Fou(Color.NOIR, 0, 5), Cavalier(Color.NOIR, 0, 6), Tour(Color.NOIR, 0, 7)],
                [Pion(Color.NOIR, 1, 0), Pion(Color.NOIR, 1, 1), Pion(Color.NOIR, 1, 2), Pion(Color.NOIR, 1, 3),
                 Pion(Color.NOIR, 1, 4), Pion(Color.NOIR, 1, 5), Pion(Color.NOIR, 1, 6), Pion(Color.NOIR, 1, 7)],
                [Vide(2, 0), Vide(2, 1), Vide(2, 2), Vide(2, 3), Vide(2, 4), Vide(2, 5), Vide(2, 6), Vide(2, 7)],
                [Vide(3, 0), Vide(3, 1), Vide(3, 2), Vide(3, 3), Vide(3, 4), Vide(3, 5), Vide(3, 6), Vide(3, 7)],
                [Vide(4, 0), Vide(4, 1), Vide(4, 2), Vide(4, 3), Vide(4, 4), Vide(4, 5), Vide(4, 6), Vide(4, 7)],
                [Vide(5, 0), Vide(5, 1), Vide(5, 2), Vide(5, 3), Vide(5, 4), Vide(5, 5), Vide(5, 6), Vide(5, 7)],
                [Pion(Color.BLANC, 6, 0), Pion(Color.BLANC, 6, 1), Pion(Color.BLANC, 6, 2), Pion(Color.BLANC, 6, 3),
                 Pion(Color.BLANC, 6, 4), Pion(Color.BLANC, 6, 5), Pion(Color.BLANC, 6, 6), Pion(Color.BLANC, 6, 7)],
                [Tour(Color.BLANC, 7, 0), Cavalier(Color.BLANC, 7, 1), Fou(Color.BLANC, 7, 2), Dame(Color.BLANC, 7, 3),
                 Roi(Color.BLANC, 7, 4), Fou(Color.BLANC, 7, 5), Cavalier(Color.BLANC, 7, 6), Tour(Color.BLANC, 7, 7)]]
        else:
            self.echiquier = args[0]

        self.historique_echiquier = [self.echiquier]
        self.dernier_coup = None
        self.historique_coups = []
        self.piece_selectionne = self.selected_piece_moves = None
        self.couleur_joueur_actuel = Color.BLANC
        self.index_historique = 0
        self.isAi = isAI

    # fonction pour la suppression de l'objet
    def __del__(self):
        del self.echiquier
        del self.historique_echiquier
        del self.dernier_coup
        del self.historique_coups
        del self.piece_selectionne
        del self.selected_piece_moves
        del self.couleur_joueur_actuel
        del self.index_historique

    # deplacer une piece
    def deplacer(self, oldL, oldC, newL, newC):
        self.echiquier[newL][newC] = self.echiquier[oldL][oldC]
        self.echiquier[oldL][oldC] = Vide(oldL, oldC)
        # on met a jour la position de la piece deplace
        self.echiquier[newL][newC].ligne = newL
        self.echiquier[newL][newC].colonne = newC
        self.echiquier[newL][newC].nb_deplacements += 1

        # on verifie si on doit retourner l'echiquier
        if self.isAi:
            self.rotation_echiquier()

            # on met a jour l'historique
            self.historique_echiquier.append(copy.deepcopy(self.echiquier))
            self.dernier_coup = (7 - oldL, 7 - oldC) , (7 - newL, 7 - newC)
        else:
            # on met a jour l'historique
            self.historique_echiquier.append(copy.deepcopy(self.echiquier))
            self.dernier_coup = (oldL, oldC), (newL, newC)

        self.historique_coups.append(self.dernier_coup)
        self.index_historique += 1


    # fonction pour inverser l'echiquier
    def rotation_echiquier(self):
        for i in range(4):
            for j in range(8):
                self.echiquier[i][j], self.echiquier[7 - i][7 - j] = self.echiquier[7 - i][7 - j], self.echiquier[i][j]
                self.echiquier[i][j].ligne = i
                self.echiquier[i][j].colonne = j
                self.echiquier[7 - i][7 - j].ligne = 7 - i
                self.echiquier[7 - i][7 - j].colonne = 7 - j

    # retourne le roi d'une couleur
    def get_roi(self, couleur):
        for ligne in self.echiquier:
            for piece in ligne:
                if isinstance(piece, Roi) and piece.couleur == couleur:
                    return piece

    # simule un déplacement
    def simuler_deplacement(self, oldL, oldC, newL, newC):
        echiquier_simulee = EchiquierNormal(self.isAi, copy.deepcopy(self.echiquier))
        echiquier_simulee.deplacer(oldL, oldC, newL, newC)

        return echiquier_simulee

    # gerer la promotion d'un pion
    def promotion_pion(self,piece, type):
        if type == Promotion.DAME:
            self.echiquier[piece.ligne][piece.colonne] = Dame(piece.couleur, piece.ligne, piece.colonne)
        elif type == Promotion.FOU:
            self.echiquier[piece.ligne][piece.colonne] = Fou(piece.couleur, piece.ligne, piece.colonne)
        elif type == Promotion.CAVALIER:
            self.echiquier[piece.ligne][piece.colonne] = Cavalier(piece.couleur, piece.ligne, piece.colonne)
        elif type == Promotion.TOUR:
            self.echiquier[piece.ligne][piece.colonne] = Tour(piece.couleur, piece.ligne, piece.colonne)

        # on inverse l'echiquier
        if self.isAi:
            self.rotation_echiquier()

        self.historique_echiquier[-1] = copy.deepcopy(self.echiquier)

    # methode qui retourne une liste de coups possibles pour le roque du roi
    def get_deplacement_roque(self):
        dep = []
        roi = self.get_roi(self.couleur_joueur_actuel)
        if roi.nb_deplacements > 0 or roi.est_en_echec(self):
            return dep
        roque = True

        max_cases_left = 4 if roi.couleur == Color.BLANC else 3
        max_cases_right = 5 if roi.couleur == Color.BLANC else 4

        # Roque à gauche (petit roque si noir grand si blanc)
        if isinstance(self.echiquier[7][0], Tour) and self.echiquier[7][0].nb_deplacements == 0:
            for i in range(1, max_cases_left):
                if not isinstance(self.echiquier[7][i], Vide) or self.echiquier[7][i].est_en_echec(self, self.couleur_joueur_actuel):
                    roque = False
                    break
            if roque:
                dep += [(7, 0)]

        roque = True
        # Roque à droite (petit roque si blanc grand si noir)
        if isinstance(self.echiquier[7][7], Tour) and self.echiquier[7][7].nb_deplacements == 0:
            for i in [max_cases_right, 6]:
                if not isinstance(self.echiquier[7][i], Vide) or self.echiquier[7][i].est_en_echec(self, self.couleur_joueur_actuel):
                    roque = False
                    break
            if roque:
                dep += [(7, 7)]

        return dep

    # on roque
    def roquer(self, l, c):
        roi = self.get_roi(self.couleur_joueur_actuel)
        if roi.couleur == Color.BLANC:
            new_col_tour = 3 if c == 0 else 5
            new_col_roi = 2 if c == 0 else 6
        else:
            new_col_tour = 2 if c == 0 else 4
            new_col_roi = 1 if c == 0 else 5

        old_col_tour = 0 if c == 0 else 7
        old_col_roi = roi.colonne

        self.echiquier[l][new_col_roi] = self.echiquier[l][roi.colonne]
        self.echiquier[l][new_col_roi].colonne = new_col_roi
        self.echiquier[l][new_col_roi].nb_deplacements += 1

        self.echiquier[l][new_col_tour] = self.echiquier[l][old_col_tour]
        self.echiquier[l][new_col_tour].colonne = new_col_tour
        self.echiquier[l][new_col_tour].nb_deplacements += 1
        self.echiquier[l][old_col_tour] = Vide(l, old_col_tour)
        self.echiquier[l][old_col_roi] = Vide(l, old_col_roi)

        # on inverse l'echiquier
        if self.isAi:
            self.rotation_echiquier()

            # on ajoute l'echiquier dans l'historique
            self.historique_echiquier.append(copy.deepcopy(self.echiquier))
            self.dernier_coup = (roi.ligne, 7 - old_col_roi), (roi.ligne, roi.colonne)
        else:
            self.historique_echiquier.append(copy.deepcopy(self.echiquier))
            self.dernier_coup = (roi.ligne, old_col_roi), (roi.ligne, roi.colonne)

        self.historique_coups.append(self.dernier_coup)
        self.index_historique += 1


    def verifier_echec_et_mat(self, couleur):
        # pour un echec et mat, il faut que le roi soit en echec
        if not self.get_roi(couleur).est_en_echec(self):
            return False

        # et il faut il n'y ait aucun déplacement possible
        for ligne in self.echiquier:
            for piece in ligne:
                # on ne traite que les pieces de la couleur du joueur
                if isinstance(piece, Vide) or piece.couleur != couleur:
                    continue

                dep_poss = piece.get_deplacements_possibles(self)

                # si la pièce peut se déplacer, ce n'est pas un échec et mat
                if dep_poss != []:
                    return False
        return True


    def verifier_pat(self, couleur):
           # pour un pat, il faut que le roi ne soit pas en echec
            if self.get_roi(couleur).est_en_echec(self):
                return False

            # et il faut il n'y ait aucun déplacement possible
            for ligne in self.echiquier:
                for piece in ligne:
                    # on ne traite que les pieces de la couleur du joueur
                    if isinstance(piece, Vide) or piece.couleur != couleur:
                        continue

                    dep_poss = piece.get_deplacements_possibles(self)

                    # si la pièce peut se déplacer, ce n'est pas un pat
                    if dep_poss != []:
                        return False
            return True

    # verifier si la partie est nulle par position morte

    def verifier_position_morte(self, couleur):
        nb_cavalier = nb_fou = nb_pieces = 0
        for ligne in self.echiquier:
            for piece in ligne:
                # on compte le nombre de cavalier et de fou
                if not isinstance(piece, Vide) and piece.couleur == couleur:
                    if isinstance(piece, Cavalier) :
                        nb_cavalier += 1
                    if isinstance(piece, Fou):
                        nb_fou += 1

                    nb_pieces+=1


        if nb_pieces == 1:
            return True
        # si il y a 1 seule cavaliers ou 1 seule fou separement, la partie est nulle
        if nb_pieces == 2 and ( (nb_cavalier == 1 and nb_fou==0 ) or (nb_fou == 1 and nb_cavalier==0) ):
            return True

        return False

    # verifier si la partie est nulle par repetition

    def verifier_repetition(self):
        if(len(self.historique_echiquier) < 10):
            return False
        cpt = 0
        # on ne regarde que les 8 derniers coups
        for echiquier in self.historique_echiquier[-10:]:
            if echiquier == self.echiquier:
                cpt += 1
        if cpt >= 3:
            return True

        return False

    # retourne vrai si on est au dernier coup de l'historique, faux sinon

    def retour_deplacement(self):
        index = self.index_historique
        if index > 0:
            self.echiquier = self.historique_echiquier[index - 1]
            self.index_historique -= 1
            # si on est pas au premier coup, on met a jour le dernier coup pour pouvoir l'afficher
            if index-1 == 0:
                self.dernier_coup = None
            else:
                self.dernier_coup = self.historique_coups[index - 2]
            return False
        if index == 0 and len(self.historique_echiquier) ==1:
            return True
        return False

    # retourne vrai si on est au dernier coup de l'historique, faux sinon

    def avancer_deplacement(self):
        index = self.index_historique
        if index < len(self.historique_echiquier)-1:
            self.echiquier = self.historique_echiquier[index + 1]
            self.index_historique += 1
            # on met a jour le dernier coup pour pouvoir l'afficher
            self.dernier_coup = self.historique_coups[index]
            if index+1 == len(self.historique_echiquier) - 1:
                return True

        if index == len(self.historique_echiquier)-1:
            return True
        return False