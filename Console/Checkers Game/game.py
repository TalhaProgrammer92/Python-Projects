from PyMisc.variable import position
import PyMisc.color as color
import sqlite3 as sq
import time

###############
# Settings
###############
settings: dict = {
    # Pieces
    'piece': {
        'black': '\u25CF',  # ●
        'white': '\u25CB'   # ○
    },

    # Color Properties
    'color': {
        # Pieces
        'piece': {
            'black': color.property(color.foreground.red()),
            'white': color.property(color.foreground.blue())
        },

        # Cells - Board
        'cell': {
            'black': color.property(color.foreground.magenta()),
            'white': color.property(color.foreground.cyan())
        },

        # Separator - Board
        'separator': {
            'row': color.property(color.foreground.yellow()),
            'column': color.property(color.foreground.yellow())
        }
    },

    # Board
    'board': {
        'size': 8,
        'separator': {
            'row': '-' * 11,     # size + 3 => 8 + 3 = 11
            'column': '|'
        },
        'cell': {
            'black': '.',
            'white': '*'
        }
    }
}


##################
# Piece Class
##################
class Piece:
    # Constructor
    def __init__(self, _symbol: str, _color: color.property, _position: position):
        self.__symbol = _symbol
        self.__color = _color
        self.__special: bool = False
        self.position: position = _position

    # Getters
    @property
    def symbol(self) -> str:
        return self.__symbol

    @property
    def color(self) -> color.property:
        return self.__color

    @property
    def special(self) -> bool:
        return self.__special

    # Make the piece special
    def make_special(self) -> None:
        """ Make the piece special i.e. 4 directional """
        self.__special = True
        self.__color.add_style(color.style.bold())


#################
# Cell Class
#################
class Cell:
    def __init__(self, piece: Piece = None):
        pass
