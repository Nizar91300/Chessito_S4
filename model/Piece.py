import model.Echiquier as echiq
class Piece:

    def __init__(self, coul, lin, col):
        self.couleur = coul
        self.ligne = lin
        self.colonne = col

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
    def get_deplacements_possibles(self, echiquier):
        dep_poss = self.get_all_deplacements(echiquier)
        print("before", dep_poss)
        # pour chaque deplacement possible on verifie si le roi sera en echec apres celui-ci
        for x, y in dep_poss.copy():
            echiquier_simulee = echiq.Echiquier.simuler_deplacement(echiquier, self.ligne, self.colonne, x, y)
            # on recupere le roi et on verifie si il est en echec
            roi = echiq.Echiquier.get_roi(echiquier_simulee, self.couleur)
            if roi.est_en_echec(echiquier_simulee):
                dep_poss.remove((x, y))
        print("after: ", dep_poss)
        return dep_poss

