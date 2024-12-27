import os
import random as rand


######################
# Functions
######################
def clear_console():
    """ Clear the console / terminal screen """
    os.system('cls' if os.name == 'nt' else 'clear')

def print_colored(text: str, color: str) -> None:
    """
      Prints the given text in the specified color to the console.

    Args:
    text: The text to be printed.
    color: The color to print the text in.
            Supported colors: 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white', 'reset'

    Returns:
    None
    """
    colors = {
      'red': '\033[91m',
      'green': '\033[92m',
      'yellow': '\033[93m',
      'blue': '\033[94m',
      'magenta': '\033[95m',
      'cyan': '\033[96m',
      'white': '\033[97m',
      'reset': '\033[0m'
    }

    color = color.lower()

    if color in colors:
        print(f"{colors[color]}{text}{colors['reset']}", end='')
    else:
        print(f"Invalid color: {color}. Available colors: {list(colors.keys())}")


######################
# Player
######################
class Player:
    def __init__(self, name: str):
        self.__name: str = name
        self.__score: int = 0

    @property
    def score(self) -> int:
        return self.__score

    @property
    def name(self) -> str:
        return self.__name

    def incrementScore(self) -> None:
        self.__score += 1

    def __repr__(self) -> str:
        return f'{self.__name} : {self.__score}'


######################
# Board
######################
class Board:
    def __init__(self):
        self.__board: list[list[str]] = []
        self.__combination_found: list[list[bool]] = []
        self.clear()

    def clear(self) -> None:
        """ To refill / reset the board """
        for y in range(9):
            b = []
            c = []
            for x in range(9):
                b.append('-')
                c.append(False)
            self.__board.append(b)
            self.__combination_found.append(c)

    def isFilled(self) -> bool:
        """ To check if the whole board is filled i.e. having not '-' """
        for y in range(9):
            for x in range(9):
                if self.__board[x][y] == '-':
                    return False
        return True

    def display(self) -> None:
        """ To display the board """

        # Number - Row
        print('\t', end='')
        for i in range(9):
            print_colored(f'  {i} ', 'red')
        print()

        # The Board
        for i in range(9):
            print_colored(str(i), 'red')            # Number - Column
            print_colored(f'\t|', 'magenta')

            for j in range(9):
                cell: str = f' {self.__board[i][j]} '

                if self.__board[i][j] == '-':
                    print_colored(cell, 'cyan')
                else:
                    if not self.__combination_found[i][j]:
                        print_colored(cell, 'yellow')
                    else:
                        print_colored(cell, 'green')

                print_colored('|', 'magenta')

            print()

    def place(self, x: int, y: int, letter: str) -> None:
        """ To place a letter in specific location at x and y """
        if self.__board[x][y] == '-':
            self.__board[x][y] = letter

    def getLetter(self, i: int, j: int) -> str:
        """ To get letter located at x and y """
        return self.__board[i][j]

    def isCombinationFound(self, i: int, j: int) -> bool:
        return self.__combination_found[i][j]

    def combinationFoundAt(self, i: int, j: int) -> None:
        self.__combination_found[i][j] = True


######################
# Game
######################
class Game:
    def __init__(self, board: Board, players: list[Player]):
        self.__board: Board = board

        self.__players: list[Player] = players
        rand.shuffle(self.__players)

        self.__turn: int = 0
        self.__game_over: bool = False

    def __update(self) -> None:
        """ To update the turn according to the number of players """
        if self.__turn < len(self.__players) - 1:
            self.__turn += 1
        else:
            self.__turn = 0
        self.__game_over = self.__board.isFilled()

    def __isAlreadyFound(self, rows: list[int], cols: list[int]) -> bool:
        """ Check if there is a combinations exist in past """
        result: bool = False

        if len(rows) == 3 and len(cols) == 3:
            result = self.__board.isCombinationFound(rows[0], cols[0]) and self.__board.isCombinationFound(rows[1], cols[1]) and self.__board.isCombinationFound(rows[2], cols[2])

        elif len(rows) == 3 and len(cols) == 1:
            result = self.__board.isCombinationFound(rows[0], cols[0]) and self.__board.isCombinationFound(rows[1], cols[0]) and self.__board.isCombinationFound(rows[2], cols[0])

        elif len(rows) == 1 and len(cols) == 3:
            result = self.__board.isCombinationFound(rows[0], cols[0]) and self.__board.isCombinationFound(rows[0], cols[1]) and self.__board.isCombinationFound(rows[0], cols[2])

        return result

    def __containCombination(self, rows: list[int], cols: list[int]) -> bool:
        """ To check if there is a combination at specific location """
        result: bool = False

        if len(rows) == 3 and len(cols) == 3:
            result = self.__board.getLetter(rows[0], cols[0]) == 'S' and self.__board.getLetter(rows[1], cols[1]) == 'O' and self.__board.getLetter(rows[2], cols[2]) == 'S'

        elif len(rows) == 3 and len(cols) == 1:
            result = self.__board.getLetter(rows[0], cols[0]) == 'S' and self.__board.getLetter(rows[1], cols[0]) == 'O' and self.__board.getLetter(rows[2], cols[0]) == 'S'

        elif len(rows) == 1 and len(cols) == 3:
            result = self.__board.getLetter(rows[0], cols[0]) == 'S' and self.__board.getLetter(rows[0], cols[1]) == 'O' and self.__board.getLetter(rows[0], cols[2]) == 'S'

        return result

    def __checkCombinationAt(self, rows: list[int], cols: list[int]) -> None:
        """ To check if there is a combination exist at given location """
        if not self.__isAlreadyFound(rows, cols):

            if len(rows) == 3 and len(cols) == 3:
                if self.__containCombination(rows, cols):
                    self.__players[self.__turn].incrementScore()

                    for i in range(3):
                        self.__board.combinationFoundAt(rows[i], cols[i])

            elif len(rows) == 3 and len(cols) == 1:
                if self.__containCombination(rows, cols):
                    self.__players[self.__turn].incrementScore()

                    for row in rows:
                        self.__board.combinationFoundAt(row, cols[0])

            elif len(rows) == 1 and len(cols) == 3:
                if self.__containCombination(rows, cols):
                    self.__players[self.__turn].incrementScore()

                    for col in cols:
                        self.__board.combinationFoundAt(rows[0], col)

    def __checkCombination(self, row: int, col: int, letter: str) -> None:
        """ To find a combination 'SOS' in the board and update player's score """
        if letter == 'S':
            rows = {
                0: [row, row - 1, row - 2],
                1: [row, row - 1, row - 2],
                2: [row],
                3: [row, row + 1, row + 2],
                4: [row, row + 1, row + 2],
                5: [row, row + 1, row + 2],
                6: [row],
                7: [row, row - 1, row - 2]
            }
            cols = {
                0: [col],
                1: [col, col + 1, col + 2],
                2: [col, col + 1, col + 2],
                3: [col, col + 1, col + 2],
                4: [col],
                5: [col, col - 1, col - 2],
                6: [col, col - 1, col - 2],
                7: [col, col - 1, col - 2]
            }
            for cycle in range(8):
                try:
                    self.__checkCombinationAt(rows[cycle], cols[cycle])
                except Exception:
                    pass

        elif letter == 'O':
            rows = {
                0: [row + 1, row, row - 1],
                1: [row + 1, row, row - 1],
                2: [row],
                3: [row - 1, row, row + 1],
            }
            cols = {
                0: [col],
                1: [col - 1, col, col + 1],
                2: [col - 1, col, col + 1],
                3: [col - 1, col, col + 1]
            }
            for cycle in range(4):
                try:
                    self.__checkCombinationAt(rows[cycle], cols[cycle])
                except Exception:
                    pass

    def __players_info(self) -> None:
        """ To display information of all players """
        for player in self.__players:
            print(player, end='\n\n')

    def __take_input(self, prompt: str) -> int:
        """ To take valid from user """
        while True:
            try:
                coor: int = int(input(prompt))
                if 0 <= coor <= 8:
                    break
                else:
                    print('Invalid Input!')
            except Exception:
                print('Invalid Input!')

        return coor

    def play(self) -> None:
        """ To play the game """
        s = ('S', 'O')

        # Game Loop
        while not self.__game_over:
            # Clear the screen
            clear_console()

            # Show board
            self.__board.display()

            # Get location
            print(self.__players[self.__turn].name + '\'s Turn:')
            i: int = self.__take_input('Enter location for row>> ')
            j: int = self.__take_input('Enter location for column>> ')
            c: int = self.__take_input('Even: S, Odd: O (Single Digit)>> ')
            board.place(i, j, s[c % 2])

            # Find Winner
            self.__checkCombination(i, j, s[c % 2])

            # Update
            self.__update()

        # Display Score of all players and the board
        self.__board.display()
        self.__players_info()

        # Hold the screen
        a = input('\nPress \'Enter\' to exit...')


if __name__ == '__main__':
    # Players
    p1 = Player('Talha')
    p2 = Player('Raza')

    # Objects
    players = [p1, p2]
    board = Board()
    game = Game(board, players)

    # Start Game
    game.play()
