import PyMisc.color as clr
import os
import time


########################
# Unicode Dictionary
########################
PIECE = {
    'black' : {
        'pawn' : "\u2659",
        'knight' : "\u265E",
        'bishop' : "\u265D",
        'rook' : "\u265C",
        'queen' : "\u265B",
        'king' : "\u265A"
    },
    'white' : {
        'pawn' : "\u2659",
        'knight' : "\u2658",
        'bishop' : "\u2657",
        'rook' : "\u2656",
        'queen' : "\u2655",
        'king' : "\u2654"
    }
}

SYMBOL = {
    'empty-white' : '\u25CF',
    'empty-black' : '\u25CB'
}


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
# Text Class
########################
class Text:
    def __init__(self, text: str, color: clr.property):
        self.__text: str = text
        self.__color: clr.property = color

    # Getters
    @property
    def text(self) -> str:
        return self.__text

    @property
    def color(self) -> clr.property:
        return self.__color

    # Representation method
    def __repr__(self) -> str:
        return clr.get_colored(self.text, self.color)


########################
# Message Class
########################
class Message:
    def __init__(self, text: Text):
        self.text: list[Text] = [text]

    # Getter - length
    @property
    def length(self) -> int:
        _len: int = 0

        # Accessing each element
        for element in self.text:
            _len += len(element.text) + 1
        _len -= 1

        return _len

    # Display method
    def display(self):
        """ This method is used to display message on console """
        for text in self.text:
            print(text, end=' ')


########################
# Error Message Class
########################
class ErrorMessage(Message):
    def __init__(self, text: str):
        super().__init__(Text(
            text,
            clr.property(
                clr.foreground.bright_red(),
                None,
                [clr.style.bold()])
        ))


########################
# Heading Class
########################
class Heading:
    def __init__(self, message: Message, decorator: Text = Text('*', clr.property(clr.foreground.bright_white())), padding: int = 1):
        # Message attribute
        self.message: Message = message

        # Style Attributes
        self.__decorator: Text = decorator
        self.__padding: int = padding

    # Print line
    def printLine(self):
        length: int = self.message.length + self.__padding * 4
        for i in range(length):
            print(self.__decorator, end='')
        print()

    # Display method
    def display(self):
        """ This method overrides Message display method """
        self.printLine()

        print(self.__decorator, ' ' * self.__padding, end='', sep='')

        self.message.display()

        print(self.__decorator, ' ' * self.__padding, sep='')

        self.printLine()


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


########################
# Main Point
########################
if __name__ == '__main__':
    board = Board()     # For testing purposes
    board.clear()
    board.display()

    head: Heading = Heading(
        message=Message(Text('Heading', clr.property(clr.foreground.bright_green()))),
        decorator=Text('$', clr.property(
            clr.foreground.bright_magenta(),
            None,
            [clr.style.bold()]
        ))
    )

    head.message.text.append(Text('Test', clr.property(clr.foreground.bright_yellow())))

    head.display()
