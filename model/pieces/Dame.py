import model.pieces.Vide
from model.Piece import Piece
from model.constantes import LIGNE_MIN, LIGNE_MAX, COLONNE_MIN, COLONNE_MAX

class Dame(Piece):
    # constructeur
    def __init__(self, coul, lin, col):
        super().__init__(coul, lin, col)

    # méthode qui retourne les déplacements possibles
    def get_all_deplacements(self, echiquier):
        deplacements = []

        # directions de la dame
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, 1), (1, 1), (1, -1), (-1, -1)]

        for dx, dy in directions:
            x, y = self.ligne + dx, self.colonne + dy
            # tant que l'on ne depasse pas les limites de l'échiquier, on continue
            while LIGNE_MIN <= x <= LIGNE_MAX and COLONNE_MIN <= y <= COLONNE_MAX:
                piece = echiquier[x][y]
                # si la case est une piece de l'echiquier
                if not isinstance(piece, model.pieces.Vide.Vide):
                    # si c'est une piece adverse on ajoute ce deplacement et on s'arrete
                    if piece.couleur != self.couleur:
                        deplacements.append((x, y))
                    # si c'est une piece alliée on s'arrete aussi
                    break
                # ici c'est une case vide donc on continue
                deplacements.append((x, y))
                x += dx
                y += dy

        return deplacements