import tkinter as tk
import tkinter.messagebox as tmsg
import sqlite3 as sq
from tkinter import ttk
from os.path import join
from os import mkdir
from datetime import datetime


##################
# Functions
##################
def get_current_datetime():
    # Get the current date and time
    return datetime.now().strftime("%d-%m-%Y %H:%M")


##################
# Item
##################
class Item:
    def __init__(self, id: int, type: str, company: str, price: int, details: str = ''):
        self.id = id
        self.type = type
        self.company = company
        self.price = price
        self.details = details
        self.sell_date: str | None = None

    @property
    def data(self) -> list:
        return [
            self.id,
            self.type,
            self.company,
            self.price,
            self.details,
            self.sell_date if self.sell_date is not None else 'None'
        ]

    @staticmethod
    def header() -> list:
        return [
            'id',
            'type',
            'company',
            'price',
            'detail',
            'sell_date'
        ]

    def sell(self, customer) -> None:
        """ Sell the item to a customer """
        self.sell_date = get_current_datetime()

        customer.item_id = self.id
        customer.purchase_date = self.sell_date

    def __repr__(self) -> str:
        """ To represent the object as string """
        repr_: str = ''

        # Adding data
        for i in range(len(self.header())):
            repr_ += self.header()[i].capitalize() + f' {'-' * 5} ' + str(self.data[i]) + '\n'

        return repr_


##################
# Customer
##################
class Customer:
    def __init__(self, id: int, name: str, contact: str):
        self.id = id
        self.name = name
        self.contact = contact
        self.item_id: int | None = None
        self.purchase_date: str | None = None

    @property
    def data(self) -> list:
        return [
            self.id,
            self.name,
            self.contact,
            self.item_id if self.item_id is not None else 'None',
            self.purchase_date if self.purchase_date is not None else 'None'
        ]

    @staticmethod
    def header() -> list:
        return [
            'id',
            'name',
            'contact',
            'item_id',
            'purchase_date'
        ]

    def __repr__(self) -> str:
        """ To represent the object as string """
        repr_: str = ''

        # Adding data
        for i in range(len(self.header())):
            repr_ += self.header()[i].capitalize() + f' {'-' * 5} ' + str(self.data[i]) + '\n'

        return repr_


##################
# Inventory
##################
class Inventory:
    def __init__(self):
        self.items: list[Item] = []


##################
# DBMS
##################
class DataBase:
    def __init__(self):
        self.database = sq.connect('data.db')
        self.cursor = self.database.cursor()
        self.__pre_process()

    def insert(self, table_name: str, data: list) -> None:
        """ Insert data in table """
        command: str = f"INSERT INTO {table_name} VALUES {str(tuple(data))}"

        self.cursor.execute(command)
        self.database.commit()

    def retrieve(self, table: str, elements: str, condition: str = '') -> list:
        """ Retrieve data from table """
        # Query
        query: str = f'SELECT {elements} FROM {table}'
        if len(condition) > 0:
            query += f' WHERE {condition}'

        # Execute & commit query
        data: list = list(self.cursor.execute(query))
        self.database.commit()

        # Return data
        return data

    def remove(self, table: str, condition: str = '') -> None:
        """ Remove data from table """
        # Query
        query: str = f'DELETE FROM {table}'

        # Condition
        if len(condition) > 0:
            query += f' WHERE {condition}'

        # Execute & commit query
        self.cursor.execute(query)
        self.database.commit()

    def update(self, table: str, elements: list[str], values: list, condition: str = ''):
        """ Update data of table """
        # Query
        query: str = f'UPDATE {table} SET '

        # Adding values to set
        for i in range(len(elements)):
            query += f'{elements[i]} = \'{values[i]}\'' if isinstance(values[i], str) else f'{elements[i]} = {values[i]}'
            if i < len(elements) - 1:
                query += ','
            query += ' '

        # Condition
        if len(condition) > 0:
            query += f'WHERE {condition};'

        # Execute & commit query
        self.cursor.execute(query)
        self.database.commit()

    def __pre_process(self) -> None:
        """ Create important tables """
        item_header: list = Item.header()
        customer_header: list = Customer.header()

        # Items Table
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS items (
                -- Header
                {item_header[0]} INTEGER PRIMARY KEY AUTOINCREMENT,
                {item_header[1]} TEXT NOT NULL,
                {item_header[2]} TEXT NOT NULL,
                {item_header[3]} REAL NOT NULL,
                {item_header[4]} TEXT,
                {item_header[5]} TEXT
            )"""
        )

        # Commit changes
        self.database.commit()

        # Customers Table
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS customers (
                -- Header
                {customer_header[0]} INTEGER PRIMARY KEY AUTOINCREMENT,
                {customer_header[1]} TEXT NOT NULL,
                {customer_header[2]} TEXT NOT NULL,
                {customer_header[3]} INTEGER,  -- Define item_id first
                {customer_header[4]} TEXT,
                FOREIGN KEY ({customer_header[3]}) REFERENCES items(id) ON DELETE SET NULL  -- Define Foreign key
            )"""
        )

        # Commit changes
        self.database.commit()


#############################
# DBMS - Global Object
#############################
database: DataBase = DataBase()


######################
# Treeview Window
######################
class TreeviewWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # Properties
        self.width = 1280
        self.height = 720
        self.geometry(f'{self.width}x{self.height}')
        self.title('Data View')
        self.minsize(self.width, self.height)
        self.maxsize(self.width, self.height)

        # Some Frames
        self.__frame_items = tk.Frame(self, padx=10, pady=10)
        self.__frame_items.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.__frame_customers = tk.Frame(self, padx=10, pady=10)
        self.__frame_customers.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Tree-views
        self.__tree_items = ttk.Treeview(self.__frame_items, columns=tuple(Item.header()), show='headings')
        self.__tree_customers = ttk.Treeview(self.__frame_customers, columns=tuple(Customer.header()), show='headings')

        # Scroll-bars
        self.__scroll_items = ttk.Scrollbar(self.__frame_items, orient=tk.VERTICAL)
        self.__scroll_customers = ttk.Scrollbar(self.__frame_customers, orient=tk.VERTICAL)

        # Set the appearance
        self.__appearance()

    def __appearance(self) -> None:
        """ Set appearance """
        # Tree-view
        self.treeview()

    def treeview(self) -> None:
        """ A Treeview to display records in database """
        # Items
        self.__scroll_items.pack(side=tk.RIGHT, fill=tk.Y)
        for head in Item.header():
            self.__tree_items.heading(head, text=head)
            self.__tree_items.column(head, width=50)
        self.__tree_items.pack(fill=tk.BOTH, expand=True)
        self.__scroll_items.config(command=self.__tree_items.yview())

        # Customers
        self.__scroll_customers.pack(side=tk.RIGHT, fill=tk.Y)
        for head in Customer.header():
            self.__tree_customers.heading(head, text=head)
            self.__tree_customers.column(head, width=25)
        self.__tree_customers.pack(fill=tk.BOTH, expand=True)
        self.__scroll_customers.config(command=self.__tree_customers.yview())

        # Load Tree-view
        self.load_treeview_data()

    def load_treeview_data(self) -> None:
        """ To load data in tree-views """
        # Clear tree-views
        for row in self.__tree_items.get_children():
            self.__tree_items.delete(row)

        for row in self.__tree_customers.get_children():
            self.__tree_customers.delete(row)

        # Fetch data
        database.cursor.execute('SELECT * FROM items')
        for row in database.cursor.fetchall():
            self.__tree_items.insert('', 'end', values=row)

        database.cursor.execute('SELECT * FROM customers')
        for row in database.cursor.fetchall():
            self.__tree_customers.insert('', 'end', values=row)


##################
# Testing
##################
if __name__ == '__main__':
    # database: DataBase = DataBase()
    #
    # item: Item = Item(1, 'Laptop', 'Lenovo', 25000, 'i5 4th Generation')
    #
    # customer: Customer = Customer(3, 'Talha Ahmad', '+92 331 4650460')
    #
    # item.sell(customer)

    # print(item, customer, sep='\n')

    # database.insert('items', item.data)
    # database.insert('customers', customer.data)

    # data = database.retrieve('items', '*')
    # print(data)

    # database.remove('items')

    '''
    database.update(
        'items',
        ['price', 'details'],
        [45000, 'i5 6th Generation'],
        'id = 1'
    )
    '''

    win = TreeviewWindow()
    win.mainloop()

    pass
