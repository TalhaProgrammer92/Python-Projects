import tkinter as tk
import tkinter.messagebox as tmsg
import sqlite3 as sq
from tkinter import ttk
from os.path import join
from os import mkdir
from datetime import datetime


########################
# Database - Global
########################
database = sq.connect('data.db')
cursor = database.cursor()


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
    def __init__(self, type: str, company: str, price: int, details: str = ''):
        self.type = type
        self.company = company
        self.price = price
        self.details = details
        self.sell_date: str | None = None

    @property
    def data(self) -> tuple:
        return (
            self.type,
            self.company,
            self.price,
            self.details,
            self.sell_date if self.sell_date is not None else 'None'
        )

    @staticmethod
    def header() -> tuple:
        return (
            'id',
            'type',
            'company',
            'price',
            'detail',
            'sell_date'
        )

    def __repr__(self) -> str:
        """ To represent the object as string """
        repr_: str = ''

        # Adding data
        for i in range(len(self.header())):
            repr_ += f'{self.header()[i]} {'-' * 5} {self.data[i]}\n'

        return repr_


##################
# Customer
##################
class Customer:
    def __init__(self, name: str, contact: str, item_id):
        self.name = name
        self.contact = contact
        self.item_id: int = item_id
        self.purchase_date: str = get_current_datetime()

    @property
    def data(self) -> tuple:
        return (
            self.name,
            self.contact,
            self.item_id if self.item_id is not None else 0,
            self.purchase_date if self.purchase_date is not None else 'None'
        )

    @staticmethod
    def header() -> tuple:
        return (
            'id',
            'name',
            'contact',
            'item_id',
            'purchase_date'
        )

    def __repr__(self) -> str:
        """ To represent the object as string """
        repr_: str = ''

        # Adding data
        for i in range(len(self.header())):
            repr_ += f'{self.header()[i]} {'-' * 5} {self.data[i]}\n'

        return repr_


#######################
# Database Functions
#######################
def create_tables():
    """ Create tables if don't exist """
    item_header: list = Item.header()
    customer_header: list = Customer.header()

    # Items Table
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS items (
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
    database.commit()

    # Customers Table
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS customers (
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
    database.commit()

def insert(table: str, names: tuple, values: tuple):
    """ To insert data in a table """
    cursor.execute(f'INSERT INTO {table} {names} VALUES {values}')
    database.commit()

# Call the function
create_tables()

##################
# Inventory
##################
class Inventory:
    def __init__(self):
        self.items: list[Item] = []


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
        tk.Label(self.__frame_items, text='Items', font=('calibri', 15, 'bold'), fg='blue').pack()
        self.__scroll_items.pack(side=tk.RIGHT, fill=tk.Y)
        for head in Item.header():
            self.__tree_items.heading(head, text=head)
            self.__tree_items.column(head, width=50)
        self.__tree_items.pack(fill=tk.BOTH, expand=True)
        self.__scroll_items.config(command=self.__tree_items.yview())

        # Customers
        tk.Label(self.__frame_customers, text='Customers', font=('calibri', 15, 'bold'), fg='blue').pack()
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
        cursor.execute('SELECT * FROM items')
        for row in cursor.fetchall():
            self.__tree_items.insert('', 'end', values=row)

        cursor.execute('SELECT * FROM customers')
        for row in cursor.fetchall():
            self.__tree_customers.insert('', 'end', values=row)


##################
# Testing
##################
if __name__ == '__main__':
    item: Item = Item('Laptop', 'Lenovo', 25000, 'i5 4th Generation')
    customer: Customer = Customer('Talha Ahmad', '+92 331 4650460', 1)
    item.sell_date = customer.purchase_date

    # Insert data
    insert('items', Item.header()[1:], item.data)
    insert('customers', Customer.header()[1:], customer.data)

    win = TreeviewWindow()
    win.mainloop()

    pass
