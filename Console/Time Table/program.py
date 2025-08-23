import sqlite3 as sq
import string


#############################################
# ? Time Class - Handles time for events
#############################################
class Time:
    # * Constructor
    def __init__(self, **kwargs):
        self.__seconds: int = 0
        self.__minutes: int = 0
        self.__hours: int = 0
        self.__day_night: list[str] = ['AM', 'PM']
    
    # * Getters
    @property
    def seconds(self) -> int:
        return self.__seconds
    
    @property
    def minutes(self) -> int:
        return self.__minutes
    
    @property
    def hours(self) -> int:
        return self.__hours
    
    # * Setters
    @seconds.setter
    def seconds(self, value: int):
        if 0 <= value < 60:
            self.__seconds = value
    
    @minutes.setter
    def minutes(self, value: int):
        if 0 <= value < 60:
            self.__minutes = value
    
    @hours.setter
    def hours(self, value: int):
        if 0 <= value < 24:
            self.__hours
    
    # * Representation method
    def __repr__(self) -> str:
        return f'{self.seconds}:{self.minutes}:{self.hours}'


###############################################
# ? Event Class - Handles different events
###############################################
class Event:
    # * COnstructor
    def __init__(self, **kwargs):
        self.__event: str | None = kwargs.get('event', None)
        self.__start_time: Time = kwargs.get('start_time', Time())
        self.__end_time: Time = kwargs.get('end_time', Time())


###################
# ? Main Entry
###################
def main() -> None:
    time = Time()
    
    time.seconds = 15
    time.minutes = 30
    time.hours = 2
    
    print(time)

if __name__ == '__main__':
    main()
