import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tmsg
import sqlite3 as sq

#######################
# Global Variables
#######################
DAYS: tuple = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')


#################
# Time class
#################
class Time:
    def __init__(self, hour: int, minute: int, second: int = 0):
        self.hour: int = hour if 24 > hour >= 0 else 0
        self.minute: int = minute if 60 > minute >= 0 else 0
        self.second: int = second if 60 > second >= 0 else 0

    # * Representation
    def __repr__(self) -> str:
        return f'{self.hour}:{self.minute}:{self.second}'


##################
# Event class
##################
class Event:
    def __init__(self, name: str, start_time: Time, end_time: Time):
        self.name: str = name if len(name) > 0 and not name.isspace() else 'Unknown'
        self.start_time: Time = start_time
        self.end_time: Time = end_time
        self.__days: list = []

    @property
    def days(self) -> list:
        return self.__days

    # * Add days
    def add_day(self, day: str) -> None:
        if day not in self.__days and day in DAYS:
            self.__days.append(day)

    # * Representation
    def __repr__(self) -> str:
        return f"""Event - {self.name}
Start: {self.start_time.__repr__()}
End: {self.end_time.__repr__()}
Days: {', '.join([day for day in self.__days]) if len(self.__days) > 0 else 'None'}\n"""


##############
# Testing
##############
if __name__ == '__main__':
    events: list = [
        Event('Breakfast', Time(8, 0), Time(8, 30)),
        Event('Code', Time(9, 0), Time(11, 0))
    ]

    for i in range(2):
        # events[0].add_day(DAYS[i])
        events[1].add_day(DAYS[i])

    for event in events:
        print(event)
