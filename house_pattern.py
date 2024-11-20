"""
========================================================================
INFO: Program to print the following house pattern in Python
========================================================================

      =================
     )V V V V V V V V V(
    )V V V V V V V V V V(
   )V V V V V V V V V V V(
  )V V V V V V V V V V V V(
 )V V V V V V V V V V V V V(
)V V V V V V V V V V V V V V(
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:::::::::::::::::::::::::::::
:::::::::::::::::::::::::::::
:::::::::::::::::::::::::::::
:::::::::::::::::::::::::::::
:::::::::::::::::::::::::::::
::::::::::::IIIII::::::::::::
::::::::::::IIIII::::::::::::
::::::::::::IIIII::::::::::::
::::::::::::IIIII::::::::::::
::::::::::::IIIII::::::::::::
"""

def printSequence(character: str, limit: int) -> None:
    print(character*limit, end='')

def printSequenceGap(character: str, limit: int) -> None:
    for count in range(limit):
        print(character, end='')
        if count != limit-1:
            print(' ', end='')

class House:
    def __init__(self) -> None:
        # TODO: Variables
        self.__row = 17
        self.__gap = 6

    def __update(self) -> None:
        self.__row += 2
        self.__gap -= 1
        
    def __drawRoof(self) -> None:
        # NOTE: Draw top
        printSequence(' ', self.__gap)      # TODO: Whitespaces
        printSequence('=', self.__row)      # TODO: Equal signs (Roof Top)
        print()
        self.__update()
        
        while self.__gap >= 0:
            printSequence(' ', self.__gap)                  # TODO: Whitespaces
            print(')', end='')                              # TODO: Right bracket
            printSequenceGap('V', int(self.__row / 2))      # TODO: Equal signs (Roof Top)
            print('(')                                      # TODO: Left bracket
            self.__update()
        
        self.__row -= 2

    def __drawBody(self) -> None:
        for count in range(10):
            # NOTE: The value of self.__row is 29, 29 / 2 (int) -> 14 - 2 => 12 + 12 => 24 - 29 (abs) => 5
            if count < 5:
                printSequence(':', self.__row)
            else:
                printSequence(':', int(self.__row / 2) - 2)
                printSequence('I', 5)
                printSequence(':', int(self.__row / 2) - 2)
            print()
    
    def draw(self) -> None:
        # TODO: Roof
        self.__drawRoof()
        
        # TODO: Cieling
        printSequence('~', self.__row)
        print()
        
        # TODO: Body
        self.__drawBody()


# Test
if __name__ == '__main__':
    my_house = House()
    my_house.draw()