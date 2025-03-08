from PyMisc.variable import constant as const

##############
# Global
##############
LEGALS: str = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'


##############
# Base
##############
class Base(const):  # INFO: Base decides which number has valid value
    def __init__(self, value: int):
        super().__init__(value)


##############
# Decimal
##############
class Decimal(const):   # INFO: Decimal number having value range 0 to 9
    def __init__(self, value: int = 0):
        super().__init__(value)             # TODO: Sets the value of the decimal number
        self.base: Base = Base(10)          # TODO: Sets the base of the decimal number
        self.__name: str = "decimal"

    @property
    def name(self) -> str:
        return self.__name.capitalize()


##############
# HexaDecimal
##############
class HexaDecimal(const):  # INFO: Hexadecimal number having value range 0 to F
    def __init__(self, value: str = ""):
        super().__init__(value)             # TODO: Sets the value of the hexadecimal number
        self.base: Base = Base(16)          # TODO: Sets the base of the hexadecimal number
        self.__name: str = "hexadecimal"

    @property
    def name(self) -> str:
        return self.__name.capitalize()


##############
# Octal
##############
class Octal(const):  # INFO: Octal number having value range 0 to 7
    def __init__(self, value: str = ""):
        super().__init__(value)             # TODO: Sets the value of the octal number
        self.base: Base = Base(8)           # TODO: Sets the base of the octal number
        self.__name: str = "octal"

    @property
    def name(self) -> str:
        return self.__name.capitalize()


##############
# Binary
##############
class Binary(const):  # INFO: Binary number having value range 0 to 1
    def __init__(self, value: str = ""):
        super().__init__(value)             # TODO: Sets the value of the binary number
        self.base: Base = Base(2)           # TODO: Sets the base of the binary number
        self.__name: str = "binary"

    @property
    def name(self) -> str:
        return self.__name.capitalize()


##############
# Custom
##############
class Custom(const):  # INFO: Custom number having value range defined by user
    def __init__(self, value: str, base: int, name: str = ""):
        super().__init__(value)             # TODO: Sets the value of the custom number
        self.base: Base = Base(base)        # TODO: Sets the base of the custom number
        self.__name: str = name.lower()

    @property
    def name(self) -> str:
        return self.__name.capitalize()


############################
# conversion Functions
############################
def convert_to_base(number: Decimal, base: int) -> Custom:
    """ Convert a number from decimal to any base (2-16) """
    if base < 2:
        raise ValueError("Base must be greater than or equal to 2")
    
    result: str = ''
    value: int = number.value
    while value > 0:
        result = LEGALS[value % base] + result
        value = int(value / base)
    return Custom(result, base)

def convert_from_base(number: Custom | Octal | Binary | HexaDecimal) -> Decimal:
    """ Convert a number from any base (2-16) to decimal """
    result: int = 0
    value: str = number.value
    for digit in value:
        result += result * number.base + LEGALS.index(digit)
    return Decimal(result)


##############
# Testing
##############
if __name__ == '__main__':
    num: Octal = Octal(56)
    dec: Decimal = convert_from_base(num)
