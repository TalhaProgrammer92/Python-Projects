#####################################################################################################3
# NOTE: Program to calculate age of a person in years, months and days
#####################################################################################################3

# TODO: Check for leap year
isLeapYear = lambda year : True if year % 4 == 0 else False
isValidYear = lambda year : True if year > 0 else False
isValidMonth = lambda month : True if month > 0 and month <= 12 else False
isValidDay = lambda day : True if day > 0 and day <= 31 else False

# TODO: Check if the date is valid or not
def isValidDate(year: int, month: int, day: int) -> bool:
    # INFO: Validity flag
    flag = False
    
    # INFO: Normal check
    if not isValidMonth(month) or not isValidDay(day) or not isValidYear(year):
        return flag
    
    # INFO: Leap year check (February)
    if isLeapYear(year):
        if month == 2:
            flag = True if day <= 29 else False
        else:
            flag = True if day <= 31 else False
    else:
        if month == 2:
            flag = True if day <= 28 else False

    # INFO: Month and day check
    if month in [1, 3, 5, 7, 8, 10, 12]:
        flag = True if day <= 31 else False
    elif month in [4, 6, 9, 11]:
        flag = True if day <= 30 else False

    return flag


# INFO: Date class
class Date:
    def __init__(self) -> None:
        self.__year = None
        self.__month = None
        self.__day = None

    @property
    def year(self) -> int:
        return self.__year

    @property
    def month(self) -> int:
        return self.__month

    @property
    def day(self) -> int:
        return self.__day
    
    @year.setter
    def year(self, value: int) -> None:
        if isValidYear(value):
            self.__year = value

    @month.setter
    def month(self, value: int) -> None:
        if isValidMonth(value):
            self.__month = value

    @day.setter
    def day(self, value: int) -> None:
        if isValidDay(value):
            self.__day = value

    # TODO: Set the date
    def set(self, year, month, day) -> None:
        if isValidDate(year, month, day):
            self.__year = year
            self.__month = month
            self.__day = day

    # TODO: Formatted output
    def __repr__(self) -> str:
        return f"{self.year}/{self.month}/{self.day}"

# TODO: Calculate age
def calculateAge(birth: Date, current: Date) -> Date:
    age = Date()
    
    # INFO: Calculate year
    age.year = current.year - birth.year
    
    # INFO: Calculate month
    age.month = abs(current.month - birth.month)
    
    # INFO: Calculate day
    age.day = abs(current.day - birth.day)
    
    return age

# INFO: Test the code
if __name__ == "__main__":
    birth_date = Date()
    current_date = Date()

    birth_date.set(2005, 9, 6)
    current_date.set(2024, 11, 16)

    age_date = calculateAge(birth_date, current_date)

    print(birth_date, current_date, age_date, sep='\n')
