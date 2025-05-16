# Importing necessary modules
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tmsg
import PyMisc.number as number
from PyMisc.variable import resolution


##################
# Main Window
##################
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        ################################
        # Window properties settings
        ################################

        # Resolution / Size
        self.resolution: resolution = resolution(350, 350)
        self.geometry("{}x{}".format(self.resolution.width, self.resolution.height))
        self.minsize(self.resolution.width, self.resolution.height)
        self.maxsize(self.resolution.width, self.resolution.height)

        # Title
        self.title("Number System")

        # Variables
        self.numbers = [
            number.Custom('', 10, 'decimal'),
            number.Custom('', 2, 'binary'),
            number.Custom('', 8, 'octal'),
            number.Custom('', 16, 'hexadecimal')
        ]
        self.numbers_names = self.get_numbers_names_list()
        self.entry = tk.StringVar()
        self.combo_from = ttk.Combobox(self, values=self.numbers_names, state="readonly")
        self.combo_to = ttk.Combobox(self, values=self.numbers_names, state="readonly")

        # Dictionary
        self.system: dict = {}
        for num in self.numbers:
            self.system[num.name] = num

        # Function call
        self.__appearance()

    def get_numbers_names_list(self) -> list[str]:
        """ Get list of numbers' names """
        options = []
        for num in self.numbers:
            # print(number.name)
            options.append(num.name.capitalize())
        return options

    def convert_number(self) -> None:
        """ To convert the given number """
        entry: str = self.entry.get().strip()

        if len(entry) > 0:
            # Error - Unsupported floating point number
            if '.' in entry:
                # Messagebox
                tmsg.showerror('Float Error', 'Floating point numbers are not supported.')

                # Reset the entry
                self.entry.set("")
                return

            # Get ComboBox options
            _from = self.combo_from.get().lower()
            _to = self.combo_to.get().lower()

            # If both options are same
            if _from == _to:
                tmsg.showerror('Conversion Error', 'You have selected same conversion type as the other number.')
                return

            # If the number is not valid according to its base
            if not number.is_valid(entry, self.system[_from].base):
                tmsg.showerror('Value Error', 'The number you have entered is incorrect')
                return

            # Conversion
            result = number.convert(number.Custom(entry, self.system[_from].base), self.system[_to].base).value

            # Reset the entry
            self.entry.set(result)
        else:
            # Messagebox
            tmsg.showerror("Value Error", "You must enter a value before performing any conversion operation")

    def __appearance(self) -> None:
        """ Set appearance of the window """
        # Label
        tk.Label(self, text="Number System Convertor", bg="blue", fg="yellow", font=("candara", 20, "bold")).pack(
            fill=tk.X)

        # Entry
        tk.Entry(self, textvariable=self.entry, bg="silver", fg="green", font=("segoe ui", 15, "bold")).pack(fill=tk.X,
                                                                                                             padx=15,
                                                                                                             pady=15)

        # Combo box
        tk.Label(self, text="Select to convert from", bg="cyan", fg="black", font=("candara", 10, "bold")).pack(
            fill=tk.X, pady=10)

        self.combo_from.set(self.numbers_names[0])
        self.combo_from.pack(padx=5, pady=5)

        tk.Label(self, text="Select to convert to", bg="cyan", fg="black", font=("candara", 10, "bold")).pack(fill=tk.X,
                                                                                                              pady=10)
        self.combo_to.set(self.numbers_names[0])
        self.combo_to.pack(padx=5, pady=5)

        # Button
        tk.Button(self, text="Convert", bg="yellow", fg="blue", font=("candara", 20, "bold"), relief="groove",
                  command=self.convert_number).pack(padx=25, pady=25)


##################
# Testing
##################
if __name__ == '__main__':
    window = MainWindow()
    window.mainloop()
