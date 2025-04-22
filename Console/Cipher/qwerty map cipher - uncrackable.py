from random import randint

keys: dict[str, list[str]] = {
    'row-0' : ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+'],

    'row-1' : ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '{', '}', '|'],

    'row-2' : ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', '"'],

    'row-3' : ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', '>', '?']
}

def getKeysList(key: str, shift: int) -> list[str]:
    """ Function to get related list from keys dictionary """
    _list: list[str] = [key]

    for i in range(len(keys)):
        if key in keys[f'row-{i}']:
            _list = keys[f'row-{i}']

    return _list, randint(1, len(keys)) + abs(shift)

class Parser:
    def __init__(self, key: str, shift: int):
        self.__key: str = key
        self.__keys_list, self.__shift = getKeysList(key, shift)

        self.__key_parsed: str = self._parse()

    @property
    def key_parsed(self) -> str:
        return self.__key_parsed

    def _parse(self) -> str:
        """ Method to parse key with shift for encoding/decoding """
        # Local Variables
        key: str = self.__key
        pointer: int = self.__keys_list.index(key)

        # Loop to encode/decode based on shift -- I used loop to prevent out-of-range exception
        for i in range(abs(self.__shift)):
            # Encode
            if pointer + 1 < len(self.__keys_list):
                pointer += 1
            else:
                pointer = 0

        return self.__keys_list[pointer]


class Cipher:
    def __init__(self, message: str, shift: int):
        self.__message: str = message
        self.__shift: int = shift

    def parse(self) -> str:
        """ Method to parse the message """
        message_parsed: str = ''

        for character in self.__message:
            message_parsed += Parser(character, self.__shift).key_parsed

        return message_parsed


if __name__ == '__main__':
    shift: int = 3

    print(Cipher("Python is Best", shift).parse())
    print(Cipher("Python is Best", shift).parse())
    print(Cipher("Python is Best", shift).parse())
    print(Cipher("Python is Best", shift).parse())
    print(Cipher("Python is Best", shift).parse())
    print(Cipher("Python is Best", shift).parse())
