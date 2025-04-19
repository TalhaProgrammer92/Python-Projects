import PyMisc.color as clr
import os
import time

########################
# Symbol Class
########################
class Symbol:
    def __init__(self, unicode: str, color_property: clr.property):
        self.unicode: str = unicode
        self.color: clr.property = color_property

    # Representation Method
    def __repr__(self) -> str:
        return clr.get_colored(self.unicode, self.color)


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
# Name Class
########################
class Name:
    def __init__(self, name: str, color: clr.property):
        self.__name: str = name
        self.__color: clr.property = color

    # Getter of name
    @property
    def name(self) -> str:
        return self.__name

    # Method to compare two names
    def __eq__(self, other) -> bool:
        return self.name.lower() == other.name.lower()

    # Representation method
    def __repr__(self) -> str:
        return clr.get_colored(self.__name, self.__color)


########################
# Score Class
########################
class Score:
    def __init__(self):
        self.__score: int = 0

    # Getter
    @property
    def score(self) -> int:
        return self.__score

    # Increment method
    def increaseBy(self, offset: int = 1) -> None:
        """ This method increase current score by given offset """
        if offset > 0:
            self.__score += offset

    # Reset the current score
    def reset(self) -> None:
        self.__score = 0

    # Representation method
    def __repr__(self) -> str:
        return str(self.__score)
