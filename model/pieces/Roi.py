from model.Piece import Piece
from model.pieces.Vide import Vide
from model.constantes import LIGNE_MIN, LIGNE_MAX, COLONNE_MIN, COLONNE_MAX, Color


class Roi(Piece):
    # constructeur
    def __init__(self, coul, lin, col):
        kingEvalWhite = [
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
            [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
            [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
            [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0]
        ]
        if coul == Color.BLANC:
            super().__init__(coul, lin, col, 0, kingEvalWhite)
        else:
            kingEvalBlack = kingEvalWhite[::-1]
            super().__init__(coul, lin, col, 0, kingEvalBlack)

    # méthode qui retourne les déplacements possibles
    def get_all_deplacements(self, model):
        deplacements = []
        echiquier = model.echiquier

        # deplacements possibles du roi
        possible_moves = [
            (self.ligne - 1,self.colonne),
            (self.ligne - 1,self.colonne + 1),
            (self.ligne, self.colonne + 1),
            (self.ligne + 1, self.colonne + 1),
            (self.ligne + 1, self.colonne),
            (self.ligne + 1,self.colonne - 1),
            (self.ligne, self.colonne - 1),
            (self.ligne - 1, self.colonne - 1)]

        for x, y in possible_moves:

            # si la case est à l'intérieur de l'échiquier
            if LIGNE_MIN <= x <= LIGNE_MAX and COLONNE_MIN <= y <= COLONNE_MAX:
                piece = echiquier[x][y]
                # si la case est vide ou est une pièce adverse on ajoute ce déplacement
                if isinstance(piece, Vide) or piece.couleur != self.couleur:
                    deplacements.append((x, y))

        return deplacements

    def get_deplacements_possibles(self, model):
        dep = super().get_deplacements_possibles(model)
        # on ajoute le déplacement du roque
        dep.extend(model.get_deplacement_roque())
        return dep

    # méthode qui retourne si le roi est en échec ou non
    def est_en_echec(self, modele):
        for ligne in range(LIGNE_MAX+1):
            for colonne in range(COLONNE_MAX+1):
                piece = modele.echiquier[ligne][colonne]
                if not isinstance(piece, Vide) and piece.couleur != self.couleur and (self.ligne, self.colonne) in piece.get_all_deplacements(modele):
                    return True
        return False



