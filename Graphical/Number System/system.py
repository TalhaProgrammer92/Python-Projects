# Importing necessary modules
import tkinter as tk
import tkinter.messagebox as tmsg
import PyMisc.system as mac
import PyMisc.number as number
from PyMisc.variable import constant, resolution


##################
# Main Window
##################
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        ################################
        # Window properties settings
        ################################

        # Resolution / Size
        self.resolution: resolution = resolution(300, 450)
        self.geometry("{}x{}".format(self.resolution.both))
        self.minsize(self.resolution.width, self.resolution.height)
        self.maxsize(self.resolution.width, self.resolution.height)

        # Title
        self.title("Number System")

        # Variables

