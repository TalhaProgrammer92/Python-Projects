from random import randint

PROCESS_COUNT: int = 0

class Process:
    def __init__(self, **kwargs):
        global PROCESS_COUNT
        PROCESS_COUNT += 1
        self.__id: int = PROCESS_COUNT
        self.__name: str = kwargs.get('name', f'P-{PROCESS_COUNT}')

        self.__arrival_time: int = kwargs.get('arrival_time', randint(1, PROCESS_COUNT * 2))
        self.__burst_time: int = kwargs.get('burst_time', randint(1, int(PROCESS_COUNT * 1.5)))
        self.completion_time: int = kwargs.get('completion_time', randint(1, int(PROCESS_COUNT * 1.25)))
        self.first_cpu_time: int = kwargs.get('first_cpu_time', randint(1, int(PROCESS_COUNT * 2.125)))

    # Getters
    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def arrival_time(self) -> int:
        return self.__arrival_time

    @property
    def burst_time(self) -> int:
        return self.__burst_time

    @property
    def turn_around_time(self) -> int:
        return abs(self.completion_time - self.arrival_time)

    @property
    def waiting_time(self) -> int:
        return abs(self.turn_around_time - self.burst_time)

    @property
    def response_time(self) -> int:
        return abs(self.first_cpu_time - self.arrival_time)

    def __repr__(self) -> str:
        return f"""{'*' * 10} {self.name} {'*' * 10}
Arrival Time:       {self.arrival_time}
Burst Time:         {self.burst_time}
Completion Time:    {self.completion_time}
Turn Around Time:   {self.turn_around_time}
Waiting Time:       {self.waiting_time}
Response Time:      {self.response_time}"""


class GanttChart:
    def __init__(self):
        self.__processes: list[Process] = []

    def add_process(self, process: Process, first_cpu_time: int):
        process.first_cpu_time = first_cpu_time
        process.completion_time = first_cpu_time + process.burst_time
        self.__processes.append(process)

    @property
    def process(self) -> list[Process]:
        return self.__processes

def first_come_first_serve(process_queue: list[Process]) -> GanttChart:
    pass

if __name__ == '__main__':
    processes: list[Process] = [Process() for i in range(5)]
    for process in processes:
        print(process)
