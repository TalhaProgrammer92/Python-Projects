import PyMisc.color as clr
import os
import time
import unicode


########################
# Time Counter Class
########################
class TimeCounter:
    def __init__(self):
        self.__start = time.time()
        self.__current = None

    # Update Time
    def update(self):
        """ This method updates current time """
        self.__current = time.time()

    # Get time duration
    @property
    def duration(self):
        return self.__current - self.__start if self.__current is not None else None

########################
# Name Class
########################
class Name:
    def __init__(self, name: str, color: clr.property):
        self.__name: str = name
        self.__color: clr.property = color

    # Getter of name
    @property
    def name(self) -> str:
        return self.__name

    # Method to compare two names
    def __eq__(self, other) -> bool:
        return self.name.lower() == other.name.lower()

    # Representation method
    def __repr__(self) -> str:
        return clr.get_colored(self.__name, self.__color)


########################
# Score Class
########################
class Score:
    def __init__(self):
        self.__score: int = 0

    # Getter
    @property
    def score(self) -> int:
        return self.__score

    # Increment method
    def increaseBy(self, offset: int = 1) -> None:
        """ This method increase current score by given offset """
        if offset > 0:
            self.__score += offset

    # Reset the current score
    def reset(self) -> None:
        self.__score = 0

    # Representation method
    def __repr__(self) -> str:
        return str(self.__score)


########################
# Player Class
########################
class Player:
    def __init__(self, name: Name):
        self.name: Name = name
        self.score: Score = Score()

    # Representation method
    def __repr__(self) -> str:
        return self.name.__repr__() + '\t' + self.score.__repr__()


########################
# Position Class
########################
class Position:
    def __init__(self, row: int, column: int):
        self.__row: int = row
        self.__column: int = column

    # Getters
    @property
    def row(self) -> int:
        return self.__row

    @property
    def column(self) -> int:
        return self.__column

    # Setters
    @row.setter
    def row(self, value: int):
        self.__row = value if value >= 0 else self.row

    @column.setter
    def column(self, value: int):
        self.__column = value if value >= 0 else self.column

    # Overloaded method for subtraction
    def __sub__(self, other):
        return Position(abs(self.row - other.row), abs(self.column - other.column))

    # Representation method
    def __repr__(self) -> str:
        return f"({self.row}, {self.column})"


########################
# Symbol Class
########################
class Symbol:
    def __init__(self, unicode: str, color_property: clr.property, position: Position):
        self.unicode: str = unicode
        self.color: clr.property = color_property
        self.position: Position = position

    # Method to get empty symbol
    @staticmethod
    def getEmptyCell(position: Position):
        """ This method generates symbol object for empty board cell dynamically based on given position """
        _, __ = [unicode.SYMBOL['empty-white'], unicode.SYMBOL['empty-black']], [clr.property(clr.foreground.cyan()), clr.property(clr.foreground.blue())]

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
        for i in range(8):
            for j in range(8):
                print(self.__board[i][j], end=' ')
            print()


########################
# Main Point
########################
if __name__ == '__main__':
    board = Board()     # For testing purposes
    board.clear()
    board.display()
