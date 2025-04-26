import settings
from board import Board
from ui import Heading

if __name__ == '__main__':
    board: Board = Board()
    board.display()

    print()

    settings.switchTheme()

    head: Heading = Heading()
    head.display()
