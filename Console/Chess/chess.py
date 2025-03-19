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


#################
# Functions
#################
def print_all_chess_pieces() -> None:
    """ function to display all chess pieces in a row """
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
    piece = ChessPiece('pawn', 'white')
    print(piece, piece.position)
    piece.change('knight')
    piece.position.row = 2
    piece.position.column = 3
    print(piece, piece.position)
