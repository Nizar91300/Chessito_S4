from controller.controller import Controller
from model.Echiquier import Echiquier

def main():
    # Création du model et du controller
    model = Echiquier()
    # le controller crée la vue
    controller = Controller(model)

    # Démarrage de l'application
    controller.run()

if __name__ == '__main__':
    main()