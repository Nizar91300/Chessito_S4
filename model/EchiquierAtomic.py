import copy

from model.EchiquierNormal import EchiquierNormal
from model.pieces.Vide import Vide


class EchiquierAtomic(EchiquierNormal):
    def __init__(self, isAi, *args):
        super().__init__(isAi, *args)

    # fonction pour la suppression de l'objet
    def __del__(self):
        super().__del__()

    def deplacer(self, oldL, oldC, newL, newC):
        e = self.echiquier

        # si on mange un pion on detruit tout atour les autre pions
        if not isinstance(e[newL][newC], Vide) and e[newL][newC].couleur != e[oldL][oldC].couleur:
            e[oldL][oldC] = Vide(oldL, oldC)
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if 0 <= newL + i <= 7 and 0 <= newC + j <= 7:
                        self.echiquier[newL + i][newC + j] = Vide(newL + i, newC + j)

            # on verifie si on doit retourner l'echiquier
            if not self.isAi:
                self.rotation_echiquier()

                # on met a jour l'historique
                self.historique_echiquier.append(copy.deepcopy(self.echiquier))
                self.dernier_coup = (7 - oldL, 7 - oldC), (7 - newL, 7 - newC)
            else:
                # on met a jour l'historique
                self.historique_echiquier.append(copy.deepcopy(self.echiquier))
                self.dernier_coup = (oldL, oldC), (newL, newC)

            self.historique_coups.append(self.dernier_coup)
            self.index_historique += 1
        else:
            super().deplacer(oldL, oldC, newL, newC)

    # simule un déplacement
    def simuler_deplacement(self, oldL, oldC, newL, newC):
        echiquier_simulee = EchiquierAtomic(self.isAi, copy.deepcopy(self.echiquier))
        echiquier_simulee.deplacer(oldL, oldC, newL, newC)

        return echiquier_simulee

    def verifier_echec_et_mat(self, couleur):
        if self.get_roi(couleur) is None:
            return True
        return super().verifier_echec_et_mat(couleur)



