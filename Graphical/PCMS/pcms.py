# import os.path
import tkinter as tk
import tkinter.messagebox as tmsg
import sqlite3 as sq
import pandas as pd
from tkinter import ttk
from os.path import join, splitext, exists
from os import mkdir, listdir, startfile
from datetime import datetime
from PyMisc.system import authorized_mac


########################
# Authorization
########################
if not authorized_mac('mac.txt'):
    tmsg.showerror('Unauthorized Access', 'Your machine has not been authorized yet. Contact your software publisher/provider.')
    exit()


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
            'id',           # 0
            'type',         # 1
            'company',      # 2
            'price',        # 3
            'detail',       # 4
            'sell_date'     # 5
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
            'id',               # 0
            'name',             # 1
            'contact',          # 2
            'item_id',          # 3
            'purchase_date'     # 4
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

def retrieve(table: str, attributes: tuple | list, condition: str = '', commit: bool = False) -> list:
    """ To retrieve data from database """
    # Query
    query: str = f"SELECT {', '.join(attributes)} FROM {table}" if len(attributes[0]) > 1 else f"SELECT {attributes} FROM {table}"

    # Condition
    if len(condition) > 0:
        query += f' WHERE {condition}'

    # Executing query
    # print(query)
    cursor.execute(query)
    data = cursor.fetchone()
    if commit:
        database.commit()

    # Return data retrieved
    return data

def update(table: str, attributes, values, condition: str) -> None:
    """ to update data in database """
    query = f'UPDATE {table} SET '

    # Adding values to be updated
    if len(attributes) == len(values):
        if not isinstance(attributes, str) and not isinstance(values, str):
            for i in range(len(attributes)):
                query += f'{attributes[i]} = \'{values[i]}\'' if isinstance(values[i], str) else f'{attributes[i]} = {values[i]}'
                if i < len(attributes) - 1:
                    query += ', '
        else:
            query += f'{attributes} = \'{values}\'' if isinstance(values, str) else f'{attributes} = {values}'
    else:
        query += f'{attributes} = \'{values}\'' if isinstance(values, str) else f'{attributes} = {values}'


    # Condition
    if len(condition) > 0:
        query += f' WHERE {condition};'

    # Execute query
    # print(query)
    cursor.execute(query)
    database.commit()

def remove(table: str, condition: str):
    """ To remove data from database """
    cursor.execute(f'DELETE FROM {table} WHERE {condition}')
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
        self.width = 250
        self.height = 160
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

        try:
            # Object of Item
            item = Item(type_, company, price, detail)

            # Insert data
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
        except sq.OperationalError:
            tmsg.showerror('Insert Wizard', 'Please make sure you\'ve entered correct data')

    def __appearance(self) -> None:
        # Labels
        tk.Label(self, text='Insert Some Data', font='arial 15', bg='orange', fg='blue').grid(row=0, column=1)
        tk.Label(self, text='Type', font='arial 12', fg='blue').grid(row=1, column=0)
        tk.Label(self, text='Company', font='arial 12', fg='blue').grid(row=2, column=0)
        tk.Label(self, text='Price', font='arial 12', fg='blue').grid(row=3, column=0)
        tk.Label(self, text='Detail', font='arial 12', fg='blue').grid(row=4, column=0)

        # Entry
        self.entry_type = tk.Entry(self, textvariable=self.type, font='calibri 12')
        self.entry_type.grid(row=1, column=1)

        self.entry_company = tk.Entry(self, textvariable=self.company, font='calibri 12')
        self.entry_company.grid(row=2, column=1)

        self.entry_price = tk.Entry(self, textvariable=self.price, font='calibri 12')
        self.entry_price.grid(row=3, column=1)

        self.entry_detail = tk.Entry(self, textvariable=self.detail, font='calibri 12')
        self.entry_detail.grid(row=4, column=1)

        # Button
        tk.Button(self, text='Insert', font='arial 13', command=self.insert_data, bg='cyan', relief='groove').grid(row=5, column=1)


############################
# Customer Insert Wizard
############################
class CustomerInsertWizard(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        # Properties
        self.title('Customer Wizard')
        self.iconbitmap('icon.ico')
        self.width = 240
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

        try:
            # Check item existence
            cursor.execute("SELECT COUNT(*) FROM items WHERE id = ?", (item_id,))
            exists = cursor.fetchone()[0]  # Fetch the count
            if not exists:
                tmsg.showerror('Insert Wizard', f'The item \'{item_id}\' does not exist in the database')
                return

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
        except sq.OperationalError:
            tmsg.showerror('Insert Wizard', 'Please make sure you\'ve entered correct data')

    def __appearance(self) -> None:
        # Labels
        tk.Label(self, text='Insert Some Data', font='arial 15', bg='orange', fg='blue').grid(row=0, column=1)
        tk.Label(self, text='Name', font='arial 12', fg='blue').grid(row=1, column=0)
        tk.Label(self, text='Contact', font='arial 12', fg='blue').grid(row=2, column=0)
        tk.Label(self, text='Item Id', font='arial 12', fg='blue').grid(row=3, column=0)

        # Entry
        self.entry_name = tk.Entry(self, textvariable=self.name, font='calibri 12')
        self.entry_name.grid(row=1, column=1)

        self.entry_contact = tk.Entry(self, textvariable=self.contact, font='calibri 12')
        self.entry_contact.grid(row=2, column=1)

        self.entry_item_id = tk.Entry(self, textvariable=self.item_id, font='calibri 12')
        self.entry_item_id.grid(row=3, column=1)

        # Button
        tk.Button(self, text='Insert', font='arial 13', command=self.insert_data, bg='cyan', relief='groove').grid(row=4, column=1)


############################
# Item Update Wizard
############################
class ItemUpdateWizard(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        # Properties
        self.title('Item Wizard')
        self.iconbitmap('icon.ico')
        self.width = 260
        self.height = 190
        self.geometry(f'{self.width}x{self.height}')
        self.minsize(self.width, self.height)
        self.maxsize(self.width, self.height)

        # Entry Variable
        self.type = tk.StringVar()
        self.company = tk.StringVar()
        self.price = tk.StringVar()
        self.detail = tk.StringVar()
        self.condition = tk.StringVar()

        # Function call
        self.__appearance()

    def update_data(self) -> None:
        """ Update data in database """
        # Get Data Entries
        type_ = self.type.get().strip()
        company = self.company.get().strip()
        price = self.price.get().strip()
        detail = self.detail.get().strip()
        condition = self.condition.get().strip()

        # Validity
        # print(type_, company, price, detail, condition)
        if len(condition) == 0:
            if not tmsg.askyesno('Update Wizard', 'You did not provide any condition. This would effect your entire data of items. Would you like to proceed at your own risk?'):
                return

        if len(type_) == 0 and len(company) == 0 and len(detail) == 0 and not price.isdigit():
            tmsg.showerror('Update Wizard', 'Please add some data to update')
            return
        elif price.isdigit():
            price = int(price)

        # Data lists
        data = []
        header = []
        if len(type_) > 0:
            data.append(type_)
            header.append(Item.header()[1])
        if len(company) > 0:
            data.append(company)
            header.append(Item.header()[2])
        if isinstance(price, int):
            if price > 0:
                data.append(price)
                header.append(Item.header()[3])
        if len(detail) > 0:
            data.append(detail)
            header.append(Item.header()[4])

        try:
            # Update data
            update(
                'items',
                header,
                data,
                condition
            )

            # Display Message
            tmsg.showinfo('Update Wizard', 'The data has been updated successfully')

            # Load data
            self.master.load_treeview_data()

            # Destroy the wizard window
            self.destroy()
        except sq.OperationalError:
            tmsg.showerror('Update Wizard', 'Please make sure you\'ve entered correct data')

    def __appearance(self) -> None:
        # Labels
        tk.Label(self, text='Insert Some Data', font='arial 15', bg='orange', fg='blue').grid(row=0, column=1)
        tk.Label(self, text='Type', font='arial 12', fg='blue').grid(row=1, column=0)
        tk.Label(self, text='Company', font='arial 12', fg='blue').grid(row=2, column=0)
        tk.Label(self, text='Price', font='arial 12', fg='blue').grid(row=3, column=0)
        tk.Label(self, text='Detail', font='arial 12', fg='blue').grid(row=4, column=0)
        tk.Label(self, text='Condition', font='arial 12', fg='blue').grid(row=5, column=0)

        # Entry
        self.entry_type = tk.Entry(self, textvariable=self.type, font='calibri 12')
        self.entry_type.grid(row=1, column=1)

        self.entry_company = tk.Entry(self, textvariable=self.company, font='calibri 12')
        self.entry_company.grid(row=2, column=1)

        self.entry_price = tk.Entry(self, textvariable=self.price, font='calibri 12')
        self.entry_price.grid(row=3, column=1)

        self.entry_detail = tk.Entry(self, textvariable=self.detail, font='calibri 12')
        self.entry_detail.grid(row=4, column=1)

        self.entry_condition = tk.Entry(self, textvariable=self.condition, font='calibri 12')
        self.entry_condition.grid(row=5, column=1)

        # Button
        tk.Button(self, text='Update', font='arial 13', command=self.update_data, relief='groove', bg='orange').grid(row=6, column=1)


############################
# Customer Update Wizard
############################
class CustomerUpdateWizard(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        # Properties
        self.title('Customer Wizard')
        self.iconbitmap('icon.ico')
        self.width = 260
        self.height = 160
        self.geometry(f'{self.width}x{self.height}')
        self.minsize(self.width, self.height)
        self.maxsize(self.width, self.height)

        # Entry Variable
        self.name = tk.StringVar()
        self.contact = tk.StringVar()
        self.item_id = tk.StringVar()
        self.condition = tk.StringVar()

        # Function call
        self.__appearance()

    def update_data(self) -> None:
        """ Update data in database """
        # Get Data Entries
        name = self.name.get().strip()
        contact = self.contact.get().strip()
        item_id = self.item_id.get().strip()
        condition = self.condition.get().strip()

        # Validity
        # print(type_, company, price, detail, condition)
        if len(condition) == 0:
            if not tmsg.askyesno('Update Wizard', 'You did not provide any condition. This would effect your entire data of items. Would you like to proceed at your own risk?'):
                return

        if len(name) == 0 and len(contact) == 0 and not item_id.isdigit():
            tmsg.showerror('Update Wizard', 'Please add some data to update')
            return
        elif item_id.isdigit():
            item_id = int(item_id)

        # Data lists
        has_item_id: bool = False
        data = []
        header = []
        if len(name) > 0:
            data.append(name)
            header.append(Customer.header()[1])
        if len(contact) > 0:
            data.append(contact)
            header.append(Customer.header()[2])
        if isinstance(item_id, int):
            data.append(item_id)
            header.append(Customer.header()[3])
            has_item_id = True

        try:
            # Update data
            if has_item_id:
                # Remove previous items' sell date
                id = retrieve(
                    'customers',
                    ('item_id'),
                    condition,
                    True
                )
                # print(id)
                if tmsg.askyesno('Update Wizard', f'Do you want to remove item sell date of id \'{id[0]}\'?'):

                    # Change Sell Date
                    update(
                        'items',
                        'sell_date',
                        'None',
                        f'id={id[0]}'
                    )

                # Update Item's sell date
                date = get_current_datetime()
                update(
                    'items',
                    'sell_date',
                    date,
                    f'id={item_id}'
                )

                # Append Purchase data
                data.append(date)
                header.append(Customer.header()[4])

            # Update Customers' data
            update(
                'customers',
                header,
                data,
                condition
            )

            # Display Message
            tmsg.showinfo('Update Wizard', 'The data has been updated successfully')

            # Load data
            self.master.load_treeview_data()

            # Destroy the wizard window
            self.destroy()
        except sq.OperationalError:
            tmsg.showerror('Update Wizard', 'Please make sure you\'ve entered correct data')

    def __appearance(self) -> None:
        # Labels
        tk.Label(self, text='Insert Some Data', font='arial 15', bg='orange', fg='blue').grid(row=0, column=1)
        tk.Label(self, text='Name', font='arial 12', fg='blue').grid(row=1, column=0)
        tk.Label(self, text='Contact', font='arial 12', fg='blue').grid(row=2, column=0)
        tk.Label(self, text='Item Id', font='arial 12', fg='blue').grid(row=3, column=0)
        tk.Label(self, text='Condition', font='arial 12', fg='blue').grid(row=4, column=0)

        # Entry
        self.entry_name = tk.Entry(self, textvariable=self.name, font='calibri 12')
        self.entry_name.grid(row=1, column=1)

        self.entry_contact = tk.Entry(self, textvariable=self.contact, font='calibri 12')
        self.entry_contact.grid(row=2, column=1)

        self.entry_item_id = tk.Entry(self, textvariable=self.item_id, font='calibri 12')
        self.entry_item_id.grid(row=3, column=1)

        self.entry_condition = tk.Entry(self, textvariable=self.condition, font='calibri 12')
        self.entry_condition.grid(row=4, column=1)

        # Button
        tk.Button(self, text='Update', font='arial 13', command=self.update_data, relief='groove', bg='orange').grid(row=5, column=1)


############################
# Item Remove Wizard
############################
class ItemRemoveWizard(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        # Properties
        self.title('Item Wizard')
        self.iconbitmap('icon.ico')
        self.width = 250
        self.height = 100
        self.geometry(f'{self.width}x{self.height}')
        self.minsize(self.width, self.height)
        self.maxsize(self.width, self.height)

        # Entry Variable
        self.condition = tk.StringVar()

        # Function call
        self.__appearance()

    def remove_data(self) -> None:
        """ Remove data from database """
        # Get Entry
        condition: str = self.condition.get().strip()

        if len(condition) > 0:
            try:
                # Remove
                remove(
                    'items',
                    condition
                )

                # Message
                tmsg.showinfo('Remove Wizard', f'Your data has been removed successfully on condition "{condition}".')

                # Load data
                self.master.load_treeview_data()

                # Destroy the wizard window
                self.destroy()
            except sq.OperationalError:
                tmsg.showerror('Remove Wizard', 'Please make sure you\'ve entered correct condition')
        else:
            tmsg.showerror('Remove Wizard', 'Please enter a condition to remove data.')

    def __appearance(self) -> None:
        # Labels
        tk.Label(self, text='Select Attributes to Remove', font='arial 15', fg='blue', bg='orange').grid(row=0, column=0, columnspan=2)
        tk.Label(self, text='Condition', font='arial 12', fg='blue').grid(row=1, column=0)

        # Entry
        self.entry_condition = tk.Entry(self, textvariable=self.condition, font='calibri 12')
        self.entry_condition.grid(row=1, column=1)

        # Button
        tk.Button(self, text='Remove', font='arial 13', command=self.remove_data, bg='red', relief='groove').grid(row=2, column=1)


############################
# Customer Remove Wizard
############################
class CustomerRemoveWizard(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        # Properties
        self.title('Customer Wizard')
        self.iconbitmap('icon.ico')
        self.width = 250
        self.height = 100
        self.geometry(f'{self.width}x{self.height}')
        self.minsize(self.width, self.height)
        self.maxsize(self.width, self.height)

        # Entry Variable
        self.condition = tk.StringVar()

        # Function call
        self.__appearance()

    def remove_data(self) -> None:
        """ Remove data from database """
        # Get Entry
        condition: str = self.condition.get().strip()

        if len(condition) > 0:
            try:
                # Remove
                remove(
                    'customers',
                    condition
                )

                # Message
                tmsg.showinfo('Remove Wizard', f'Your data has been removed successfully on condition "{condition}".')

                # Load data
                self.master.load_treeview_data()

                # Destroy the wizard window
                self.destroy()
            except sq.OperationalError:
                tmsg.showerror('Remove Wizard', 'Please make sure you\'ve entered correct condition')
        else:
            tmsg.showerror('Remove Wizard', 'Please enter a condition to remove data.')

    def __appearance(self) -> None:
        # Labels
        tk.Label(self, text='Select Attributes to Remove', font='arial 15', fg='blue', bg='orange').grid(row=0, column=0, columnspan=2)
        tk.Label(self, text='Condition', font='arial 12', fg='blue').grid(row=1, column=0)

        # Entry
        self.entry_condition = tk.Entry(self, textvariable=self.condition, font='calibri 12')
        self.entry_condition.grid(row=1, column=1)

        # Button
        tk.Button(self, text='Remove', font='arial 13', command=self.remove_data, bg='red', relief='groove').grid(row=2, column=1)


############################
# Item Filter Wizard
############################
class ItemFilterWizard(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        # Properties
        self.title('Item Wizard')
        self.iconbitmap('icon.ico')
        self.width = 240
        self.height = 250
        self.geometry(f'{self.width}x{self.height}')
        self.minsize(self.width, self.height)
        self.maxsize(self.width, self.height)

        # Entry Variable
        self.type = tk.BooleanVar()
        self.company = tk.BooleanVar()
        self.price = tk.BooleanVar()
        self.detail = tk.BooleanVar()
        self.sell_date = tk.BooleanVar()
        self.condition = tk.StringVar()

        # Function call
        self.__appearance()

    def filter_data(self) -> None:
        """ Filter data in database """
        # Reload Actual Attributes
        self.master.reload_items_attributes()

        # Filter Attributes
        if not self.type.get() and Item.header()[1] in self.master.items_attributes:
            self.master.items_attributes.remove(Item.header()[1])
        elif Item.header()[1] not in self.master.items_attributes:
            self.master.items_attributes.append(Item.header()[1])

        if not self.company.get() and Item.header()[2] in self.master.items_attributes:
            self.master.items_attributes.remove(Item.header()[2])
        elif Item.header()[2] not in self.master.items_attributes:
            self.master.items_attributes.append(Item.header()[2])

        if not self.price.get() and Item.header()[3] in self.master.items_attributes:
            self.master.items_attributes.remove(Item.header()[3])
        elif Item.header()[3] not in self.master.items_attributes:
            self.master.items_attributes.append(Item.header()[3])

        if not self.detail.get() and Item.header()[4] in self.master.items_attributes:
            self.master.items_attributes.remove(Item.header()[4])
        elif Item.header()[4] not in self.master.items_attributes:
            self.master.items_attributes.append(Item.header()[4])

        if not self.sell_date.get() and Item.header()[5] in self.master.items_attributes:
            self.master.items_attributes.remove(Item.header()[5])
        elif Item.header()[5] not in self.master.items_attributes:
            self.master.items_attributes.append(Item.header()[5])

        self.master.items_condition = self.condition.get().strip()

        try:
            # Load data
            self.master.load_treeview_data()

            # Destroy the wizard window
            self.destroy()

            # Message
            tmsg.showinfo('Filter Wizard', 'Your data has been filtered successfully')
        except sq.OperationalError:
            # Error Message
            tmsg.showerror('Filter Wizard', f'You\'ve entered invalid condition. Your condition is "{self.master.items_condition}".')

            # Reload Actual Attributes
            self.master.reload_items_attributes()

            # Load data
            self.master.load_treeview_data()

    def __appearance(self) -> None:
        # Labels
        tk.Label(self, text='Select Attributes to Filter', font='arial 15', fg='blue', bg='orange').grid(row=0, column=0, columnspan=2)
        tk.Label(self, text='Type', font='arial 12', fg='blue').grid(row=1, column=0)
        tk.Label(self, text='Company', font='arial 12', fg='blue').grid(row=2, column=0)
        tk.Label(self, text='Price', font='arial 12', fg='blue').grid(row=3, column=0)
        tk.Label(self, text='Detail', font='arial 12', fg='blue').grid(row=4, column=0)
        tk.Label(self, text='Sell Date', font='arial 12', fg='blue').grid(row=5, column=0)
        tk.Label(self, text='Condition', font='arial 12', fg='blue').grid(row=6, column=0)

        # Entry
        self.check_type = tk.Checkbutton(self, variable=self.type, font='calibri 12')
        self.check_type.grid(row=1, column=1)

        self.check_company = tk.Checkbutton(self, variable=self.company, font='calibri 12')
        self.check_company.grid(row=2, column=1)

        self.check_price = tk.Checkbutton(self, variable=self.price, font='calibri 12')
        self.check_price.grid(row=3, column=1)

        self.check_detail = tk.Checkbutton(self, variable=self.detail, font='calibri 12')
        self.check_detail.grid(row=4, column=1)

        self.check_sell_date = tk.Checkbutton(self, variable=self.sell_date, font='calibri 12')
        self.check_sell_date.grid(row=5, column=1)

        self.entry_condition = tk.Entry(self, textvariable=self.condition, font='calibri 12')
        self.entry_condition.grid(row=6, column=1)

        # Button
        tk.Button(self, text='Filter', font='arial 13', command=self.filter_data, bg='green', relief='groove').grid(row=7, column=1)


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
        self.items_attributes = list(Item.header())
        self.customers_attributes = list(Customer.header())
        self.items_condition: str = ''
        self.customers_condition: str = ''

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

    def reload_items_attributes(self) -> None:
        """ Reload attributes of Item """
        self.items_attributes = list(Item.header())
        self.items_condition = ''

    def reload_customers_attributes(self) -> None:
        """ Reload attributes of Customer """
        self.customers_attributes = list(Customer.header())
        self.customers_condition = ''

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
        update_wizard = ItemUpdateWizard(self)
        update_wizard.grab_set()

    def update_customers(self) -> None:
        update_wizard = CustomerUpdateWizard(self)
        update_wizard.grab_set()

    def remove_items(self) -> None:
        remove_wizard = ItemRemoveWizard(self)
        remove_wizard.grab_set()

    def remove_customers(self) -> None:
        remove_wizard = CustomerRemoveWizard(self)
        remove_wizard.grab_set()

    def filter_items(self) -> None:
        filter_wizard = ItemFilterWizard(self)
        filter_wizard.grab_set()

    def filter_customers(self) -> None:
        tmsg.showinfo('Filter', 'The customers data has been filtered successfully')

    def create_menus(self) -> None:
        """ To create menus and sub-menus """
        # Main Bar
        menu_bar = tk.Menu(self)

        # File Menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Reload", command=self.reload_treeview_data)
        file_menu.add_command(label="Save to Excel", command=self.save_to_excel)
        file_menu.add_separator()  # Add a separator line
        file_menu.add_command(label="Exit", command=exit)

        # Action Menu
        action_menu = tk.Menu(menu_bar, tearoff=0)
        action_menu.add_command(label="Insert Item", command=self.add_item)
        action_menu.add_command(label="Insert Customer", command=self.add_customer)
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
        query: str = f"SELECT {', '.join(self.items_attributes)} FROM items"
        if len(self.items_condition) > 0:
            query += f" WHERE {self.items_condition}"
        # print(query)
        cursor.execute(query)
        for row in cursor.fetchall():
            self.__tree_items.insert('', 'end', values=row)

        query = f"SELECT {', '.join(self.customers_attributes)} FROM customers"
        if len(self.customers_condition) > 0:
            query += f" WHERE {self.customers_condition}"
        # print(query)
        cursor.execute(query)
        for row in cursor.fetchall():
            self.__tree_customers.insert('', 'end', values=row)

         # Message
        # tmsg.showinfo('Reload', 'The data has been reloaded successfully')

    def reload_treeview_data(self) -> None:
        """ To load data in tree-view with default values """
        self.reload_items_attributes()
        self.reload_customers_attributes()
        self.load_treeview_data()
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
