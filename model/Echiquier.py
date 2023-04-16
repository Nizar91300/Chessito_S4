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
class Echiquier:

    # represente le plateau de jeu avec les pieces
    echiquier = None

    # historique des echiquier
    historique_echiquier = None

    # contient le dernier coup joue
    dernier_coup = None

    # contient l'historique des coups joues
    historique_coups = None

    # pour retrouver la piece selectionnee
    piece_selectionne = selected_piece_moves = None
    couleur_joueur_actuel = Color.BLANC

    # index dans l'historique
    index_historique = 0

    # on initialise le jeu
    @staticmethod
    def init():
        Echiquier.echiquier = [
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

        Echiquier.historique_echiquier = [copy.deepcopy(Echiquier.echiquier)]

        Echiquier.dernier_coup = None

        Echiquier.historique_coups = []

        Echiquier.piece_selectionne = Echiquier.selected_piece_moves = None

        Echiquier.couleur_joueur_actuel = Color.BLANC

        Echiquier.index_historique = 0


    # deplacer une piece
    @staticmethod
    def deplacer(oldL, oldC, newL, newC):
        Echiquier.echiquier[newL][newC] = Echiquier.echiquier[oldL][oldC]
        Echiquier.echiquier[oldL][oldC] = Vide(oldL, oldC)
        # on met a jour la position de la piece deplace
        Echiquier.echiquier[newL][newC].ligne = newL
        Echiquier.echiquier[newL][newC].colonne = newC
        Echiquier.echiquier[newL][newC].nb_deplacements += 1

        #on inverse l'echiquier
        Echiquier.echiquier = Echiquier.rotation_echiquier(Echiquier.echiquier)

        # on met a jour l'historique
        Echiquier.historique_echiquier.append(copy.deepcopy(Echiquier.echiquier))
        Echiquier.dernier_coup = (7 - oldL, 7 - oldC) , (7 - newL, 7 - newC)
        Echiquier.historique_coups.append(Echiquier.dernier_coup)
        Echiquier.index_historique += 1

    # fonction pour inverser l'echiquier
    @staticmethod
    def rotation_echiquier(e):
        for i in range(4):
            for j in range(8):
                e[i][j], e[7 - i][7 - j] = e[7 - i][7 - j], e[i][j]
                e[i][j].ligne = i
                e[i][j].colonne = j
                e[7 - i][7 - j].ligne = 7 - i
                e[7 - i][7 - j].colonne = 7 - j
        return e

    # retourne le roi d'une couleur
    @staticmethod
    def get_roi(echiquier, couleur):
        for ligne in echiquier:
            for piece in ligne:
                if isinstance(piece, Roi) and piece.couleur == couleur:
                    return piece

    # simule un déplacement
    @staticmethod
    def simuler_deplacement(echiquier, oldL, oldC, newL, newC):
        echiquier_simulee = copy.deepcopy(echiquier)
        echiquier_simulee[newL][newC] = echiquier_simulee[oldL][oldC]
        echiquier_simulee[oldL][oldC] = Vide(oldL, oldC)

        # on met a jour la position de la piece deplace
        echiquier_simulee[newL][newC].ligne = newL
        echiquier_simulee[newL][newC].colonne = newC

        echiquier_simulee = Echiquier.rotation_echiquier(echiquier_simulee)

        return echiquier_simulee

    # gerer la promotion d'un pion
    @staticmethod
    def promotion_pion(piece, type):
        if type == Promotion.DAME:
            Echiquier.echiquier[piece.ligne][piece.colonne] = Dame(piece.couleur, piece.ligne, piece.colonne)
        elif type == Promotion.FOU:
            Echiquier.echiquier[piece.ligne][piece.colonne] = Fou(piece.couleur, piece.ligne, piece.colonne)
        elif type == Promotion.CAVALIER:
            Echiquier.echiquier[piece.ligne][piece.colonne] = Cavalier(piece.couleur, piece.ligne, piece.colonne)
        elif type == Promotion.TOUR:
            Echiquier.echiquier[piece.ligne][piece.colonne] = Tour(piece.couleur, piece.ligne, piece.colonne)
        # on inverse l'echiquier
        Echiquier.echiquier = Echiquier.rotation_echiquier(Echiquier.echiquier)

        Echiquier.historique_echiquier[-1] = copy.deepcopy(Echiquier.echiquier)

    # methode qui retourne une liste de coups possibles pour le roque du roi
    @staticmethod
    def get_deplacement_roque():
        e = Echiquier.echiquier
        dep = []
        roi = Echiquier.get_roi(e, Echiquier.couleur_joueur_actuel)
        if roi.nb_deplacements > 0 or roi.est_en_echec(e):
            return dep
        roque = True

        max_cases_left = 4 if roi.couleur == Color.BLANC else 3
        max_cases_right = 5 if roi.couleur == Color.BLANC else 4

        # Roque à gauche (petit roque si noir grand si blanc)
        if isinstance(e[7][0], Tour) and e[7][0].nb_deplacements == 0:
            for i in range(1, max_cases_left):
                if not isinstance(e[7][i], Vide) or e[7][i].est_en_echec(e, Echiquier.couleur_joueur_actuel):
                    roque = False
                    break
            if roque:
                dep += [(7, 0)]

        roque = True
        # Roque à droite (petit roque si blanc grand si noir)
        if isinstance(e[7][7], Tour) and e[7][7].nb_deplacements == 0:
            for i in [max_cases_right, 6]:
                if not isinstance(e[7][i], Vide) or e[7][i].est_en_echec(e, Echiquier.couleur_joueur_actuel):
                    roque = False
                    break
            if roque:
                dep += [(7, 7)]

        return dep

    # on roque
    @staticmethod
    def roquer(l, c):
        echiquier = Echiquier.echiquier
        roi = Echiquier.get_roi(echiquier, Echiquier.couleur_joueur_actuel)
        if roi.couleur == Color.BLANC:
            new_col_tour = 3 if c == 0 else 5
            new_col_roi = 2 if c == 0 else 6
        else:
            new_col_tour = 2 if c == 0 else 4
            new_col_roi = 1 if c == 0 else 5

        old_col_tour = 0 if c == 0 else 7
        old_col_roi = roi.colonne

        echiquier[l][new_col_roi] = echiquier[l][roi.colonne]
        echiquier[l][new_col_roi].colonne = new_col_roi
        echiquier[l][new_col_roi].nb_deplacements += 1

        echiquier[l][new_col_tour] = echiquier[l][old_col_tour]
        echiquier[l][new_col_tour].colonne = new_col_tour
        echiquier[l][new_col_tour].nb_deplacements += 1
        echiquier[l][old_col_tour] = Vide(l, old_col_tour)
        echiquier[l][old_col_roi] = Vide(l, old_col_roi)

        # on inverse l'echiquier
        Echiquier.echiquier = Echiquier.rotation_echiquier(Echiquier.echiquier)

        # on ajoute l'echiquier dans l'historique
        Echiquier.historique_echiquier.append(copy.deepcopy(Echiquier.echiquier))
        Echiquier.dernier_coup = (roi.ligne, 7 - old_col_roi), (roi.ligne, roi.colonne)
        Echiquier.historique_coups.append(Echiquier.dernier_coup)
        Echiquier.index_historique += 1

    @staticmethod
    def verifier_echec_et_mat(couleur):
        # pour un echec et mat, il faut que le roi soit en echec
        if not Echiquier.get_roi(Echiquier.echiquier, couleur).est_en_echec(Echiquier.echiquier):
            return False

        # et il faut il n'y ait aucun déplacement possible
        for ligne in Echiquier.echiquier:
            for piece in ligne:
                # on ne traite que les pieces de la couleur du joueur
                if isinstance(piece, Vide) or piece.couleur != couleur:
                    continue

                dep_poss = piece.get_deplacements_possibles(Echiquier.echiquier)

                # si la pièce peut se déplacer, ce n'est pas un échec et mat
                if dep_poss != []:
                    return False
        return True

    @staticmethod
    def verifier_pat( couleur):
           # pour un pat, il faut que le roi ne soit pas en echec
            if Echiquier.get_roi(Echiquier.echiquier, couleur).est_en_echec(Echiquier.echiquier):
                return False

            # et il faut il n'y ait aucun déplacement possible
            for ligne in Echiquier.echiquier:
                for piece in ligne:
                    # on ne traite que les pieces de la couleur du joueur
                    if isinstance(piece, Vide) or piece.couleur != couleur:
                        continue

                    dep_poss = piece.get_deplacements_possibles(Echiquier.echiquier)

                    # si la pièce peut se déplacer, ce n'est pas un pat
                    if dep_poss != []:
                        return False
            return True

    # verifier si la partie est nulle par position morte
    @staticmethod
    def verifier_position_morte( couleur):
        nb_cavalier = nb_fou = nb_pieces = 0
        for ligne in Echiquier.echiquier:
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
    @staticmethod
    def verifier_repetition():
        if(len(Echiquier.historique_echiquier) < 10):
            return False
        cpt = 0
        # on ne regarde que les 8 derniers coups
        for echiquier in Echiquier.historique_echiquier[-10:]:
            if echiquier == Echiquier.echiquier:
                cpt += 1
        if cpt >= 3:
            return True

        return False

    # retourne vrai si on est au dernier coup de l'historique, faux sinon
    @staticmethod
    def retour_deplacement():
        index = Echiquier.index_historique
        if index > 0:
            Echiquier.echiquier = Echiquier.historique_echiquier[index - 1]
            Echiquier.index_historique -= 1
            # si on est pas au premier coup, on met a jour le dernier coup pour pouvoir l'afficher
            if index-1 == 0:
                Echiquier.dernier_coup = None
            else:
                Echiquier.dernier_coup = Echiquier.historique_coups[index - 2]
            return False
        if index == 0 and len(Echiquier.historique_echiquier) ==1:
            return True
        return False

    # retourne vrai si on est au dernier coup de l'historique, faux sinon
    @staticmethod
    def avancer_deplacement():
        index = Echiquier.index_historique
        if index < len(Echiquier.historique_echiquier)-1:
            Echiquier.echiquier = Echiquier.historique_echiquier[index + 1]
            Echiquier.index_historique += 1
            # on met a jour le dernier coup pour pouvoir l'afficher
            Echiquier.dernier_coup = Echiquier.historique_coups[index]
            if index+1 == len(Echiquier.historique_echiquier) - 1:
                return True

        if index == len(Echiquier.historique_echiquier)-1:
            return True
        return False