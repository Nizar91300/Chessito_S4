from controller.controller import Controller
from model.Echiquier import Echiquier

def main():
    # on initialise le model
    Echiquier.init()
    # le controller crée la vue
    controller = Controller()

    # Démarrage de l'application
    controller.run()

if __name__ == '__main__':
    main()