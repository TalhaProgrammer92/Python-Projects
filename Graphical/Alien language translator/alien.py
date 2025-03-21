import random
import string
# import unicodedata

def get_valid_unicode():
    """ Function to generate a unique unicode character """
    # Define restricted ranges
    restricted_ranges = [
        (0x0020, 0x007F),  # Basic Latin (includes a-z, A-Z, 0-9, symbols)
        (0x00A0, 0x00FF),  # Latin-1 Supplement
    ]

    while True:
        # Generate a random Unicode character
        unicode_code = random.choice(range(0x2000, 0x3000))
        unicode_char = chr(unicode_code)  # General Punctuation, Symbols


        # Check if it falls within restricted ranges
        if not any(start <= ord(unicode_char) <= end for start, end in restricted_ranges):
            return unicode_char, unicode_code
        else:
            return get_valid_unicode()

# Checks validity of a Unicode character depending on it's given code
is_valid_unicode = lambda unicode_character, unicode_code: unicode_character == chr(unicode_code)


#################
# Character
#################
class UnicodeCharacter:
    def __init__(self, character: str, code: int):
        self.__character: str = character
        self.__code: int = code

    @property
    def character(self) -> str:
        return self.__character

    @property
    def code(self) -> int:
        return self.__code

    def __repr__(self) -> str:
        return '{} {} {}'.format(self.character, self.code, is_valid_unicode(self.character, self.code))


#############################
# My custom dictionary
#############################
class UnicodeDictionary:
    def __init__(self, keyboard: UnicodeCharacter, alien: UnicodeCharacter):
        self.__keyboard: UnicodeCharacter = keyboard
        self.__alien: UnicodeCharacter = alien

    @property
    def keyboard(self) -> UnicodeCharacter:
        return self.__keyboard

    @property
    def alien(self) -> UnicodeCharacter:
        return self.__alien

    def __repr__(self) -> str:
        uniqueness = ['Not Unique', 'Unique']
        return '{} --- {} -- {}'.format(self.keyboard.__repr__(), self.alien.__repr__(), uniqueness[int(is_unique(self.__alien.character))])


############################
# Unicode Mapping
############################
# Pre-defined Tuples
keyboard_characters: tuple = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~')
keyboard_codes: tuple = (97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 58, 59, 60, 61, 62, 63, 64, 91, 92, 93, 94, 95, 96, 123, 124, 125, 126, 32)
alien_characters: tuple = ('⠮', '⼺', '⨙', '⌖', '⠽', '⊧', '⢗', '⋻', '⸶', '⪂', 'Ⳮ', '⎎', '⌊', '┘', '☶', '⣗', '⚍', '⅛', '⺉', '⧢', '⧤', '⦟', '⪠', '⠟', '⺮', '⣓', 'Ⱨ', 'ℜ', '⡉', '⺕', '∋', '⠰', '⺢', '⟣', '⣋', '⡥', '⒮', '⺹', '⍵', '⡖', '⎕', '⼯', '⡌', '⡑', '∃', '⍙', '⣶', '⧗', '✜', '⚅', '⡡', '⌘', '⼐', '⩀', 'ⵃ', '⢎', '⭯', '⽜', '⒋', '⡗', 'ⴸ', '⻓')
alien_codes: tuple = (10286, 12090, 10777, 8982, 10301, 8871, 10391, 8955, 11830, 10882, 11501, 9102, 8970, 9496, 9782, 10455, 9869, 8539, 11913, 10722, 10724, 10655, 10912, 10271, 11950, 10451, 11367, 8476, 10313, 11925, 8715, 10288, 11938, 10211, 10443, 10341, 9390, 11961, 9077, 10326, 9109, 12079, 10316, 10321, 8707, 9049, 10486, 10711, 10012, 9861, 10337, 8984, 12048, 10816, 11587, 10382, 11119, 12124, 9355, 10327, 11576, 11987)

# The empty unicode dictionary list
unicode_dictionary: list[UnicodeDictionary] = []

# Append objects to the list of unicode dictionary
limit: int = min(len(keyboard_characters), len(keyboard_codes), len(alien_characters), len(alien_codes))     # Get smallest tuple's length among above three pre-defined tuples to prevent index overflow exception.
for i in range(limit):
    unicode_dictionary.append(
        UnicodeDictionary(
            keyboard=UnicodeCharacter(
                keyboard_characters[i],
                keyboard_codes[i]
            ),
            alien=UnicodeCharacter(
                alien_characters[i],
                alien_codes[i]
            )
        )
    )

def get_alien_character(character: str) -> str:
    """ Get corresponding alien text in unicode_dictionary """
    index: int = keyboard_characters.index(character)
    return unicode_dictionary[index].alien.character

def convert_to_alien(message: str) -> str:
    """ Converts human text to alien like text """
    alien: str = ''
    for character in message:
        if character in keyboard_characters[:limit]:
            alien += get_alien_character(character)
        else:
            alien += character
    return alien

def is_unique(alien: str) -> bool:
    """ Checks if all unicode characters are unique """
    return alien_characters.count(alien) == 1

def print_unicode_dictionary():
    """ Print all members in unicode_dictionary """
    for unicode_dict in unicode_dictionary:
        print(unicode_dict)

if __name__ == '__main__':
    # for i in range(len(normal_characters)):
    #     print(normal_characters[i])
    #     for count in range(5):
    #         unicode, value = get_valid_unicode()
    #         print('>'*4, unicode, value, unicodedata.name(unicode, "Unknown Character"))
    #     print()
    print_unicode_dictionary()
    print(
        '\nDone:', limit,
        '\nLeft:', len(keyboard_characters) - limit
    )

    # print(convert_to_alien('my name is talha ahmad'))
    # print(convert_to_alien('i love to code in python'))
    # print(convert_to_alien('he loves x man series'))
    # print(convert_to_alien('The quick brown fox jumps over a lazy dog'))