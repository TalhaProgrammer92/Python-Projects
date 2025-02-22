import os.path
import tkinter as tk
import tkinter.messagebox as tmsg
import sqlite3 as sq
import pandas as pd
from tkinter import ttk
from os.path import join, splitext, exists
from os import mkdir, listdir, startfile
from datetime import datetime


########################
# Database - Global
########################
database = sq.connect('data.db')
cursor = database.cursor()

if not exists('records'):
    mkdir('records')


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

def update(table: str, attributes, values, condition: str) -> None:
    """ to update data in database """
    query = f'UPDATE {table} SET '

    # Adding values to be updated
    if isinstance(attributes, tuple) or isinstance(attributes, list):
        for i in range(len(attributes)):
            query += f'{attributes[i]} = \'{values[i]}\'' if isinstance(values[i], str) else f'{attributes[i]} = {values[i]}'
            if i < len(attributes) - 1:
                query += ', '
    else:
        query += f'{attributes} = \'{values}\'' if isinstance(values, str) else f'{attributes} = {values}'

    # Condition
    query += f' WHERE {condition};'

    # Execute query
    print(query)
    cursor.execute(query)
    database.commit()


# Call the function
create_tables()


############################
# Item Insert Wizard
############################
class ItemInsertWizard(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        # Properties
        self.title('Item Wizard')
        self.iconbitmap('icon.ico')
        self.width = 280
        self.height = 150
        self.geometry(f'{self.width}x{self.height}')
        self.minsize(self.width, self.height)
        self.maxsize(self.width, self.height)

        # Entry Variables
        self.type = tk.StringVar()
        self.company = tk.StringVar()
        self.price = tk.StringVar()
        self.detail = tk.StringVar()

        # Function call
        self.__appearance()

    def insert_data(self):
        """ Insert data in database """
        # Get Data Entries
        type_ = self.type.get().strip()
        company = self.company.get().strip()
        price = self.price.get().strip()
        detail = self.detail.get().strip()

        # Validity
        if not price.isdigit():
            tmsg.showerror('Insert Wizard', 'Please make sure you have entered correct price')
            return
        price = int(price)
        if not (len(type_) > 0 and len(company) > 0 and price > 0):
            tmsg.showerror('Insert Wizard', 'Please make sure you have entered correct data')
            return

        # Object of Item
        item = Item(type_, company, price, detail)
        insert(
            'items',
            Item.header()[1:],
            item.data
        )

        # Display Message
        tmsg.showinfo('Insert Wizard', 'The data has been inserted successfully')

        # Load data
        self.master.load_treeview_data()

        # Destroy the wizard window
        self.destroy()

    def __appearance(self) -> None:
        # Labels
        tk.Label(self, text='Type', font='arial 12', fg='blue').grid(row=0, column=0)
        tk.Label(self, text='Company', font='arial 12', fg='blue').grid(row=1, column=0)
        tk.Label(self, text='Price', font='arial 12', fg='blue').grid(row=2, column=0)
        tk.Label(self, text='Detail', font='arial 12', fg='blue').grid(row=3, column=0)

        # Entry
        self.entry_type = tk.Entry(self, textvariable=self.type, font='calibri 12')
        self.entry_type.grid(row=0, column=1)

        self.entry_company = tk.Entry(self, textvariable=self.company, font='calibri 12')
        self.entry_company.grid(row=1, column=1)

        self.entry_price = tk.Entry(self, textvariable=self.price, font='calibri 12')
        self.entry_price.grid(row=2, column=1)

        self.entry_detail = tk.Entry(self, textvariable=self.detail, font='calibri 12')
        self.entry_detail.grid(row=3, column=1)

        # Button
        tk.Button(self, text='Insert', font='arial 13', command=self.insert_data).grid(row=4, column=1)


############################
# Customer Insert Wizard
############################
class CustomerInsertWizard(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        # Properties
        self.title('Customer Wizard')
        self.iconbitmap('icon.ico')
        self.width = 280
        self.height = 150
        self.geometry(f'{self.width}x{self.height}')
        self.minsize(self.width, self.height)
        self.maxsize(self.width, self.height)

        # Entry Variables
        self.name = tk.StringVar()
        self.contact = tk.StringVar()
        self.item_id = tk.StringVar()

        # Function Call
        self.__appearance()

    def insert_data(self) -> None:
        # Get Data Entries
        name = self.name.get().strip()
        contact = self.contact.get().strip()
        item_id = self.item_id.get().strip()

        # Validity
        if not item_id.isdigit():
            tmsg.showerror('Insert Wizard', 'Please make sure you have entered correct item id')
            return
        if not (len(name) > 0 and len(contact) > 0):
            tmsg.showerror('Insert Wizard', 'Please make sure you have entered correct data')
            return
        item_id = int(item_id)

        # Object of Customer
        customer = Customer(name, contact, item_id)

        # Update Item sell data
        update(
            'items',
            'sell_date',
            customer.purchase_date,
            f'id = {item_id}'
        )

        # Add Customer
        insert(
            'customers',
            Customer.header()[1:],
            customer.data
        )

        # Display Message
        tmsg.showinfo('Insert Wizard', 'The data has been inserted successfully')

        # Load data
        self.master.load_treeview_data()

        # Destroy the wizard window
        self.destroy()

    def __appearance(self) -> None:
        # Labels
        tk.Label(self, text='Name', font='arial 12', fg='blue').grid(row=0, column=0)
        tk.Label(self, text='Contact', font='arial 12', fg='blue').grid(row=1, column=0)
        tk.Label(self, text='Item Id', font='arial 12', fg='blue').grid(row=2, column=0)

        # Entry
        self.entry_name = tk.Entry(self, textvariable=self.name, font='calibri 12')
        self.entry_name.grid(row=0, column=1)

        self.entry_contact = tk.Entry(self, textvariable=self.contact, font='calibri 12')
        self.entry_contact.grid(row=1, column=1)

        self.entry_item_id = tk.Entry(self, textvariable=self.item_id, font='calibri 12')
        self.entry_item_id.grid(row=2, column=1)

        # Button
        tk.Button(self, text='Insert', font='arial 13', command=self.insert_data).grid(row=3, column=1)


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

        # Items
        query: str = f'SELECT * FROM items'
        dataframe = pd.read_sql_query(query, database)
        items_file: str = f'items {datetime.now().strftime("%d-%m-%Y %H %M")}.xls'
        # print(dataframe.empty)
        dataframe.to_excel(join('records', items_file), index=False, engine='openpyxl')


        # Customers
        query: str = f'SELECT * FROM customers'
        dataframe = pd.read_sql_query(query, database)
        customers_file: str = f'customers {datetime.now().strftime("%d-%m-%Y %H %M")}.xlsx'
        # print(dataframe.empty)
        dataframe.to_excel(join('records', customers_file), index=False, engine='openpyxl')

        # Message
        agreed = tmsg.askyesno('Excel', 'The data has been saved successfully in the records folder. Would you like to open these files?')
        if agreed:
            startfile(join('records', items_file))
            startfile(join('records', customers_file))

    def add_item(self) -> None:
        insert_wizard = ItemInsertWizard(self)  # Pass 'self' as master
        insert_wizard.grab_set()  # Makes the window modal (disables main window until closed)

    def add_customer(self) -> None:
        insert_wizard = CustomerInsertWizard(self)
        insert_wizard.grab_set()

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
        # Treeview style
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 9, "bold"), bg="silver")  # Bold headings

        # Items
        tk.Label(self.__frame_items, text='ITEMS DATA', font=('calibri', 15, 'bold'), fg='blue', bg='orange').pack(fill='x')
        self.__scroll_items.pack(side=tk.RIGHT, fill=tk.Y)
        for head in Item.header():
            self.__tree_items.heading(head, text=head.upper())
            self.__tree_items.column(head, width=50)
        self.__tree_items.pack(fill=tk.BOTH, expand=True)
        self.__scroll_items.config(command=self.__tree_items.yview())

        # Customers
        tk.Label(self.__frame_customers, text='CUSTOMERS DATA', font=('calibri', 15, 'bold'), fg='blue', bg='orange').pack(fill='x')
        self.__scroll_customers.pack(side=tk.RIGHT, fill=tk.Y)
        for head in Customer.header():
            self.__tree_customers.heading(head, text=head.upper())
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
    # item: Item = Item('Laptop', 'Lenovo', 25000, 'i5 4th Generation')
    # customer: Customer = Customer('Talha Ahmad', '+92 331 4650460', 1)
    # item.sell_date = customer.purchase_date

    # Insert data
    # insert('items', Item.header()[1:], item.data)
    # insert('customers', Customer.header()[1:], customer.data)

    win = TreeviewWindow()
    win.mainloop()

    pass
