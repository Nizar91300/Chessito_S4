from enum import Enum

# longueur et hauteur de la fenêtre
WIDTH_WINDOW = 700
HEIGHT_WINDOW = 600

BG_COLOR = "#808080"
GRIS = '#676B6C'

# taille des cases
TAILLE_CASE = 60

# couleur case blanche et noire
CASE_BLANCHE = "#e4edef"
CASE_NOIRE = "#5b5b68"

# couleur des cases de l'ancien deplacement
CASE_ANC_DEP = (255, 255, 0)

# taille du canvas pour la promotion
WIDTH_CANVAS = TAILLE_CASE * 2
HEIGHT_CANVAS = TAILLE_CASE * 2

# valeurs minimales et maximales de la colonne
COLONNE_MIN = LIGNE_MIN = 0
COLONNE_MAX = LIGNE_MAX = 7

class Color(Enum):
    BLANC = 1
    NOIR = 2

# different piece de promotion
class Promotion(Enum):
    DAME = "dame"
    TOUR = "tour"
    FOU = "fou"
    CAVALIER = "cavalier"

# valeur pour la fin de partie
class FinPartie(Enum):
    ECHEC_ET_MAT = 1
    PAT = 2
    POSITION_MORTE = 3
    REPETITION = 4
