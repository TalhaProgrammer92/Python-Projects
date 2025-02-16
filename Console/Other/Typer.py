from PyMisc.variable import constant
from time import sleep
from pynput.keyboard import Key, Controller
from string import ascii_letters, punctuation, digits
from os.path import exists

'''
Typing Speed Estimation:

Characters per second:  11.36 ~ 11
Characters per minute:  681.6 ~ 682
'''

##############
# Function
##############
def press(key: str | Key) -> None:
    keyboard.press(key)
    keyboard.release(key)
    sleep(delay.value / speed.value)

def get_text(location: str) -> str:
    if exists(location):
        with open(location, 'r') as file:
            return file.read()
    exit()

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
keyboard: Controller = Controller()
text: str = get_text(input('Enter complete path of the text file you want to write from bot>> '))
print_time_estimation(text)
delay: constant = constant(0.3)     # Delay between each character
speed: constant = constant(8)       # Typing speed multiplier
legals: constant = constant(ascii_letters + punctuation + digits)
hold: constant = constant(5)            # Hold for few seconds before start typing


##############
# Typing
##############
print(f'Starting in {hold.value} sec...')
sleep(hold.value)
for character in text:
    # Normal Text
    if character in legals.value:
        press(character)

    # Escape Sequence and whitespace
    elif character == ' ':
        press(Key.space)
    elif character == '\t':
        press(Key.tab)
    elif character == '\n':
        press(Key.enter)
