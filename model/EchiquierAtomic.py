import copy

from model.EchiquierNormal import EchiquierNormal
from model.pieces.Vide import Vide
class EchiquierAtomic(EchiquierNormal):
    @staticmethod
    def deplacer(oldL, oldC, newL, newC):
        e = EchiquierAtomic.echiquier
        # si on mange un pion on detruit tout atour les autre pions
        if not isinstance(e[newL][newC], Vide) and e[newL][newC].couleur != e[oldL][oldC].couleur:
            e[oldL][oldC] = Vide(oldL, oldC)
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if 0 <= newL + i <= 7 and 0 <= newC + j <= 7:
                        EchiquierAtomic.echiquier[newL + i][newC + j] = Vide(newL + i, newC + j)

            # on inverse l'echiquier
            EchiquierAtomic.echiquier = EchiquierAtomic.rotation_echiquier(EchiquierAtomic.echiquier)

            # on met a jour l'historique
            EchiquierAtomic.historique_echiquier.append(copy.deepcopy(EchiquierAtomic.echiquier))
            EchiquierAtomic.dernier_coup = (7 - oldL, 7 - oldC), (7 - newL, 7 - newC)
            EchiquierAtomic.historique_coups.append(EchiquierAtomic.dernier_coup)
            EchiquierAtomic.index_historique += 1
        else:
            EchiquierNormal.deplacer(oldL, oldC, newL, newC)



