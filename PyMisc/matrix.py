from PyMisc import variable


###############
# Matrix
###############
class matrix:
    def __init__(self, *args: list[int]):
        self.__data: list[list[variable.constant]] = []

        # Adding data
        for list_ in args:
            row: list[variable.constant] = []
            for number in list_:
                row.append(variable.constant(number))
            self.__data.append(row)

        # Initializing size of the matrix
        self.__size: variable.size = variable.size(len(self.__data), len(self.__data[0]))

    @property
    def order(self):
        return self.__size

    def getData(self, position: variable.position) -> variable.constant:
        """ Get data at specific position of matrix """
        return self.__data[position.row.value][position.column.value]

    def __add__(self, other):
        """ Adding two matrices """
        if self.order == other.order:
            solution_data: list = []

            # Adding data of two matrices
            for row_index in range(self.order.row.value):
                nums: list[int] = []
                for columns_index in range(self.order.column.value):
                    nums.append(
                        self.getData(variable.position(row_index, columns_index)).value +
                        other.getData(variable.position(row_index, columns_index)).value
                    )
                solution_data.append(nums)

            # Return the solution
            solution: matrix = matrix(
                [row for row in solution_data]
            )
            return solution

        return None

    def __repr__(self) -> str | None:
        """ To represent the class object """
        if self.__data is not None:
            matrix_string: str = ''

            # Reading data
            if self.__data is not None:
                for row in self.__data:
                    matrix_string += '['
                    for number in row:
                        matrix_string += f'{number.value}\t'
                    matrix_string += '\b]\n'

            return matrix_string

        return None


###############
# Testing
###############
if __name__ == '__main__':
    matrix_: matrix = matrix(
        # [1, 2],
        #       [3, 4]
        [num for num in range(1, 3)],
        [num for num in range(3, 5)]
    )

    print(matrix_)
