import PyMisc.variable as var


####################
# Foreground
####################
class foreground:
    # Get color directly
    @staticmethod
    def black() -> str:
        return '\033[30m'

    @staticmethod
    def red() -> str:
        return '\033[31m'

    @staticmethod
    def green() -> str:
        return '\033[32m'

    @staticmethod
    def yellow() -> str:
        return '\033[33m'

    @staticmethod
    def blue() -> str:
        return '\033[34m'

    @staticmethod
    def magenta() -> str:
        return '\033[35m'

    @staticmethod
    def cyan() -> str:
        return '\033[36m'

    @staticmethod
    def white() -> str:
        return '\033[37m'

    @staticmethod
    def bright_black() -> str:
        return '\033[90m'

    @staticmethod
    def bright_red() -> str:
        return '\033[91m'

    @staticmethod
    def bright_green() -> str:
        return '\033[92m'

    @staticmethod
    def bright_yellow() -> str:
        return '\033[93m'

    @staticmethod
    def bright_blue() -> str:
        return '\033[94m'

    @staticmethod
    def bright_magenta() -> str:
        return '\033[95m'

    @staticmethod
    def bright_cyan() -> str:
        return '\033[96m'

    @staticmethod
    def bright_white() -> str:
        return '\033[97m'


####################
# Background
####################
class background:
    # Get color directly
    @staticmethod
    def black() -> str:
        return '\033[40m'

    @staticmethod
    def red() -> str:
        return '\033[41m'

    @staticmethod
    def green() -> str:
        return '\033[42m'

    @staticmethod
    def yellow() -> str:
        return '\033[43m'

    @staticmethod
    def blue() -> str:
        return '\033[44m'

    @staticmethod
    def magenta() -> str:
        return '\033[45m'

    @staticmethod
    def cyan() -> str:
        return '\033[46m'

    @staticmethod
    def white() -> str:
        return '\033[47m'

    @staticmethod
    def bright_black() -> str:
        return '\033[100m'

    @staticmethod
    def bright_red() -> str:
        return '\033[101m'

    @staticmethod
    def bright_green() -> str:
        return '\033[102m'

    @staticmethod
    def bright_yellow() -> str:
        return '\033[103m'

    @staticmethod
    def bright_blue() -> str:
        return '\033[104m'

    @staticmethod
    def bright_magenta() -> str:
        return '\033[105m'

    @staticmethod
    def bright_cyan() -> str:
        return '\033[106m'

    @staticmethod
    def bright_white() -> str:
        return '\033[107m'


####################
# Style
####################
class style:
    @staticmethod
    def bold() -> str:
        return '\033[1m'

    @staticmethod
    def dim() -> str:
        return '\033[2m'

    @staticmethod
    def italic() -> str:
        return '\033[2m'

    @staticmethod
    def under_line() -> str:
        return '\033[3m'

    @staticmethod
    def blink() -> str:
        return '\033[4m'

    @staticmethod
    def reverse() -> str:
        return '\033[5m'

    @staticmethod
    def hidden() -> str:
        return '\033[6m'


####################
# Property
####################
class property:
    def __init__(self, fg_color_code: str = None, bg_color_code: str = None, style_codes: list[str] = None):
        self.__foreground: var.constant = var.constant(fg_color_code if fg_color_code is not None else None)
        self.__background: var.constant = var.constant(bg_color_code if bg_color_code is not None else None)
        self.__styles: list[var.constant] = [var.constant(value) for value in style_codes] if style_codes is not None else None

    @staticmethod
    def is_correct_code(code: str) -> bool:
        return code[:5] == '\033[' and code[-1] == 'm'

    def __repr__(self) -> str:
        code: str = ''

        # Adding code
        if self.__foreground.value is not None: code += self.__foreground.value
        if self.__background.value is not None: code += self.__background.value
        if self.__styles is not None:
            for style in self.__styles:
                code += style.value

        return code


####################
# Functions
####################
def reset() -> str:
    return '\033[0m'

def print_colored(text: str, prop: property, end: str = '') -> None:
    print(prop, text, reset(), sep='', end=end)

"""
foreground_colors = {
    'black': '\033[30m',
    'red': '\033[31m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'blue': '\033[34m',
    'magenta': '\033[35m',
    'cyan': '\033[36m',
    'white': '\033[37m',
    'bright-black': '\033[90m',
    'bright-red': '\033[91m',
    'bright-green': '\033[92m',
    'bright-yellow': '\033[93m',
    'bright-blue': '\033[94m',
    'bright-magenta': '\033[95m',
    'bright-cyan': '\033[96m',
    'bright-white': '\033[97m',
}

background_colors = {
    'black': '\033[40m',
    'red': '\033[41m',
    'green': '\033[42m',
    'yellow': '\033[43m',
    'blue': '\033[44m',
    'magenta': '\033[45m',
    'cyan': '\033[46m',
    'white': '\033[47m',
    'bright-black': '\033[100m',
    'bright-red': '\033[101m',
    'bright-green': '\033[102m',
    'bright-yellow': '\033[103m',
    'bright-blue': '\033[104m',
    'bright-magenta': '\033[105m',
    'bright-cyan': '\033[106m',
    'bright-white': '\033[107m',
}

style_codes = {
    'bold': '\033[1m',
    'dim': '\033[2m',
    'italic': '\033[3m',
    'underline': '\033[4m',
    'blink': '\033[5m',
    'reverse': '\033[7m',
    'hidden': '\033[8m',
}
"""
