class Time:
    def __init__(self, hours: int, minutes: int, seconds: int):
        self.__hours: int = hours
        self.__minutes: int = minutes
        self.__seconds: int = seconds

    @property
    def hours(self) -> int:
        return self.__hours

    @property
    def minutes(self) -> int:
        return self.__minutes

    @property
    def seconds(self) -> int:
        return self.__seconds

    @property
    def total_seconds(self) -> int:
        return self.seconds + self.minutes * 60 + self.hours * 3600

    @property
    def total_minutes(self) -> int:
        return self.minutes + self.hours * 60

    @property
    def total_hours(self):
        return self.hours

    @staticmethod
    def get_minutes(seconds: int) -> int:
        minutes: int = seconds % 60
        return minutes, abs(int(minutes / 60) - seconds)

    @staticmethod
    def get_hours(seconds: int) -> int:
        hours: int = seconds % 3600
        return hours, abs(int(hours / 3600) - seconds)

    def __repr__(self):
        return '{}:{}:{}'.format(self.hours, self.minutes, self.seconds)


class Math:
    @staticmethod
    def add(*args: Time) -> Time:
        """ Add time """
        seconds: int = 0
        for t in args:
            seconds += t.total_seconds
        minutes, seconds = Time.get_minutes(seconds)
        hours, seconds = Time.get_hours(seconds)

        return Time(hours, minutes, seconds)


if __name__ == '__main__':
    # sum_: Time = Math.add(
    #     Time(0, 37, 13),
    #     Time(0, 32, 52),
    #     Time(0, 20, 56),
    #     Time(0, 29, 33),
    #     Time(0, 20, 49),
    #     Time(0, 18, 27),
    #     Time(0, 16, 42)
    # )

    a: Time = Time(0, 5, 15)
    b: Time = Time(0, 3, 45)

    sum_: Time = Math.add(a, b)

    # print(a.total_seconds, a.total_minutes, a.total_hours)
    print(sum_)
