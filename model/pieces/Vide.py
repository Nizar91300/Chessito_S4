from model.constantes import *

# classe vide qui représente une case vide de l'echiquier
class Vide:

    # constructeur
    def __init__(self, lin, col):
        self.ligne = lin
        self.colonne = col

    # pour comparer deux cases vides
    def __eq__(self, other):
        # si la classe à comparer n'est pas la meme que la classe courante
        if not isinstance(other, Vide):
            return NotImplemented

        return self.ligne == other.ligne and self.colonne == other.colonne

    # méthode qui retourne si le roi est en échec ou non
    def est_en_echec(self, modele, couleur):
        for ligne in range(LIGNE_MAX+1):
            for colonne in range(COLONNE_MAX+1):
                piece = modele.echiquier[ligne][colonne]
                if not isinstance(piece, Vide) and piece.couleur != couleur and (self.ligne, self.colonne) in piece.get_all_deplacements(modele):
                    return True
        return False
