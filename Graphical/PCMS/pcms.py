import tkinter as tk
import tkinter.messagebox as tmsg
import sqlite3 as sq
from os.path import exists, join
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
        self.customer_id: int | None = None
        self.sell_date: str | None = None

    @property
    def data(self) -> tuple:
        return (
            self.id,
            self.type,
            self.company,
            self.price,
            self.details,
            self.customer_id if self.customer_id is not None else 'None',
            self.sell_date if self.sell_date is not None else 'None'
        )

    @property
    def header(self) -> tuple:
        return (
            'id',
            'type',
            'company',
            'price',
            'details',
            'customer_id',
            'sell_date'
        )

    def sell(self, customer) -> None:
        """ Sell the item to a customer """
        self.sell_date = get_current_datetime()
        self.customer_id = customer.id

        customer.item_id = self.id
        customer.purchase_date = self.sell_date

    def __repr__(self) -> str:
        """ To represent the object as string """
        repr_: str = ''

        # Adding data
        for i in range(len(self.header)):
            repr_ += self.header[i].capitalize() + f' {'-' * 5} ' + str(self.data[i]) + '\n'

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
    def data(self) -> tuple:
        return (
            self.id,
            self.name,
            self.contact,
            self.item_id if self.item_id is not None else 'None',
            self.purchase_date if self.purchase_date is not None else 'None'
        )

    @property
    def header(self) -> tuple:
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
        for i in range(len(self.header)):
            repr_ += self.header[i].capitalize() + f' {'-' * 5} ' + str(self.data[i]) + '\n'

        return repr_


##################
# DBMS
##################
class DataBase:
    def __init__(self):
        self.database = sq.connect('data.db')
        self.cursor = self.database.cursor()
        self.__pre_process()

    def insert_data(self, table_name: str, data: tuple) -> None:
        """ Insert data in table """
        self.cursor.execute(f"""
        INSERT INTO {table_name} VALUES {data}
        """)

    def __pre_process(self) -> None:
        """ Create important tables """
        try:
            item_header: tuple = Item().header
            '''
                    'id',
                    'type',
                    'company',
                    'price',
                    'details',
                    'customer_id',
                    'sell_date'
            '''
            customer_header: tuple = Customer().header
            '''
                    'id',
                    'name',
                    'contact',
                    'item_id',
                    'purchase_date'
            '''

            # Tables Creation
            self.cursor.execute(f"""
            CREATE TABLE items (
                    -- Header
                    {item_header[0]} INTEGER PRIMARY KEY,
                    {item_header[1]} TEXT,
                    {item_header[2]} TEXT,
                    {item_header[3]} INTEGER,
                    {item_header[4]} TEXT,
                    {item_header[5]} INTEGER,
                    {item_header[6]} TEXT
            )

            CREATE TABLE customer (
                    -- Header
                    {item_header[0]} INTEGER PRIMARY KEY,
                    {item_header[1]} TEXT,
                    {item_header[2]} TEXT,
                    {item_header[3]} INTEGER,
                    {item_header[4]} TEXT,
            )
            """)
        except Exception as e:
            print(f'Tables already created\n')


##################
# Testing
##################
if __name__ == '__main__':
    item: Item = Item(1, 'Laptop', 'Lenovo', 25000, 'i5 4th Generation')

    customer: Customer = Customer(3, 'Talha Ahmad', '+92 331 4650460')

    item.sell(customer)

    print(item, customer, sep='\n')
