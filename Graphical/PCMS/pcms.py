import tkinter as tk
import tkinter.messagebox as tmsg
import sqlite3 as sq
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
# Testing
##################
if __name__ == '__main__':
    pass