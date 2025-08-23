import sqlite3 as sq
import string


# * Function - Get double digit value
def double_digit_value(value: int) -> str | None:
    if value > 99: return None
    
    return f"{value:02}" if value <= 9 else str(value)

#############################################
# ? Time Class - Handles time for events
#############################################
class Time:
    # * Constructor
    def __init__(self, **kwargs):
        seconds, minutes, hours = kwargs.get('seconds', 0), kwargs.get('minutes', 0), kwargs.get('hours', 0)
        
        self.__seconds: int = seconds if self.is_seconds_valid(seconds) else 0
        self.__minutes: int = minutes if self.is_minutes_valid(minutes) else 0
        self.__hours: int = hours if self.is_hours_valid(hours) else 0
    
    # * Methods - Check validity
    is_seconds_valid = lambda self, seconds : 0 <= seconds < 60 and isinstance(seconds, int)
    is_minutes_valid = lambda self, minutes : 0 <= minutes < 60 and isinstance(minutes, int)
    is_hours_valid = lambda self, hours : 0 <= hours < 24 and isinstance(hours, int)
    
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
        if self.is_seconds_valid(value):
            self.__seconds = value
    
    @minutes.setter
    def minutes(self, value: int):
        if self.is_minutes_valid(value):
            self.__minutes = value
    
    @hours.setter
    def hours(self, value: int):
        if self.is_hours_valid(value):
            self.__hours = value
    
    # * Representation method
    def __repr__(self) -> str:
        return f'{double_digit_value(self.hours)}:{double_digit_value(self.minutes)}' + (f':{double_digit_value(self.seconds)}' if self.seconds > 0 else '')


###############################################
# ? Event Class - Handles different events
###############################################
class Event:
    # * Constructor
    def __init__(self, **kwargs):
        self.event: str | None = kwargs.get('event', None)
        self.description: str | None = kwargs.get('description', None)
        self.start_time: Time = kwargs.get('start_time', Time())
        self.end_time: Time = kwargs.get('end_time', Time())
    
    # * Getter - As dictionary
    @property
    def get_dict(self) -> dict:
        return {
            'event': self.event,
            'description': self.description,
            'time': {
                'start': self.start_time,
                'end': self.end_time
            }
        }

    # * Representation method
    def __repr__(self) -> str:
        return f"Event:\t{self.event if self.event is not None else 'An Event'}\nStart:\t{self.start_time}\nEnd:\t{self.end_time}" + (f"\n- {self.description}" if self.description is not None else '')


####################################################
# ? EventsList Class - Handles a list of events
####################################################
class EventsList:
    # * Constructor
    def __init__(self, name: str):
        self.__events: list[Event] = []
        self.name: str = name
    
    # * Getters
    @property
    def events(self) -> list[Event]:
        return self.__events
    
    def get_event(self, event_name: str) -> Event | None:
        """
        TODO: This method get event name as parameter and find an even of same name in the list of events
        ? Return:
        1. Event - If an event found
        2. None - If no event found
        """
        
        # TODO: Finding the given event in the list
        for event in self.events:
            if event_name.lower() == event.event.lower():
                return event
        
        # ! If no event found
        return None

    # * Method - Add an event
    def add_event(self, event: Event) -> None:
        self.__events.append(event)
    
    # * Representation method
    def __repr__(self) -> str:
        return f"***** {self.name} *****\n" + "\n--------------------\n".join([event.__repr__() for event in self.events])


###################
# ? Main Entry
###################
def main() -> None:
    events: EventsList = EventsList('Monday')
    
    events.add_event(Event(
        event = 'Breakfast',
        description = 'Eat healthy',
        start_time = Time(hours = 10),
        end_time = Time(hours = 10, minutes = 30)
    ))
    
    events.add_event(Event(
        event = 'Gaming',
        description = 'Play video games',
        start_time = Time(hours = 10, minutes = 30),
        end_time = Time(hours = 12, minutes = 30)
    ))
    
    events.add_event(Event(
        event = 'Rest',
        start_time = Time(hours = 12, minutes = 30),
        end_time = Time(hours = 13, minutes = 30)
    ))
    
    print(events)

if __name__ == '__main__':
    main()
