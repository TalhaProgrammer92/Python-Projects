from random import shuffle, sample, randint
from string import ascii_uppercase
import json
import csv
import PyMisc.pattern as ptrn
import PyMisc.color as clr
import PyMisc.variable as var

#######################
# GLOBAL VARIABLES
#######################
SETTINGS_JSON = open('settings.json', 'r')
SETTINGS_DATA = json.load(SETTINGS_JSON)
EMPTY_BOX_CHAR: str = SETTINGS_DATA["default-box-symbol"]
PLAYER1_SYMBOL: str = SETTINGS_DATA["default-player1-symbol"]
PLAYER2_SYMBOL: str = SETTINGS_DATA["default-player2-symbol"]


###################
# Player class
###################
class Player:
    # Constructor
    def __init__(self, **kwargs):
        self.__player_count: int = randint(0, 9)
        self.__name: str = kwargs.get('name', f'PR{self.__player_count}')
        self.__score: int = kwargs.get('score', 0)
        self.__symbol: str = kwargs.get('symbol', PLAYER1_SYMBOL if self.__player_count % 2 == 0 else PLAYER2_SYMBOL)

    # Getters
    @property
    def name(self) -> str:
        return self.__name

    @property
    def score(self) -> int:
        return self.__score

    @property
    def symbol(self) -> str:
        return self.__symbol

    # Setters
    @name.setter
    def name(self, value: str):
        self.__name = value if len(value) >= 3 and value.isalpha() else f'PR{self.__player_count}'

    @symbol.setter
    def symbol(self, value: str):
        self.__symbol = value.upper() if len(value) == 1 and value.isalpha() else PLAYER1_SYMBOL if self.__player_count % 2 == 0 else PLAYER2_SYMBOL

    # Method - Update score by increment
    def updateScore(self) -> None:
        self.__score += 1

    # Method - Display Data
    def displayInfo(self) -> None:
        print(f'''Name:   {self.name}
Score:  {self.score}
Symbol: {self.symbol}''')


################
# Box class
################
class Box:
    # Constructor
    def __init__(self, symbol: str | None = None):
        self.__symbol: str = symbol if Box.isValidSymbol(symbol) else EMPTY_BOX_CHAR

    # Getter
    @property
    def symbol(self) -> str:
        return self.__symbol

    # Setter
    @symbol.setter
    def symbol(self, value: str):
        if Box.isValidSymbol(value):
            self.__symbol = value
        else:
            raise ValueError("Invalid value for symbol! It must be an uppercase alphabet.")

    # Method - Check if given symbol is valid or not
    @staticmethod
    def isValidSymbol(self, symbol: str | None = None) -> bool:
        if symbol is None: return False
        return len(symbol) == 1 and symbol.isalpha() and symbol.isupper()

    # Method - Check if the box is empty or not
    def isEmpty(self) -> bool:
        return self.symbol == EMPTY_BOX_CHAR

    # Method - Clear the box
    def clearBox(self) -> None:
        self.__symbol = EMPTY_BOX_CHAR


##################
# Board class
##################
class Board:
    # Constructor
    def __init__(self, boxes: list[Box] | None = None):
        self.__grid: ptrn.Grid = ptrn.Grid(var.size(7, 13))
        self.__box_location_map: dict[int, var.position] = {
            # Row 1
            1: var.position(1, 2),
            2: var.position(1, 6),
            3: var.position(1, 10),

            # Row 2
            4: var.position(3, 2),
            5: var.position(3, 6),
            6: var.position(3, 10),

            # Row 6
            7: var.position(5, 2),
            8: var.position(5, 6),
            9: var.position(5, 10)
        }

        # Place given boxes' symbols into the grid
        if boxes is not None:
            self.placeBoxes(boxes)

        # Testing - Draw a border to check if boxes are aligned or not
        self.__grid.draw_hollow_box(
            var.char('+'),
            var.position(0, 0),
            var.size(7, 13)
        )

    # Method - Place boxes into the grid
    def placeBoxes(self, boxes: list[Box]) -> None:
        if len(boxes) != 9:
            raise ValueError("No enough boxes! The boxes' length must be 9.")

        # Place boxes
        for i in range(9):
            self.__grid.insert_individual(
                var.char(boxes[i].symbol),
                self.__box_location_map[i + 1]
            )

    # Method - Display Grid
    def display(self) -> None:
        self.__grid.draw()

if __name__ == '__main__':
    board: Board = Board()
    board.placeBoxes([
        Box(),
        Box(),
        Box(),
        Box(),
        Box(),
        Box(),
        Box(),
        Box(),
        Box()
    ])
    board.display()

'''
OUTPUT

+++++++++++++
+ -   -   - +
+           +
+ -   -   - +
+           +
+ -   -   - +
+++++++++++++
'''