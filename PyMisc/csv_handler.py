from os.path import exists, join
from PyMisc.variable import char


##################
# CSV Reader
##################
class Reader:
    def __init__(self, path: str, file: str, separator: char = char(',')):
        self.__path = join(path, file)
        self.__separator = separator.value_
        self.__data = []

        # Extract data
        with open(self.__path, 'r') as file:
            rows = file.read().split('\n')

        # Append data to the actual list
        for row in rows:
            if len(row) > 0 and row != '\n':
                self.__data.append(row.split(self.__separator))

    def extract_all_data(self) -> list:
        """ Extract all the data from csv file """
        return self.__data

    def get_indexed_row(self, index: int) -> list:
        """ Get specific row """
        return self.__data[index]

    def get_header(self):
        """ Get first (header) row """
        return self.__data[0]


##################
# CSV Writer
##################
class Writer:
    def __init__(self, path: str, file: str, separator: char = char(',')):
        self.__path = join(path, file)
        self.__separator = separator.value_

    def write_data(self, mode: str, *args: list) -> None:
        """ Write data to csv file """
        with open(self.__path, mode) as file:
            # Read each row in the data 'args'
            data: str = ''
            for row in args:
                # The text to write in the file
                text: str = '\n'

                # Write each element to the text
                for i in range(len(row)):
                    text += str(row[i]) if row[i] is not None else 'None'
                    if i < len(row) - 1:
                        text += self.__separator
                if mode == 'a':
                    # Write in the file
                    file.write(text)
                else:
                    data += text
            if mode == 'w':
                file.write(data)


##################
# CSV Updater
##################
class Updater:
    pass
