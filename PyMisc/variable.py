################
# Constant
################
class constant:
    def __init__(self, value):
        self.__value = value

    @property
    def value(self):
        return self.__value

    def __repr__(self) -> str:
        return str(self.value)


################
# Position
################
class position:
    def __init__(self, row: int, column: int):
        self.__row: constant = constant(row)
        self.__column: constant = constant(column)

    @property
    def row(self) -> constant:
        return self.__row

    @property
    def column(self) -> constant:
        return self.__column

    @property
    def get(self) -> tuple[int, int]:
        return (self.row.value, self.column.value)


################
# Resolution
################
class resolution:
    def __init__(self, width: int, height: int):
        self.__width: int = width
        self.__height: int = height

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    @property
    def both(self) -> int:
        return self.width, self.height

    def area(self) -> int:
        return self.width * self.height

    def __repr__(self) -> str:
        return '{}x{}'.format(self.width, self.height)


################
# Size
################
class size(position):
    def __init__(self, row: int, column: int):
        super().__init__(row, column)

    @property
    def area(self) -> constant.value:
        return self.row.value * self.column.value

    def __eq__(self, other):
        if self.row.value == other.row.value and self.column.value == other.column.value:
            return True
        return False


################
# Length
################
class length:
    def __init__(self, length_: int):
        self.__length: constant = constant(length_)

    @property
    def length_(self):
        return self.__length


################
# Character
################
class char:
    def __init__(self, value: str | int):
        self.__value: str = ''
        self.value_ = value

    @property
    def value_(self):
        return self.__value

    @value_.setter
    def value_(self, value: str | int):
        if self.eligible(value):
            if isinstance(value, str):
                self.__value = value
            elif isinstance(value, int):
                self.__value = chr(value)

    @staticmethod
    def eligible(value: str | int) -> bool:
        if isinstance(value, str):
            if len(value) == 1:
                return True

        elif isinstance(value, int):
            if 0 <= value < 1114112:
                return True

        return False


################
# Complex
################
class complex:
    def __init__(self, real: float, imaginary: float):
        self.__real: float = real
        self.__imaginary: float = imaginary

    @property
    def real(self) -> float:
        return self.__real

    @property
    def imaginary(self) -> float:
        return self.__imaginary

    def __add__(self, other):
        return complex(self.__real + other.real, self.__imaginary + other.imaginary)

    def __sub__(self, other):
        return complex(self.__real - other.real, self.__imaginary - other.imaginary)

    def __mul__(self, other):
        return complex(self.__real * other.real - self.__imaginary * other.imaginary, self.__real * other.imaginary + self.__imaginary * other.real)

    def __truediv__(self, other):
        return complex(
            (self.__real * other.real + self.__imaginary * other.imaginary) / (other.real ** 2 + other.imaginary ** 2),
            (self.__imaginary * other.real - self.__real * other.imaginary) / (other.real ** 2 + other.imaginary ** 2)
        )

    def __repr__(self) -> str:
        number: str = f'{self.__real} '
        if self.__imaginary >= 0.0:
            number += f'+ {self.__imaginary}'
        else:
            number += f'- {self.__imaginary * -1}'
        number += 'i'
        return number
