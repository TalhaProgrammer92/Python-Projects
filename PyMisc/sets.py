########################
# Set (Class)
########################
class Set:
    def __init__(self):
        self.__elements: list[int] = []

    @property
    def power(self):
        return len(self.__elements)

    @property
    def elements(self) -> list[int]:
        return self.__elements

    def add(self, *args: int) -> None:
        """ Append values in the set's elements list """
        for value in args:
            if value not in self.__elements:
                self.__elements.append(value)
        self.__elements.sort()

    def __repr__(self) -> str:
        set_: str = '{'

        # Fill the set string
        for element in self.__elements:
            set_ += str(element)
            if self.__elements.index(element) < self.power - 1:
                set_ += ', '
        set_ += '}'

        return set_


########################
# Common (Operations)
########################
class CommonOperation:
    @staticmethod
    def union(set1: Set, set2: Set) -> Set:
        """ Perform union operation on two sets """
        result: Set = Set()  # Reference Size

        # Copy elements -- Set 1
        for element in set1.elements:
            result.add(element)

        # Copy elements -- Set 2
        for element in set2.elements:
            if element not in set1.elements:
                result.add(element)

        return result

    @staticmethod
    def intersect(set1: Set, set2: Set) -> Set:
        """ Perform intersection operation on two sets """
        result: Set = Set()

        # Copy common elements -- Set 1
        for element in set1.elements:
            if element in set2.elements:
                result.add(element)

        # Copy common elements -- Set 2
        for element in set2.elements:
            if element in set1.elements:
                result.add(element)

        return result

    @staticmethod
    def difference(set1: Set, set2: Set) -> Set:
        """ Perform difference operation on two sets """
        result: Set = Set()

        for element in set1.elements:
            if element not in set2.elements:
                result.add(element)

        return result


########################
# Advance (Operations)
########################
class AdvanceOperation:
    @staticmethod
    def complement(set_: Set, universal: Set) -> Set:
        """ Find complement of a set """
        return CommonOperation.intersect(universal, set_)

    @staticmethod
    def symmetric_difference(set1: Set, set2: Set) -> Set:
        """ Find symmetric difference of two sets """
        result: Set = Set()

        # Copy common elements -- Set 1
        for element in set1.elements:
            if element not in set2.elements:
                result.add(element)

        # Copy common elements -- Set 2
        for element in set2.elements:
            if element not in set1.elements:
                result.add(element)

        return result


###################################
# Cartesian Product (Class)
###################################
class Cartesian:
    def __init__(self, set1: Set, set2: Set):
        self.__product: list[list[int]] = []
        self.__operation(set1, set2)

    @property
    def pairs(self) -> list[list[int]]:
        return self.__product

    def __operation(self, set1: Set, set2: Set) -> None:
        """ finds the cartesian product of two given sets """
        pass
