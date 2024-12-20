##############################
# Global - Variables
##############################
LEGALS: str = '+-*/&|~^<>(){}[]_!@.'

##############################
# Cell - Class
##############################
class Cell:
    def __init__(self):
        self.__value: int = 0

    ##############
    # Getters
    ##############
    @property
    def value(self) -> int:
        return self.__value

    ##############
    # Methods
    ##############
    def increment(self) -> None:
        """ To increase cell's value by 1 """
        self.__value += 1 if self.value < 127 else 0

    def decrement(self) -> None:
        """ To decrease cell's value by 1 """
        self.__value -= 1 if self.value > 0 else 0

    def double(self) -> None:
        """ To double the cell's value """
        self.__value *= 2 if self.value * 2 <= 127 else 1

    def half(self) -> None:
        """ To half the cell's value """
        self.__value = int(self.__value / 2 if int(self.value * 2) >= 0 else 1)

    def bitwise_and(self, value: int) -> None:
        """ Perform bitwise AND operation """
        self.__value = self.__value & value

    def bitwise_or(self, value: int) -> None:
        """ Perform bitwise OR operation """
        self.__value = self.__value | value

    def bitwise_not(self) -> None:
        """ Perform bitwise NOT operation """
        self.__value = ~self.__value

    def bitwise_xor(self, value: int) -> None:
        """ Perform bitwise XOR operation """
        self.__value = self.__value ^ value

    def output(self) -> None:
        """ To display ASCII character of the value """
        print(chr(self.value), end='')

    def reset(self) -> None:
        """ To reset the value """
        self.__value = 0


##############################
# Stack - Class
##############################
class Stack:
    def __init__(self):
        self.cells: list[Cell] = []
        self.__limit: int = 8
        self.__pointer: int = 0

        for count in range(self.__limit):
            cell = Cell()
            self.cells.append(cell)

    ##############
    # Getters
    ##############
    @property
    def pointer(self):
        return self.__pointer

    ######################
    # Methods - Stack
    ######################
    def to_next(self) -> None:
        """ Goto next cell in the stack """
        self.__pointer += 1 if self.__pointer < self.__limit - 1 else 0

    def to_previous(self) -> None:
        """ Goto previous cell in the stack """
        self.__pointer -= 1 if self.__pointer > 0 else 0

    def jump_start(self) -> None:
        """ Goto to first cell in the stack """
        self.__pointer = 0

    def jump_end(self) -> None:
        """ Goto to last cell in the stack """
        self.__pointer = self.__limit - 1

    def reset(self) -> None:
        """ To reset values of all cells in the stack """
        for cell in self.cells:
            cell.reset()
        self.__pointer = 0


##############################
# Memory - Class
##############################
class Memory:
    def __init__(self):
        self.stacks: list[Stack] = []
        self.__limit: int = 16
        self.__pointer: int = 0
        self.add()

    ##############
    # Getters
    ##############
    @property
    def pointer(self):
        return self.__pointer

    ######################
    # Methods - Memory
    ######################
    def add(self) -> None:
        """ To add a Stack in the memory """
        if len(self.stacks) < self.__limit - 1:
            stack = Stack()
            self.stacks.append(stack)

    def to_next(self) -> None:
        """ Goto next cell in the memory """
        self.__pointer += 1 if self.__pointer < self.__limit - 1 else 0

    def to_previous(self) -> None:
        """ Goto previous cell in the memory """
        self.__pointer -= 1 if self.__pointer > 0 else 0

    def jump_start(self) -> None:
        """ Goto first cell in the memory """
        self.__pointer = 0

    def jump_end(self) -> None:
        """ Goto last cell in the memory """
        self.__pointer = self.__limit - 1


##############################
# Token - Class
##############################
class Token:
    def __init__(self, symbol: str):
        self.__symbol: str = symbol
        self.__is_valid: bool = self.__validity()

    ##############
    # Methods
    ##############
    def __validity(self) -> bool:
        if self.__symbol in LEGALS:
            return True
        return False

    ##############
    # Getters
    ##############
    @property
    def symbol(self) -> str:
        return self.__symbol

    @property
    def is_valid(self) -> int:
        return self.__is_valid


##############################
# ASCII - Class
##############################
class Ascii:
    def __init__(self, character: str = chr(0)):
        self.__char: str = character
        self.__code: int = ord(self.__char)

    @property
    def code(self):
        return self.__code

    @property
    def character(self):
        return self.__char

    def __repr__(self):
        return f'{self.code} : {self.character}'


##############################
# Program - Class
##############################
class Program:
    def __init__(self, source_code: str = ""):
        self.__source_code: str = source_code
        self.__tokens: list[Token] = []
        self.__stacks: Memory = Memory()

    ##############
    # Methods
    ##############
    def write(self) -> None:
        """ To write program """
        coding: bool = True
        while coding:
            statement: str = input()
            self.__source_code += statement
            if '.' in statement:
                coding = False

    def load(self) -> None:
        """ To load the program written """
        self.__tokens = []
        for character in self.__source_code:
            token: Token = Token(character)
            if token.is_valid:
                self.__tokens.append(token)
                if token.symbol == '.':
                    break

    def execute(self) -> None:
        """ To execute the program loaded """
        for token in self.__tokens:
            stack_pointer: int = self.__stacks.pointer
            cell_pointer: int = self.__stacks.stacks[stack_pointer].pointer
            match token.symbol:
                #################
                # Operators
                #################
                case '+':
                    self.__stacks.stacks[stack_pointer].cells[cell_pointer].increment()
                case '-':
                    self.__stacks.stacks[stack_pointer].cells[cell_pointer].decrement()
                case '*':
                    self.__stacks.stacks[stack_pointer].cells[cell_pointer].double()
                case '/':
                    self.__stacks.stacks[stack_pointer].cells[cell_pointer].half()
                case '&':
                    value: int = self.__stacks.stacks[stack_pointer].cells[cell_pointer + 1].value if cell_pointer < 7 else self.__stacks.stacks[stack_pointer].cells[cell_pointer - 1].value
                    self.__stacks.stacks[stack_pointer].cells[cell_pointer].bitwise_and(value)
                case '|':
                    value: int = self.__stacks.stacks[stack_pointer].cells[cell_pointer + 1].value if cell_pointer < 7 else self.__stacks.stacks[stack_pointer].cells[cell_pointer - 1].value
                    self.__stacks.stacks[stack_pointer].cells[cell_pointer].bitwise_or(value)
                case '~':
                    self.__stacks.stacks[stack_pointer].cells[cell_pointer].bitwise_not()
                case '^':
                    value: int = self.__stacks.stacks[stack_pointer].cells[cell_pointer + 1].value if cell_pointer < 7 else \
                    self.__stacks.stacks[stack_pointer].cells[cell_pointer - 1].value
                    self.__stacks.stacks[stack_pointer].cells[cell_pointer].bitwise_xor(value)

                #################
                # Navigation
                #################
                case '<':
                    self.__stacks.stacks[stack_pointer].to_previous()
                case '>':
                    self.__stacks.stacks[stack_pointer].to_next()
                case '(':
                    self.__stacks.stacks[stack_pointer].jump_start()
                case ')':
                    self.__stacks.stacks[stack_pointer].jump_end()
                case '{':
                    self.__stacks.to_previous()
                case '}':
                    self.__stacks.to_next()
                case '[':
                    self.__stacks.jump_start()
                case ']':
                    self.__stacks.jump_end()

                #################
                # Advance
                #################
                case '@':
                    self.__stacks.stacks[stack_pointer].cells[cell_pointer].output()
                case '_':
                    self.__stacks.add()
                case '!':
                    self.__stacks.stacks[stack_pointer].reset()

    def save(self) -> None:
        """ To save the program in text file """
        pass
