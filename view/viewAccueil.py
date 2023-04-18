import os
import tkinter
from functools import partial
from tkinter import Tk, Button

from controller.controllerNormal import ControllerNormal
from model.EchiquierAtomic import EchiquierAtomic
from model.EchiquierNormal import EchiquierNormal
from model.constantes import *
class ViewAccueil:
    def close_frame(self):
        self.fenetre.quit()
        self.fenetre.destroy()
        os._exit(0)
    def __init__(self):
        self.fenetre = Tk() # fenetre principale
        self.fenetre.protocol("WM_DELETE_WINDOW", self.close_frame) # fermer la fenetre
        self.fenetre.title("Chessito")
        logo = tkinter.PhotoImage(file="images/logo.png")
        self.fenetre.iconphoto(False, logo)

        # on centre la fenetre
        xmax, ymax = self.fenetre.winfo_screenwidth(), self.fenetre.winfo_screenheight()
        x0, y0 = int(xmax / 2 - WIDTH_WINDOW / 2), int(ymax / 2 - HEIGHT_WINDOW / 2)
        self.fenetre.geometry(f"{WIDTH_WINDOW}x{HEIGHT_WINDOW}+{x0}+{y0}")

        # on ne peut pas redimensionner la fenetre et on change la couleur de fond
        self.fenetre.resizable(width=False, height=False)
        self.fenetre.configure(background = BG_COLOR)


        Button(self.fenetre, text="Normal", command=partial(self.change_mode, "normal")).pack()
        Button(self.fenetre, text="Atomic", command=partial(self.change_mode, "atomic")).pack()


        while True:
            self.fenetre.update()
            self.fenetre.update_idletasks()

    def change_mode(self, mode):
        self.fenetre.destroy()

        if mode == "atomic":
            controller = ControllerNormal(EchiquierAtomic(True))
        else:
            controller = ControllerNormal(EchiquierNormal(False))

        controller.run()

