import os
import random as rand


######################
# Functions
######################
def clear_console():
    """ Clear the console / terminal screen """
    os.system('cls' if os.name == 'nt' else 'clear')

def printColored(text: str, color: str, end='') -> None:
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
    'black': '\033[30m',
    'red': '\033[31m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'blue': '\033[34m',
    'magenta': '\033[35m',
    'cyan': '\033[36m',
    'white': '\033[37m',
    'reset': '\033[0m',
    'bright-black': '\033[90m',
    'bright-red': '\033[91m',
    'bright-green': '\033[92m',
    'bright-yellow': '\033[93m',
    'bright-blue': '\033[94m',
    'bright-magenta': '\033[95m',
    'bright-cyan': '\033[96m',
    'bright-white': '\033[97m',
    }

    color = color.lower()

    if color in colors:
        print(f"{colors[color]}{text}{colors['reset']}", end=end)
    else:
        print(f"Invalid color: {color}. Available colors: {list(colors.keys())}")

def takeInput(prompt: str, valid_nums: list[int], color: str = 'white') -> int:
    """ To take valid from user """
    while True:
        try:
            printColored(prompt, color)
            num: int = int(input())
            if num in valid_nums:
                break
            else:
                printColored('Out of range!', 'red', '\n')
        except Exception:
            printColored('Invalid Input!', 'red', '\n')

    return num


######################
# Player
######################
class Player:
    def __init__(self, name: str):
        self.__name: str = name
        self.__score: int = 0
        self.__scores: list[int] = []

    @property
    def score(self) -> int:
        return self.__score

    @property
    def name(self) -> str:
        return self.__name

    def incrementScore(self) -> None:
        self.__score += 1

    def reset(self) -> None:
        """ To reset player's score """
        self.__score = 0
        self.__scores.append(self.score)

    def restart(self) -> None:
        """ To make player as fresher """
        self.__score = 0
        self.__scores = []

    def showHistory(self) -> None:
        """ Display the history of player """
        text: str = '*' * 5 + f' {self.name}\'s ' + '*' * 5
        printColored(text, 'magenta', '\n')
        for score in self.__scores:
            printColored(f'Game # {self.__scores.index(score) + 1}\'s Score is {score}', 'cyan')

    def __repr__(self) -> str:
        return f'{self.name} : {self.score}'


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
        print(' ' * 3, end='')
        for i in range(9):
            printColored(f'  {i} ', 'bright-red')
        print()

        # The Board
        for i in range(9):
            printColored(str(i), 'bright-red')            # Number - Column
            printColored(f'  |', 'bright-magenta')

            for j in range(9):
                cell: str = f' {self.__board[i][j]} '

                if self.__board[i][j] == '-':
                    printColored(cell, 'cyan')
                else:
                    if not self.__combination_found[i][j]:
                        printColored(cell, 'yellow')
                    else:
                        printColored(cell, 'bright-green')

                printColored('|', 'bright-magenta')

            print()

    def place(self, x: int, y: int, letter: str) -> None:
        """ To place a letter in specific location at x and y """
        if self.__board[x][y] == '-':
            self.__board[x][y] = letter

    def getLetter(self, i: int, j: int) -> str:
        """ To get letter located at x and y """
        return self.__board[i][j]

    def isCombinationFound(self, i: int, j: int) -> bool:
        """ Checks if there is a combination or not """
        return self.__combination_found[i][j]

    def combinationFoundAt(self, i: int, j: int) -> None:
        """ Ensures that a combination found at given location """
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
            if self.__containCombination(rows, cols):
                self.__players[self.__turn].incrementScore()

                if len(rows) == 3 and len(cols) == 3:
                    for i in range(3):
                        self.__board.combinationFoundAt(rows[i], cols[i])

                elif len(rows) == 3 and len(cols) == 1:
                    for row in rows:
                        self.__board.combinationFoundAt(row, cols[0])

                elif len(rows) == 1 and len(cols) == 3:
                    for col in cols:
                        self.__board.combinationFoundAt(rows[0], col)

                self.__turn -= 1    # To give the player an extra turn (Rule: If he completes "SOS")

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

    def __displayResult(self) -> None:
        """ To display information of all players """
        # Show board
        self.__board.display()

        # Players Information
        for player in self.__players:
            print(player, end='\n\n')

    def play(self) -> None:
        """ To play the game """
        s = ('S', 'O')

        # Game Loop
        while not self.__game_over:

            # Show board
            self.__board.display()

            # Get location
            printColored('\n' + self.__players[self.__turn].name + '\'s Turn:', 'blue', '\n')
            i: int = takeInput('Enter location for row>> ', [n for n in range(9)], 'blue')
            j: int = takeInput('Enter location for column>> ', [n for n in range(9)], 'blue')
            c: int = takeInput('1: S, 2: O (Single Digit)>> ', [1, 2], 'blue')
            board.place(i, j, s[c - 1])

            # Clear the screen
            clear_console()

            # Find Winner
            self.__checkCombination(i, j, s[c - 1])

            # Update
            self.__update()

        # Display Score of all players and the board
        self.__board.display()
        self.__displayResult()

        # Replay or else
        option: int = takeInput('\n1-Restart, 2-Replay, 3-All Scores, 4-Exit', [n + 1 for n in range(4)], 'blue')

        match option:
            # Restart Game (Start a new game)
            case 1:
                self.__board.clear()
                for player in self.__players:
                    player.restart()
                self.play()

            # Replay Game (Start next game)
            case 2:
                self.__board.clear()
                for player in self.__players:
                    player.reset()
                self.play()

            # Display all Scores
            case 3:
                for player in self.__players:
                    player.showHistory()

            case 4:
                exit()


if __name__ == '__main__':
    # Players
    p1 = Player('Talha')
    p2 = Player('Amelia')

    # Objects
    players = [p1, p2]
    board = Board()
    game = Game(board, players)

    # Start Game
    game.play()
