######################
# Game variables
######################
chess_piece: dict = {
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


#################
# Functions
#################
def print_all_chess_pieces() -> None:
    """ function to display all chess pieces in a row """
    for _class in ['white', 'black']:
        print(_class.upper() + ':', end='\t')
        for piece in ['king', 'queen', 'rook', 'bishop', 'knight', 'pawn']:
            print(chess_piece[_class][piece], end=' ')
        print()


#################
# Testing
#################
if __name__ == '__main__':
    print_all_chess_pieces()