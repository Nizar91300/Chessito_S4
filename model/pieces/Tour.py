from model.Piece import Piece
from model.pieces.Vide import Vide
from model.constantes import LIGNE_MIN, LIGNE_MAX, COLONNE_MIN, COLONNE_MAX, Color


class Tour(Piece):
    # constructeur
    def __init__(self, coul, lin, col):
        rookEvalWhite = [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0]
        ]
        if coul == Color.BLANC:
            super().__init__(coul, lin, col, 5, rookEvalWhite)
        else:
            rookEvalBlack = rookEvalWhite[::-1]
            super().__init__(coul, lin, col, 5, rookEvalBlack)

    # méthode qui retourne les déplacements possibles
    def get_all_deplacements(self, model):
        deplacements = []
        echiquier = model.echiquier

        # directions de la tour
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dx, dy in directions:
            # on test les cases dans chaque direction
            x, y = self.ligne + dx, self.colonne + dy

            # tant que l'on ne depasse pas les limites de l'échiquier, on continue
            while LIGNE_MIN <= x <= LIGNE_MAX and COLONNE_MIN <= y <= COLONNE_MAX:
                piece = echiquier[x][y]
                # si la case est une piece
                if not isinstance( piece , Vide):
                    # si c'est une piece adverse on ajoute ce deplacement et on s'arrete
                    if piece.couleur != self.couleur:
                        deplacements.append((x, y))
                    # si c'est une piece alliée on s'arrete aussi
                    break
                # ici c'est une case vide donc on continue
                deplacements.append((x, y))
                # on testera pour la case suivante
                x += dx
                y += dy

        return deplacements