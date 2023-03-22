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
