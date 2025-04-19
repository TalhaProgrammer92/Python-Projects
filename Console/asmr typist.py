from time import sleep
from pynput.keyboard import Key, Controller
from string import ascii_letters, punctuation, digits
from os.path import exists

##############
# Functions
##############

#* Typing Speed Estimation:
#* Characters per second:  11.36 ~ 11
#* Characters per minute:  681.6 ~ 682
def press(key: str | Key) -> None:
    keyboard.press(key)
    keyboard.release(key)
    sleep(delay / speed)

#* Get text from file
#* If file does not exist, exit the program
def get_text(location: str) -> str:
    if exists(location):
        with open(location, 'r') as file:
            return file.read()
    exit()

#* Print time estimation for typing the text
#* Calculate number of seconds the bot would take to type
def print_time_estimation(text: str):
    """ Calculate number of seconds the bot would take to type """
    seconds = (len(text) / 682) * 60
    minutes = ((len(text) / 682) * 60) // 60

    if minutes == 0:
        print(f'It\'d take {seconds:.2f} seconds for me to type.')
    else:
        print(f'It\'d take {int(minutes)} minutes for me to type.')

##############
# Variables
##############

#* Keyboard controller
keyboard: Controller = Controller()

#* Get text from file
text: str = get_text(input('Enter complete path of the text file you want to write from bot>> '))

#* Print time estimation for typing the text
print_time_estimation(text)
delay: float = 0.3      # Delay between each character
speed: int = 4          # Typing speed multiplier (4 is normal speed)
legals: str = ascii_letters + punctuation + digits
hold: int = 5           # Hold for few seconds before start typing

##############
# Typing
##############
print(f'Starting in {hold} sec...')
sleep(hold)
for character in text:
    # Normal Text
    if character in legals:
        press(character)

    # Escape Sequence and whitespace
    elif character == ' ':
        press(Key.space)
    elif character == '\t':
        press(Key.tab)
    elif character == '\b':
        press(Key.backspace)
    elif character == '\n':
        press(Key.enter)