
keys: dict[str, list[str]] = {
    'row-0' : ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+'],

    'row-1' : ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '{', '}', '|'],

    'row-2' : ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', '"'],

    'row-3' : ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', '>', '?']
}

def getKeysList(key: str) -> list[str]:
    """ Function to get related list from keys dictionary """
    _list: list[str] = [key]

    for i in range(len(keys)):
        if key in keys[f'row-{i}']:
            _list = keys[f'row-{i}']

    return _list

class Parser:
    def __init__(self, key: str, shift: int):
        self.__key: str = key
        self.__shift: int = shift

        self.__key_parsed: str = self._parse()

    @property
    def key_parsed(self) -> str:
        return self.__key_parsed

    def _parse(self) -> str:
        """ Method to parse key with shift for encoding/decoding """
        # Local Variables
        key: str = self.__key
        keys_list: list[str] = getKeysList(key)
        pointer: int = keys_list.index(key)

        # Loop to encode/decode based on shift -- I used loop to prevent out-of-range exception
        for i in range(abs(self.__shift)):
            # Encode
            if self.__shift >= 0:
                if pointer + 1 < len(keys_list):
                    pointer += 1
                else:
                    pointer = 0

            # Decode
            else:
                if pointer - 1 >= 0:
                    pointer -= 1
                else:
                    pointer = len(keys_list) - 1

        return keys_list[pointer]


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
    # shift: int = 3
    # print(
    #     Cipher("The quick brown fox jumps over a lazy dog.", shift).parse(),
    #     Cipher("Ily rp[n' ,u]t. j]b ;p/\\g ]myu f Afvo h]kX", -shift).parse(),
    #     sep='\n'
    # )

    shift = 5
    print(Cipher("My name is Talha Ahmad.", shift).parse())
    print(Cipher("I'm a computer science student.", shift).parse())
    print(Cipher("Is it correct? 2 + 2 = 3. Yes, But in binary system.", shift).parse())
    print(Cipher("The quick brown fox jumps over a lazy dog. This is a pangram which means it contains all aplhabets of English.", shift).parse())
