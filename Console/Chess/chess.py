######################
# Game variables
######################
chess_pieces_dictionary: dict = {
    'black' : {
        'king' : '\u2654',
        'queen' : '\u2655',
        'rook' : '\u2656',
        'bishop' : '\u2657',
        'knight' : '\u2658',
        'pawn' : '\u2659'
    },
    'white' : {
        'king' : '\u265A',
        'queen' : '\u265B',
        'rook' : '\u265C',
        'bishop' : '\u265D',
        'knight' : '\u265E',
        'pawn' : '\u265F'
    }
}


########################
# Position - Class
########################
class Position:
    def __init__(self, row: int, column: int):
        self.row: int = row
        self.column: int = column

    def __repr__(self) -> str:
        return '({}, {})'.format(self.row, self.column)


########################
# Chess Piece - Class
########################
class ChessPiece:
    def __init__(self, name: str, group: str, initial_position: Position = Position(0, 0)):
        self.__group: str = group
        self.__name: str = name
        self.__code: str = chess_pieces_dictionary[group][name]
        self.position: Position = initial_position

    @property
    def name(self) -> str:
        return self.__name

    @property
    def code(self) -> str:
        return self.__code

    @property
    def group(self) -> str:
        return self.__group

    def change(self, name: str) -> None:
        """ Change the pawn piece to other """
        if self.__name == 'pawn' and name not in ['pawn', 'king']:
            self.__name = name
            self.__code = chess_pieces_dictionary[self.__group][name]

    def __repr__(self) -> str:
        return self.__code


########################
# Chess Board - Class
########################
class ChessBoard:
    def __init__(self):
        self.grid = [[" " for _ in range(8)] for _ in range(8)]

    def display(self):
        print("  a   b   c   d   e   f   g   h")  # Column labels
        print(" +" + "---+" * 8)  # Top border

        for i, row in enumerate(self.grid, start=1):  # Change `self.Sgrid` → `self.grid`
            print(f"{9 - i}| " + " | ".join(row) + " |")  # Row number + board row
            print(" +" + "---+" * 8)  # Row separator


########################
# Game - Class
########################
class Game:
    def __init__(self, board: ChessBoard):
        self.__chess_board: ChessBoard = board
        self.__white_pieces: list = []
        self.__black_pieces: list = []

    @property
    def board(self) -> ChessBoard:
        return self.__chess_board

    def initialize_pieces(self):
        """Initialize all chess pieces with correct starting positions and update the board"""

        # Define piece placement (row, column) based on standard chessboard
        piece_order = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]

        # Initialize white pieces
        for col, piece in enumerate(piece_order):
            piece_obj = ChessPiece(piece, "white", Position(7, col))
            self.__white_pieces.append(piece_obj)
            self.__chess_board.grid[7][col] = piece_obj.code  # Place on board

            pawn_obj = ChessPiece("pawn", "white", Position(6, col))
            self.__white_pieces.append(pawn_obj)
            self.__chess_board.grid[6][col] = pawn_obj.code  # Place pawn on board

        # Initialize black pieces
        for col, piece in enumerate(piece_order):
            piece_obj = ChessPiece(piece, "black", Position(0, col))
            self.__black_pieces.append(piece_obj)
            self.__chess_board.grid[0][col] = piece_obj.code  # Place on board

            pawn_obj = ChessPiece("pawn", "black", Position(1, col))
            self.__black_pieces.append(pawn_obj)
            self.__chess_board.grid[1][col] = pawn_obj.code  # Place pawn on board

#################
# Functions
#################
def print_all_chess_pieces() -> None:
    """ Function to display all chess pieces in a row """
    for _class in ['white', 'black']:
        print(_class.upper() + ':', end='\t')
        for piece in ['king', 'queen', 'rook', 'bishop', 'knight', 'pawn']:
            print(chess_pieces_dictionary[_class][piece], end=' ')
        print()


#################
# Testing
#################
if __name__ == '__main__':
    # print_all_chess_pieces()

    # piece = ChessPiece('pawn', 'white')
    # print(piece, piece.position)
    # piece.change('knight')
    # piece.position.row = 2
    # piece.position.column = 3
    # print(piece, piece.position)

    board = ChessBoard()
    # board.display()

    game = Game(board)
    game.initialize_pieces()
    game.board.display()
