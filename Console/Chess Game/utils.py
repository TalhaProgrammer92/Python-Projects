import time

########################
# Time Counter Class
########################
class TimeCounter:
    def __init__(self):
        self.__start = time.time()
        self.__current = None

    # Update Time
    def update(self):
        """ This method updates current time """
        self.__current = time.time()

    # Get time duration
    @property
    def duration(self):
        return self.__current - self.__start if self.__current is not None else None


########################
# Position Class
########################
class Position:
    def __init__(self, row: int, column: int):
        self.__row: int = row
        self.__column: int = column

    # Getters
    @property
    def row(self) -> int:
        return self.__row

    @property
    def column(self) -> int:
        return self.__column

    # Setters
    @row.setter
    def row(self, value: int):
        self.__row = value if value >= 0 else self.row

    @column.setter
    def column(self, value: int):
        self.__column = value if value >= 0 else self.column

    # Overloaded method for subtraction
    def __sub__(self, other):
        return Position(abs(self.row - other.row), abs(self.column - other.column))

    # Representation method
    def __repr__(self) -> str:
        return f"({self.row}, {self.column})"