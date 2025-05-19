from string import ascii_letters


def shifted_character_index(char: str, _list: list | tuple, shift: int) -> int:
    """ Get index of the shifted character """
    # ! The index to be shifted
    index: int = _list.index(char)

    # * Do shift
    # ! If shift is positive
    if shift > 0:
        for i in range(shift):
            # * If the index reached limit of the list ascii_letters' size
            if index == len(_list) - 1:
                index = 0
                continue
            index += 1
    # ! If shift is negative
    elif shift < 0:
        for i in range(abs(shift)):
            # * If the index reached the starting index of the list of ascii_letters
            if index == 0:
                index = len(_list) - 1
                continue
            index -= 1

    return index


class Ceaser:
    """
	? Layer 1 - Ceaser Cipher

	* Encode: Shift +ve
	* Decode: Shift -ve
	"""

    @staticmethod
    def parse(text: str, shift: int) -> str:
        result: str = ''

        print(text)  # ? Debug

        # * Iterate through each character of the text
        for c in text:
            print(f'{c} -> ', end='')  # ? Debug

            # * If the character is an ascii letter
            if c in ascii_letters:
                c = ascii_letters[shifted_character_index(c, list(ascii_letters), shift)]

            print(c)  # ? Debug
            result += c

        return result
