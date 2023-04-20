from random import random

from model.constantes import Color
from model.pieces.Vide import Vide


class Piece:
    PROFONDEUR = 2
    counter = 0
    def __init__(self, coul, lin, col, val):
        self.couleur = coul
        self.ligne = lin
        self.colonne = col
        self.nb_deplacements = 0
        self.valeur = val

    # pour comparer deux pieces
    def __eq__(self, other):
        # si la classe à comparer n'est pas la meme que la classe courante
        if not isinstance(other, Piece):
            return NotImplemented

        return self.ligne == other.ligne and self.colonne == other.colonne and self.couleur == other.couleur

    # renvoie la liste des deplacements de la piece sans tenir compte des echecs
    def get_all_deplacements(self, echiquier):
        pass

    # renvoie la liste des deplacements de la piece en tenant compte des echecs
    def get_deplacements_possibles(self, model):
        dep_poss = self.get_all_deplacements(model)
        # pour chaque deplacement possible on verifie si le roi sera en echec apres celui-ci
        for x, y in dep_poss.copy():
            echiquier_simulee = model.simuler_deplacement(self.ligne, self.colonne, x, y)
            # on recupere le roi et on verifie si il est en echec
            roi = echiquier_simulee.get_roi(self.couleur)
            if roi is None or roi.est_en_echec(echiquier_simulee):
                dep_poss.remove( (x, y) )
            # on supprime l'objet echiquier_simulee
            del echiquier_simulee
        return dep_poss

    def get_deplacements_possibles_AI(self, model):
        dep_poss = self.get_all_deplacements(model)
        # for each possible move, check if it leaves the king in check
        for move in dep_poss.copy():
            echiquier_simulee = model.simuler_deplacement(self.ligne, self.colonne, move[0], move[1])
            # check if the move puts the king in check
            roi = echiquier_simulee.get_roi(self.couleur)
            if roi is None or roi.est_en_echec(echiquier_simulee):
                dep_poss.remove(move)
                # on supprime l'objet echiquier_simulee
            del echiquier_simulee
        # return the list of possible moves with the piece itself
        return [(self, move[0], move[1]) for move in dep_poss]

    @staticmethod
    def get_all_deplacements_p(model, couleur):
        all_dep_poss = []
        for ligne in model.echiquier:
            for piece in ligne:
                if not isinstance(piece, Vide) and piece.couleur == couleur:
                    # Do something with the piece instance
                    all_dep_poss += [(piece, x, y) for (p, x, y) in piece.get_deplacements_possibles_AI(model)]
                    # print(piece.couleur, piece.ligne, piece.colonne, piece.nb_deplacements)
        return all_dep_poss

    @staticmethod
    def randomOrEat(model):
        tous_dep_noires = Piece.get_all_deplacements_p(model, Color.NOIR)
        random_index = random.randint(0, len(tous_dep_noires) - 1)
        # print(tous_dep_noires)
        scoreInitial = model.scoreEchiquier()

        mv_a_faire = []
        print("Score initial: ", scoreInitial)
        for mv in tous_dep_noires:
            piece, new_row, new_col = mv[0], mv[1], mv[2]
            echiquier_simulee = model.simuler_deplacement(piece.ligne, piece.colonne, new_row, new_col)
            score = echiquier_simulee.scoreEchiquier()
            if score < scoreInitial:
                mv_a_faire.append((mv, score))

        if (len(mv_a_faire) > 0):
            print(mv_a_faire)
            lowest_score = float('inf')
            lowest_score_move = None
            for move, score in mv_a_faire:
                print("Score avant", score, lowest_score)
                if score < lowest_score:
                    print("Score après", score)
                    lowest_score = score
                    lowest_score_move = move
            return lowest_score_move
        return tous_dep_noires[random_index]

    @staticmethod
    def chercheMeilleurDp(model):
        global prochainDp
        Piece.counter = 0

        Piece.trouverDpNegaMaxAlphaBeta(model, Piece.PROFONDEUR, -1, -1000, 1000)
        print(Piece.counter)
        return prochainDp

    @staticmethod
    def trouverDpNegaMaxAlphaBeta(model, profondeur, joueur, alpha, beta):
        global prochainDp
        if profondeur == 0:
            return joueur * model.scoreEchiquier()

        if joueur == 1:
            tous_dp = Piece.get_all_deplacements_p(model, Color.BLANC)
        else:
            tous_dp = Piece.get_all_deplacements_p(model, Color.NOIR)

        maxScore = -1000
        for piece, new_row, new_col in tous_dp:
            Piece.counter += 1
            echiquier_simulee = model.simuler_deplacement(piece.ligne, piece.colonne, new_row, new_col)
            score = -Piece.trouverDpNegaMaxAlphaBeta(echiquier_simulee, profondeur - 1, -joueur, -beta, -alpha)
            if score > maxScore:
                maxScore = score
                if profondeur == Piece.PROFONDEUR:
                    prochainDp = (piece, new_row, new_col)
            del echiquier_simulee
            if maxScore > alpha:
                alpha = maxScore
            if alpha >= beta:
                break
        return maxScore