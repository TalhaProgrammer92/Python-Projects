import tkinter as tk
import tkinter.messagebox as tmsg
from PyMisc.csv_handler import *
from os.path import exists
from os import mkdir
from datetime import datetime


##################
# Functions
##################
def get_current_datetime():
    # Get the current date and time
    current_date_time = datetime.now()
    return current_date_time


##################
# Item
##################
class Item:
    def __init__(self, id: int, type_: str, company: str, price: int, description: str = 'none'):
        self.id: int = id
        self.type: str = type_.lower()
        self.company: str = company.lower()
        self.price: int = price
        self.sell: str = 'none'
        self.description: str = description.lower()

    @staticmethod
    def get_header() -> list:
        """ To get list of headers """
        return [
            'id',           # 0
            'type',         # 1
            'company',      # 2
            'price',        # 3
            'sell',         # 4
            'description'   # 5
        ]

    @property
    def data(self) -> list:
        """ To get list of data """
        return [
            self.id,            # 0
            self.type,          # 1
            self.company,       # 2
            self.price,         # 3
            self.sell,          # 4
            self.description    # 5
        ]

    def __repr__(self) -> str:
        """ To represent with print() function """
        return f"""
Id:         {self.id}
Type:       {self.type.capitalize()}
Company:    {self.company.capitalize()}
Price:      Rs. {self.price}
Sell:       {self.sell}
Details:    {self.description}"""


##################
# Customer
##################
class Customer:
    def __init__(self, id: int, name: str, item_id: int, ph_number: str):
        self.id: int = id
        self.name: str = name.lower()
        self.item_id: int = item_id
        self.ph_number: str = ph_number.lower()
        self.buy: str = get_current_datetime()

    @property
    def data(self) -> list:
        """ To get list of data """
        return [
            self.id,            # 0
            self.name,          # 1
            self.item_id,       # 2
            self.ph_number,     # 3
            self.buy            # 4
        ]

    def get_header() -> list:
        """ To get list of headers """
        return [
            'id',           # 0
            'name',         # 1
            'item-id',      # 2
            'ph',           # 3
            'buy'           # 4
        ]


##################
# Iventory
##################
class Inventory:
    def __init__(self):
        self.__items: list[Item] = []

    @property
    def get_all(self):
        return self.__items

    def add(self, *args: Item):
        """ Add item to the inventory """
        for item in args:
            self.__items.append(item)


##################
# Data Base
##################
class DataBase:
    def __init__(self, path: str, file: str):
        self.__path: str = path
        self.__file: str = file
        self.__data: list = None
        self.reload_data()

    @property
    def data(self):
        return self.__data

    def reload_data(self) -> None:
        """ Reload the data to manage changes """
        self.__data = Reader(self.__path, self.__file).extract_all_data()

    def update(self, id: int, new_data: Item | Customer) -> None:
        """ Update specific row's data of given id """
        # Find the item
        for i in range(len(self.__data)):
            # Update the item
            if self.__data[i].id == id:
                self.__data[i] = new_data.data
                break

    def redundancy(self, data: Item | Customer) -> bool:
        """ To check whether new data is already in current data list or not """
        # Check redundancy
        # For item object
        if isinstance(data, Item):
            # Check each row in the data list
            for row in self.__data:
                if row[1:] == data.data[1:]:
                    return True

        # For customer object
        elif isinstance(data, Customer):
            # Check each row in the data list
            for row in self.__data:
                if row[1] == data.name and row[3] == data.ph_number:
                    return True
        return False

    def add(self, data: Item | Customer) -> None:
        """ To add new data """
        # Add to the list
        if not self.redundancy(data):
            self.__data.append(data.data)

            # Save to the file
            write_data: Writer = Writer(self.__path, self.__file)
            write_data.write_data('a', data.data)
        else:
            tmsg.showerror('Redundancy', 'The data you entered already exists in the current data-base')

    def save_changes(self) -> None:
        """ To manage changes in the data base """
        # Update data in the file
        write_data: Writer = Writer(self.__path, self.__file)
        write_data.write_data('w', self.__data)    # Over-write the data

        # Reload data list
        self.reload_data()

    def delete(self, id: int) -> None:
        """ Remove the specific data row """
        # Find the item
        for i in range(len(self.__data)):
            # Update the item
            if self.__data[i].id == id:
                self.__data.remove(self.__data[i])
                break

    def retrieve(self):
        pass


if __name__ == '__main__':
    ###################################################
    # If following dirs don't exist i.e.:
    #   data <dir>
    #   items.csv
    #   customers.csv
    ###################################################

    # Directory
    path: str = 'data'
    if not exists(path):
        mkdir(path)

    # Files
    files: list = ['items.csv', 'customers.csv']
    headers: list = [Item.get_header(), Customer.get_header()]
    for i in range(len(files)):
        if not exists(join(path, files[i])):
            writer: Writer = Writer(path, files[i])
            writer.write_data('a', headers[i])

    # Testing
    db: DataBase = DataBase(path, files[0])

    item1: Item = Item(len(db.data), 'Laptop', 'Lenovo', 30000, 'i5 4th Generation')
    print(item1)
    db.add(item1)

    item2: Item = Item(len(db.data), 'Desktop', 'Dell', 25000, 'intel Xeon 3.5 GHz')
    db.add(item2)
    print(item2)

    print(db.data)
