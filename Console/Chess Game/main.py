import settings as sets
from board import Board
from ui import Heading

if __name__ == '__main__':
    board: Board = Board()
    board.display()

    print()

    head: Heading = Heading()
    head.display()
