from controller.controllerNormal import ControllerNormal
from model.Echiquier import Echiquier

def main():
    # on initialise le model
    Echiquier.init()
    # le controller crée la vue
    controller = ControllerNormal()

    # Démarrage de l'application
    controller.run()

if __name__ == '__main__':
    main()