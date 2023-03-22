from model.Piece import Piece
from model.pieces.Vide import Vide
from model.constantes import LIGNE_MIN, LIGNE_MAX, COLONNE_MIN, COLONNE_MAX

class Cavalier(Piece):
    # constructeur
    def __init__(self, coul, lin, col):
        self.couleur = coul
        self.ligne = lin
        self.colonne = col

    # méthode qui retourne les déplacements possibles
    def get_all_deplacements(self, echiquier):
        deplacements = []

        # déplacements possibles pour le cavalier
        possible_moves = [
            (self.ligne - 2, self.colonne + 1),
            (self.ligne - 2, self.colonne - 1),

            (self.ligne - 1, self.colonne + 2),
            (self.ligne + 1, self.colonne + 2),

            (self.ligne + 2, self.colonne + 1),
            (self.ligne + 2, self.colonne - 1),

            (self.ligne + 1, self.colonne - 2),
            (self.ligne - 1, self.colonne - 2)
        ]

        for x, y in possible_moves:
            # on vérifie que la case est dans les limites de l'échiquier
            if LIGNE_MIN <= x <= LIGNE_MAX and COLONNE_MIN <= y <= COLONNE_MAX:
                piece = echiquier[x][y]
                # si la case est vide ou est une pièce adverse, on ajoute ce déplacement
                if isinstance(piece, Vide) or piece.couleur != self.couleur:
                    deplacements.append((x, y))

        return deplacements