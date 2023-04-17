
class Piece:

    def __init__(self, coul, lin, col):
        self.couleur = coul
        self.ligne = lin
        self.colonne = col
        self.nb_deplacements = 0

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
            if roi.est_en_echec(echiquier_simulee):
                dep_poss.remove((x, y))
        return dep_poss

