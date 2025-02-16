import PyMisc.color as color
import PyMisc.variable as var


############
# Cell
############
class Cell:
    def __init__(self):
        self.__character: var.char = var.char(' ')
        self.__property: color.property = color.property()

    @property
    def character(self) -> str:
        return self.__character.value_

    @property
    def property(self) -> str:
        return self.__property.__repr__()

    @character.setter
    def character(self, value: var.char):
        self.__character = value

    @property.setter
    def property(self, value: color.property) -> None:
        """ Change property for bg, fg, and styles """
        self.__property = value

    def __repr__(self):
        return self.property + self.character + color.reset()


############
# Grid
############
class Grid:
    def __init__(self, size: var.size):
        self.__size = size
        self.__cells: list[list[Cell]] | None = None
        self.clear()

    @property
    def area(self):
        return self.__size.area

    @property
    def height(self):
        return self.__size.row.value

    @property
    def width(self):
        return self.__size.column.value

    def get_cell(self, position: var.position) -> Cell:
        """ Get cell of specific position """
        return self.__cells[position.row.value][position.column.value]

    def clear(self) -> None:
        """ Clears the grid """
        self.__cells: list[list[Cell]] = []
        if len(self.__cells) > 0:
            for r in range(self.__size.row.value):
                for c in range(self.__size.column.value):
                    self.__cells[r][c].character = ' '
                    self.__cells[r][c].property = color.property()

        else:
            for r in range(self.__size.row.value):
                row: list[Cell] = []
                for c in range(self.__size.column.value):
                    row.append(Cell())
                self.__cells.append(row)

    def draw(self) -> None:
        """ Prints the pattern """
        for row in self.__cells:
            for column in row:
                print(column, end='')
            print()

    def draw_filled_box(self, char: var.char, position: var.position, size: var.size, property_: color.property = color.property()) -> None:
        """ Insert a filled box at specific position of given size """
        for row in range(position.row.value, position.row.value + size.row.value):
            for column in range(position.column.value, position.column.value + size.column.value):
                self.__cells[row][column].character = char
                self.__cells[row][column].property = property_

    def draw_hollow_box(self, char: var.char, position: var.position, size: var.size, property_: color.property = color.property()) -> None:
        """ Insert a hollow box at specific position of given size """
        for row in range(position.row.value, position.row.value + size.row.value):
            for column in range(position.column.value, position.column.value + size.column.value):
                if row == position.row.value or row == position.row.value + size.row.value - 1:
                    self.__cells[row][column].character = char
                    self.__cells[row][column].property = property_

                elif column == position.column.value or column == position.column.value + size.column.value - 1:
                    self.__cells[row][column].character = char
                    self.__cells[row][column].property = property_

    def draw_horizontal_line(self, char: var.char, position: var.position, length: var.length, step: var.length = var.length(0), property_: color.property = color.property()) -> None:
        """ Insert a straight line horizontally """
        row: int = position.row.value
        column: int = position.column.value

        # Create
        for count in range(length.length_.value):
            # Line
            self.__cells[row][column].character = char
            self.__cells[row][column].property = property_

            # Step
            for step_count in range(step.length_.value):
                column += 1

            column += 1

    def draw_vertical_line(self, char: var.char, position: var.position, length: var.length, step: var.length = var.length(0), property_: color.property = color.property()) -> None:
        """ Insert a straight line vertically """
        row: int = position.row.value
        column: int = position.column.value

        # Create
        for count in range(length.length_.value):
            # Line
            self.__cells[row][column].character = char
            self.__cells[row][column].property = property_

            # Step
            for step_count in range(step.length_.value):
                row += 1

            row += 1

    def draw_diagonal_line_upward(self, char: var.char, position: var.position, length: var.length, step: var.length = var.length(0), property_: color.property = color.property()) -> None:
        """ Insert a straight line diagonally upward """
        row: int = position.row.value
        column: int = position.column.value

        # Create
        for count in range(length.length_.value):
            # Line
            self.__cells[row][column].character = char
            self.__cells[row][column].property = property_

            # Step
            for step_count in range(step.length_.value):
                row -= 1
                column += 1

            row -= 1
            column += 1

    def draw_diagonal_line_downward(self, char: var.char, position: var.position, length: var.length, step: var.length = var.length(0), property_: color.property = color.property()) -> None:
        """ Insert a straight line diagonally downward """
        row: int = position.row.value
        column: int = position.column.value

        # Create
        for count in range(length.length_.value):
            # Line
            self.__cells[row][column].character = char
            self.__cells[row][column].property = property_

            # Step
            for step_count in range(step.length_.value):
                row += 1
                column += 1

            row += 1
            column += 1

    def insert_individual(self, char: var.char, position: var.position, property_: color.property = color.property()) -> None:
        """ Insert an individual character at specific position """
        self.__cells[position.row.value][position.column.value].character = char
        self.__cells[position.row.value][position.column.value].property = property_

    def insert_grid(self, position: var.position, grid_, remove_bg_mode: bool = True) -> None:
        """ Insert a small grid """
        if self.area > grid_.area:
            row_index: int = position.row.value

            # Insert the new grid
            for row in range(grid_.height):
                column_index: int = position.column.value
                for column in range(grid_.width):
                    new_cell: Cell = grid_.get_cell(var.position(row, column))

                    # Remove Background
                    if remove_bg_mode:
                        check_cell: Cell = Cell()
                        if new_cell != check_cell:
                            self.__cells[row_index][column_index] = new_cell

                    # Normal
                    else:
                        self.__cells[row_index][column_index] = new_cell

                    column_index += 1
                row_index += 1

    def insert_text(self, position: var.position, text: var.constant, alignment: var.constant = var.constant('left'), property_: color.property = color.property()):
        """ Insert a word """
        match alignment.value:
            case 'left':
                column_index: int = position.column.value
                for char in text.value:
                    self.__cells[position.row.value][column_index].character = var.char(char)
                    self.__cells[position.row.value][column_index].property = property_
                    column_index += 1

            case 'right':
                pass

            case 'centre':
                pass

            case 'justify':
                pass
