from PyMisc.variable import constant as const

##############
# Global
##############
LEGALS: str = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def is_valid(number: str, base: int) -> bool:
    for digit in number:
        if digit.upper() not in LEGALS[:base]:
            return False
    return True


##############
# Custom
##############
class Custom:  # INFO: Custom number having value range defined by user
    def __init__(self, value: str, base: int, name: str = "unknown"):
        self.__value = value  # TODO: Sets the value of the custom number
        self.__base: int = base  # TODO: Sets the base of the custom number
        self.__name: str = name.lower()

    @property
    def name(self) -> str:
        return self.__name

    @property
    def base(self) -> int:
        return self.__base

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, v: str):
        self.__value = v if is_valid(self.__value, self.base) else self.__value

    def __repr__(self) -> str:
        return f'Value:\t{self.value}\nBase:\t{self.base}\nName:\t{self.name.capitalize()}'


############################
# conversion Functions
############################
def convert(number: Custom, base: int) -> Custom:
    """ Convert a number from decimal to any base (2-16) """
    if base < 2:
        raise ValueError("Base must be greater than or equal to 2")

    result = ''

    # From base 10
    if number.base == 10:
        value: int = int(number.value)
        while value > 0:
            result = LEGALS[value % base] + result
            value = int(value / base)
        return Custom(result, base)

    # To base 10
    else:
        result = 0
        value: str = number.value
        p: int = len(value) - 1
        for digit in value:
            result += LEGALS.index(digit.upper()) * pow(number.base, p)
            p -= 1
        result = str(result)

    return Custom(result, base)


##############
# Testing
##############
if __name__ == '__main__':
    decimal: Custom = Custom('11', 10)
    binary: Custom = convert(decimal, 2)
    print(
        binary,
        convert(binary, 10),
        sep='\n\n'
    )
