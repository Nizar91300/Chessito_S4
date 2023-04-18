from model.Piece import Piece
from model.constantes import *
from model.pieces.Vide import Vide

# classe pion qui représente un pion de jeu d'échec
class Pion(Piece):
    # valeur de deplacement du pion en fonction de sa couleur
    UP = -1
    DOWN = 1

    # constructeur
    def __init__(self, coul, lin, col):
        super().__init__(coul, lin, col)

    # méthode qui retourne les déplacements possibles
    def get_all_deplacements(self, modele):
        # si le pion est sur la premiere ou la derniere ligne alors il est promu
        if self.ligne in (LIGNE_MIN, LIGNE_MAX):
            return []

        deplacements = []
        echiquier = modele.echiquier

        # direction de déplacement du pion
        if not modele.isAi:
            direction = Pion.UP
            place_initiale = 6
        else:
            direction = Pion.UP if self.couleur == Color.BLANC else Pion.DOWN
            # place initiale du pion pour pouvoir se deplacer de 2 cases
            place_initiale = 6 if self.couleur == Color.BLANC else 1

        # si la premiere case en face est vide
        x = self.ligne + direction
        piece = echiquier[x][self.colonne]
        if isinstance( piece , Vide ):
            deplacements.append((x, self.colonne))

            # si pion sur sa place initiale et que la deuxieme case en face est vide
            x = self.ligne + (2 * direction)
            if self.ligne == place_initiale and isinstance( echiquier[x][self.colonne] , Vide):
                deplacements.append( (x, self.colonne) )

        # Vérifie les cases en diagonale
        for diag in (-1, 1):
            y = self.colonne + diag
            if COLONNE_MIN <= y <= COLONNE_MAX:
                x = self.ligne + direction
                diagonale = echiquier[x][y]
                if not isinstance(diagonale, Vide) and diagonale.couleur != self.couleur:
                    deplacements.append((x, y))

        return deplacements

    def promotion_possible(self):
        print(self.ligne in (LIGNE_MIN, LIGNE_MAX))
        return self.ligne in (LIGNE_MIN, LIGNE_MAX)