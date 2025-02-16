#######################
# Math Operations
#######################
class operation:
    @staticmethod
    def factorial(number: int) -> int:
        fact: int = 1

        for n in range(number):
            fact *= n + 1

        return fact