import PyMisc.color as clr
import settings as sets
from utils import Position
from unicode import *

########################
# Symbol Class
########################
class Symbol:
    def __init__(self, unicode: str, color_property: clr.property, position: Position = None):
        self.unicode: str = unicode
        self.color: clr.property = color_property
        self.position: Position | None = position

    # Method to get empty symbol
    @staticmethod
    def getEmptyCell(position: Position):
        """ This method generates symbol object for empty board cell dynamically based on given position """
        _, __ = [SYMBOL['empty-white'], SYMBOL['empty-black']], [clr.property(clr.foreground.cyan()), clr.property(clr.foreground.blue())]

        index: int = (position.row + position.column) % 2

        return Symbol(_[index], __[index], position)

    # Representation Method
    def __repr__(self) -> str:
        return clr.get_colored(self.unicode, self.color)


########################
# Board Class
########################
class Board:
    def __init__(self):
        self.__board: list = []
        self.clear()

    # Method to clear board
    def clear(self) -> None:
        """ This method clears entire board """
        # If board is an empty list
        if len(self.__board) == 0:
            for i in range(8):
                row: list[Symbol] = []
                for j in range(8):
                    row.append(Symbol.getEmptyCell(Position(i, j)))
                self.__board.append(row)

        # If board is not an empty list
        else:
            for i in range(8):
                for j in range(8):
                    self.__board[i][j] = Symbol.getEmptyCell(Position(i, j))

    # Method to display board
    def display(self) -> None:
        """ This method display the entire board """
        # Variables
        gap: str = ' ' * 2

        column_separator: Symbol = Symbol('|', clr.property(clr.foreground.magenta()))
        row_seperator: Symbol = Symbol(gap + '---------------------------------', clr.property(clr.foreground.magenta()))

        num: int = 1

        # Numbers Strip - Horizontal
        print(gap, end='')

        for i in range(8):
            print(f"{gap}{Symbol(str(i + 1), clr.property(clr.foreground.yellow())).__repr__()} ", end='')

        print()

        # Display loop
        print(row_seperator)
        for row in self.__board:
            # Numbers Strip - Vertical
            print(Symbol(str(num), clr.property(clr.foreground.yellow())), column_separator, end='')

            for cell in row:
                print(" ", cell, " ", column_separator, end='', sep='')
            print('\n', row_seperator, sep='')

            num += 1