from logging import raiseExceptions

from PyMisc.variable import constant
import string

###################
# Variable
###################
class Variable:
    def __init__(self, name: str, value):
        self.__name = None
        if Variable.validName(name):
            self.__name = name
        else:
            raise ValueError('Illegal variable name')
        self.value = value

    @staticmethod
    def validName(name: str) -> bool:
        """ Checks if the name is valid or not """
        # Rule 1
        if ' ' in name or name[0] in string.digits:
            return False

        # Rule 2
        for char in name:
            if char in string.punctuation and char != '_':
                return False

        # Final Result
        return True

    @property
    def name(self) -> str:
        return self.__name

    def __repr__(self) -> str:
        return f'{type(self.value)} {self.name} = {self.value}'

###################
# Constant
###################
class Constant(constant):
    def __init__(self, name: str, value):
        self.__name = None
        if Variable.validName(name):
            self.__name = name
        else:
            raise ValueError('Illegal constant variable name')
        super().__init__(value)

    @property
    def name(self) -> str:
        return self.__name

    def __repr__(self) -> str:
        return f'Constant {type(self.value)} {self.name} = ' + super().__repr__()


###################
# Node
###################
class Node:
    def __init__(self, properties: list):
        self.__properties = properties

    @property
    def properties(self) -> list:
        return self.__properties

    def __repr__(self) -> str:
        output: str = ''
        for i in range(len(self.properties)):
            output += f'{i + 1}. {self.properties[i].__repr__()}\n'
        return output


###################
# Testing
###################
if __name__ == '__main__':
    node: Node = Node([
        Variable('name', 'Talha Ahmad'),
        Constant('lucky_number', 7)
    ])

    print(node)
