import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tmsg
import sqlite3 as sq


#################
# Time class
#################
class Time:
    def __init__(self, hour: int, minute: int, second: int):
        self.__hour: int = hour if 24 > hour >= 0 else 0
        self.__minute: int = minute if 60 > minute >= 0 else 0
        self.__second: int = second if 60 > second >= 0 else 0

    # * Getters
    @property
    def hour(self) -> int:
        return self.__hour

    @property
    def minute(self) -> int:
        return self.__minute

    @property
    def second(self) -> int:
        return self.__second

    # * Representation
    def __repr__(self) -> str:
        return f'{self.__hour}:{self.__minute}:{self.__second}'

