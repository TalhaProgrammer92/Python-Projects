import settings
import PyMisc.color as clr

########################
# Text Class
########################
class Text:
    def __init__(self, text: str, color: clr.property):
        self.__text: str = text
        self.__color: clr.property = color

    # Getters
    @property
    def text(self) -> str:
        return self.__text

    @property
    def color(self) -> clr.property:
        return self.__color

    # Representation method
    def __repr__(self) -> str:
        return clr.get_colored(self.text, self.color)

# Function to take input from user
def takeInput(message: Text) -> int:
    """ Take input from user """
    while True:
        try:
            num = int(input(message))
            break
        except Exception:
            continue
    return num


########################
# Message Class
########################
class Message:
    def __init__(self, text: Text):
        self.text: list[Text] = [text]

    # Getter - length
    @property
    def length(self) -> int:
        _len: int = 0

        # Accessing each element
        for element in self.text:
            _len += len(element.text) + 1
        _len -= 1

        return _len

    # Display method
    def display(self):
        """ This method is used to display message on console """
        for text in self.text:
            print(text, end=' ')


########################
# Error Message Class
########################
class ErrorMessage(Message):
    def __init__(self, text: str):
        super().__init__(Text(
            text,
            clr.property(
                clr.foreground.bright_red(),
                None,
                [clr.style.bold()])
        ))


########################
# Heading Class
########################
class Heading:
    def __init__(self, message: Message = Message(Text(settings.ui['text']['default']['text-content'], settings.ui['text']['default']['text-color'])), decorator: Text = Text(settings.ui['text']['default']['heading-symbol'], settings.ui['text']['default']['heading-color'][settings.theme[settings.theme_toggle]]), padding: int = 1):
        # Message attribute
        self.message: Message = message

        # Style Attributes
        self.__decorator: Text = decorator
        self.__padding: int = padding

    # Print line
    def printLine(self):
        length: int = self.message.length + self.__padding * 4
        for i in range(length):
            print(self.__decorator, end='')
        print()

    # Display method
    def display(self):
        """ This method overrides Message display method """
        self.printLine()

        print(self.__decorator, ' ' * self.__padding, end='', sep='')

        self.message.display()

        print(self.__decorator, ' ' * self.__padding, sep='')

        self.printLine()


########################
# Menu Class
########################
class Menu:
    def __init__(self, heading: Heading | None = None):
        self.heading: Heading | None = heading
        self.__options: list[Text] = []

    @property
    def options(self) -> list[Text]:
        return self.__options

    def addOption(self, option: Text) -> None:
        """ Method to add an option for the menu """
        self.__options.append(option)

    def display(self):
        """ Method to display menu """
        self.heading.display()
        print()

        for i in range(len(self.__options)):
            print(Text(str(i+1) + '.', clr.property(clr.foreground.bright_white())), self.__options[i])