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
        'black': '\u25CF',
        'white': '\u25CB'
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
        }
    }
}
