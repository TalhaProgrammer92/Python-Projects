import PyMisc.color as clr

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


########################
# Player Class
########################
class Player:
    def __init__(self, name: Name):
        self.name: Name = name
        self.score: Score = Score()

    # Representation method
    def __repr__(self) -> str:
        return self.name.__repr__() + '\t' + self.score.__repr__()