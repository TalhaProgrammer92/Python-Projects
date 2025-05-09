import time as t
import PyMisc.csv_handler as csv

# Time
class Time:
    def __init__(self, start, end):
        self.start = start
        self.end = end

# Event
class Event:
    def __init__(self, name: str, time: Time, details: str = ''):
        self.name: str = name
        self.time: Time = time
        self.details: str = details

    @staticmethod
    def header(self) -> list:
        return ['name', 'start_time', 'end_time', 'details']

    def __repr__(self) -> str:
        event: str = f'Name: {self.name} --- Start: {self.time.start} --- End: {self.time.end}'
        if len(self.details) > 0:
            event += f' --- Detail: {self.details}'
        return event

# Table
class Table:
    def __init__(self):
        self.events: list[Event] = []

    def add_event(self, event: Event) -> None:
        self.events.append(event)

    def display_all(self):
        for event in self.events:
            print(event)


if __name__ == '__main__':
    time_table: Table = Table()

    # time_table.add_event(Event('Code', Time(t.time(), t.strftime('%hh:%mm:%ss'))))
