import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tmsg
import sqlite3 as sq


#################
# Time class
#################
class Time:
    def __init__(self, hour: int, minute: int, second: int):
        self.__hour: int = hour
        self.__minute: int = minute
        self.__second: int = second

    # * Getters
    @property
    def hour(self) -> int:
        return self.__hour
