from controller.controllerNormal import ControllerNormal
from model.EchiquierNormal import EchiquierNormal

def main():
    # on initialise le model
    EchiquierNormal.init()
    # le controller crée la vue
    controller = ControllerNormal()

    # Démarrage de l'application
    controller.run()

if __name__ == '__main__':
    main()