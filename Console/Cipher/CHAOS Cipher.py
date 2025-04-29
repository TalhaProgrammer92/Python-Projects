# Cipher of Highly Abstract Obfuscation System (CHAOS) - Talha Ahmad (c)

import QMC

# Global variables
shift: int = 3

# Layer 1 - Ceaser Cipher
def ceaser(text: str, mode: int = 1) -> str:
    global shift
    _: str = ''

    shift *= mode
    for i in range(len(text)):
        value: int = ord(text[i])
        if text[i].isalnum():
            value += shift
        _ += chr(value)
    shift *= mode

    return _

# Layer 2 - QMC Cipher
def qwerty_map_cipher(text: str, mode: int = 1) -> str:
    global shift

    shift *= mode
    _: str = QMC.Cipher(text, shift).parse()
    shift *= mode

    return _

# Encoder
def encode(text: str) -> str:
    l1: str = ceaser(text)
    l2: str = qwerty_map_cipher(l1)

    return l2

# Decoder
def decode(text: str) -> str:
    l1: str = qwerty_map_cipher(text, -1)
    l2: str = ceaser(l1, -1)

    return l2

if __name__ == '__main__':
    print(encode("Hello World"), decode('"l]]u Vup]k'), sep='\n')