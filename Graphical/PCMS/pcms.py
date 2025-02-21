import tkinter as tk
import tkinter.messagebox as tmsg
import sqlite3 as sq
import pandas as pd
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

def retrieve(table: str, attributes: tuple | str, condition: str = '', commit: bool = False) -> list:
    """ To retrieve data from database """
    # Query
    query: str = f'SELECT {attributes} FROM {table}'

    # Condition
    if len(condition) > 0:
        query += f' WHERE {condition}'

    # Executing query
    data: list = list(cursor.execute(query))
    if commit:
        database.commit()

    # Return data retrieved
    return data

# Call the function
create_tables()

##################
# Excel Wizard
##################
class ExcelWizard(tk.Tk):
    def __init__(self):
        super().__init__()

        # Properties
        self.title('Excel Wizard')
        self.width = 350
        self.height = 300
        self.geometry(f'{self.width}x{self.height}')
        self.maxsize(self.width, self.height)
        self.minsize(self.width, self.height)
        self.iconbitmap('icon.ico')

        # Actions (Attributes)
        self.__item_check = [[label, tk.IntVar()] for label in Item.header()[1:]]
        self.__item_options = ['id']
        self.__customer_check = [[label, tk.IntVar()] for label in Customer.header()[1:]]
        self.__customer_options = ['id']

        # Function Call
        self.__set_appearance()

    def __set_appearance(self) -> None:
        """ Set appearance and behaviour """
        # Label
        tk.Label(self, text='Save records of your choice', font=('bahnschrift', 15, 'bold'), bg='orange', fg='blue').pack(fill='x')

        # Methods Call
        self.__selection_box()

    def action_item(self) -> None:
        """ Perform some action on user's selection for Item """
        print('\n*** Item ***')
        for attribute in self.__item_check:
            if attribute[1].get() and attribute not in self.__item_options:
                self.__item_options.append(attribute[0])
            elif attribute[0] in self.__item_options:
                self.__item_options.remove(attribute[0])
            print(attribute[0], attribute[1].get())

    def action_customer(self) -> None:
        """ Perform some action on user's selection for Customer"""
        print('\n*** Customer ***')
        for attribute in self.__customer_check:
            if attribute[1].get() and attribute[0] not in self.__customer_options:
                self.__customer_options.append(attribute[0])
            elif attribute[0] in self.__customer_options:
                self.__customer_options.remove(attribute[0])
            print(attribute[0], attribute[1].get())

    def __selection_box(self) -> None:
        """ Set all selection options for user to select which data he wants to store """
        # Frames
        item_frame = tk.Frame(self, padx=5, pady=5)
        item_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        customer_frame = tk.Frame(self, padx=5, pady=5)
        customer_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Adding Options - Item
        tk.Label(item_frame, text='ITEM', bg='yellow', fg='green', font='arial 10 bold').pack(fill='x')
        for label, check in self.__item_check:
            tk.Checkbutton(item_frame, text=label.capitalize(), variable=check, command=self.action_item, pady=2).pack()

        # Adding Options - Customer
        tk.Label(customer_frame, text='CUSTOMER', bg='yellow', fg='green', font='arial 10 bold').pack(fill='x')
        for label, check in self.__customer_check:
            tk.Checkbutton(customer_frame, text=label.capitalize(), variable=check, command=self.action_customer, pady=2).pack()


######################
# Treeview Window
######################
class TreeviewWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # Properties
        self.geometry('1280x720')
        self.title('Data View')
        self.minsize(800, 600)
        # self.maxsize(self.width, self.height)
        self.iconbitmap('icon.ico')

        # Attributes to show
        self.items_attributes = Item.header()
        self.customers_attributes = Customer.header()

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
        # Menu bar
        self.create_menus()

        # Tree-view
        self.treeview()

    def save_to_excel(self) -> None:
        """ To save current data in excel file to increase portability """
        excel_win = ExcelWizard()
        excel_win.mainloop()

    def add_item(self) -> None:
        tmsg.showinfo('Action', 'The item has been added successfully')

    def add_customer(self) -> None:
        tmsg.showinfo('Action', 'The customer has been added successfully')

    def update_items(self) -> None:
        tmsg.showinfo('Action', 'The item has been updated successfully')

    def update_customers(self) -> None:
        tmsg.showinfo('Action', 'The customer has been updated successfully')

    def remove_items(self) -> None:
        tmsg.showinfo('Action', 'The item has been removed successfully')

    def remove_customers(self) -> None:
        tmsg.showinfo('Action', 'The customer has been removed successfully')

    def filter_items(self) -> None:
        tmsg.showinfo('Filter', 'The items data has been filtered successfully')

    def filter_customers(self) -> None:
        tmsg.showinfo('Filter', 'The customers data has been filtered successfully')

    def create_menus(self) -> None:
        """ To create menus and sub-menus """
        # Main Bar
        menu_bar = tk.Menu(self)

        # File Menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Reload", command=self.load_treeview_data)
        file_menu.add_command(label="Save to Excel", command=self.save_to_excel)
        file_menu.add_separator()  # Add a separator line
        file_menu.add_command(label="Exit", command=exit)

        # Action Menu
        action_menu = tk.Menu(menu_bar, tearoff=0)
        action_menu.add_command(label="Add Item", command=self.add_item)
        action_menu.add_command(label="Add Customer", command=self.add_customer)
        action_menu.add_separator()
        action_menu.add_command(label="Update Item(s)", command=self.update_items)
        action_menu.add_command(label="Update Customer(s)", command=self.update_customers)
        action_menu.add_separator()
        action_menu.add_command(label="Remove Item(s)", command=self.remove_items)
        action_menu.add_command(label="Remove Customer(s)", command=self.remove_customers)

        # Filter Menu
        filter_menu = tk.Menu(menu_bar, tearoff=0)
        filter_menu.add_command(label="Filter Items Data", command=self.filter_items)
        filter_menu.add_command(label="Filter Customers Data", command=self.filter_customers)

        # Add Menus to Menu Bar
        menu_bar.add_cascade(label="File", menu=file_menu)
        menu_bar.add_cascade(label="Action", menu=action_menu)
        menu_bar.add_cascade(label='Filter', menu=filter_menu)

        # Configure the window to use this menu bar
        self.config(menu=menu_bar)

    def treeview(self) -> None:
        """ A Treeview to display records in database """
        # Items
        tk.Label(self.__frame_items, text='ITEMS DATA', font=('calibri', 15, 'bold'), fg='blue').pack()
        self.__scroll_items.pack(side=tk.RIGHT, fill=tk.Y)
        for head in Item.header():
            self.__tree_items.heading(head, text=head)
            self.__tree_items.column(head, width=50)
        self.__tree_items.pack(fill=tk.BOTH, expand=True)
        self.__scroll_items.config(command=self.__tree_items.yview())

        # Customers
        tk.Label(self.__frame_customers, text='CUSTOMERS DATA', font=('calibri', 15, 'bold'), fg='blue').pack()
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
        cursor.execute(f'SELECT * FROM items')
        for row in cursor.fetchall():
            self.__tree_items.insert('', 'end', values=row)

        cursor.execute(f'SELECT * FROM customers')
        for row in cursor.fetchall():
            self.__tree_customers.insert('', 'end', values=row)

         # Message
        tmsg.showinfo('Reload', 'The data has been reloaded successfully')


##################
# Testing
##################
if __name__ == '__main__':
    item: Item = Item('Laptop', 'Lenovo', 25000, 'i5 4th Generation')
    customer: Customer = Customer('Talha Ahmad', '+92 331 4650460', 1)
    item.sell_date = customer.purchase_date

    # Insert data
    # insert('items', Item.header()[1:], item.data)
    # insert('customers', Customer.header()[1:], customer.data)

    # win = TreeviewWindow()
    # win.mainloop()

    excel_win = ExcelWizard()
    excel_win.mainloop()

    pass
