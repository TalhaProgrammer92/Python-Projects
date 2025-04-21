import tkinter as tk
from tkinter import font, messagebox
import math

class AdvancedCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DevCode Journey")
        self.root.geometry("400x650")
        self.root.resizable(False, False)
        self.root.configure(bg="#2E3440")

        self.expression_font = font.Font(family="Helvetica", size=18)
        self.result_font = font.Font(family="Helvetica", size=28, weight="bold")
        self.button_font = font.Font(family="Helvetica", size=16)
        
        self.create_widgets()
        self.create_menu()
        
        self.current_expression = ""
        self.full_expression = ""
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        about_menu = tk.Menu(menubar, tearoff=0)
        about_menu.add_command(label="About", command=self.show_about)
        about_menu.add_command(label="Exit", command=self.root.quit)
        
        menubar.add_cascade(label="Menu", menu=about_menu)
        self.root.config(menu=menubar)
    
    def show_about(self):
        messagebox.showinfo("About", "Subscribe to DevCode Jurney")
    
    def create_widgets(self):

        display_frame = tk.Frame(self.root, bg="#3B4252")
        display_frame.pack(pady=20, padx=20, fill=tk.BOTH)

        self.expression_display = tk.Label(
            display_frame, 
            text="", 
            anchor=tk.E, 
            bg="#3B4252", 
            fg="#D8DEE9", 
            font=self.expression_font,
            padx=20,
            pady=10,
            height=1
        )
        self.expression_display.pack(fill=tk.BOTH)

        self.result_display = tk.Label(
            display_frame, 
            text="0", 
            anchor=tk.E, 
            bg="#3B4252", 
            fg="#ECEFF4", 
            font=self.result_font,
            padx=20,
            pady=20
        )
        self.result_display.pack(fill=tk.BOTH)

        button_frame = tk.Frame(self.root, bg="#2E3440")
        button_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        buttons = [
            ('C', '(', ')', '/', '√'),
            ('7', '8', '9', '*', 'x²'),
            ('4', '5', '6', '-', 'sin'),
            ('1', '2', '3', '+', 'cos'),
            ('0', '.', 'π', '=', 'tan')
        ]
        
        for i, row in enumerate(buttons):
            for j, button_text in enumerate(row):
                button = tk.Button(
                    button_frame,
                    text=button_text,
                    font=self.button_font,
                    bg="#4C566A" if button_text not in ['=', 'C'] else ("#BF616A" if button_text == 'C' else "#A3BE8C"),
                    fg="#ECEFF4",
                    activebackground="#5E81AC",
                    activeforeground="#ECEFF4",
                    relief=tk.FLAT,
                    command=lambda text=button_text: self.on_button_click(text)
                )
                button.grid(row=i, column=j, padx=5, pady=5, sticky=tk.NSEW)
                button_frame.grid_columnconfigure(j, weight=1)
            button_frame.grid_rowconfigure(i, weight=1)
    
    def on_button_click(self, button_text):
        if button_text == 'C':
            self.current_expression = ""
            self.full_expression = ""
            self.update_displays()
        elif button_text == '=':
            self.calculate_result()
        elif button_text == '√':
            exp = self.current_expression
            self.current_expression = ""
            self.append_operator(f'sqrt({exp})')
        elif button_text == 'x²':
            self.append_operator('**2')
        elif button_text == 'π':
            self.append_operator(str(math.pi))
        elif button_text in ['sin', 'cos', 'tan']:
            exp = self.current_expression
            self.current_expression = ""
            self.append_operator(f'{button_text}(radians({exp}))')
        else:
            self.append_operator(button_text)
    
    def append_operator(self, operator):
        if operator in ['+', '-', '*', '/']:
            if self.current_expression and self.current_expression[-1] not in ['+', '-', '*', '/']:
                self.full_expression += self.current_expression + " " + operator + " "
                self.current_expression = ""
            elif self.current_expression and self.current_expression[-1] in ['+', '-', '*', '/']:
                self.full_expression = self.full_expression[:-3] + " " + operator + " "
        else:
            self.current_expression += operator
        
        self.update_displays()
    
    def update_displays(self):
        self.expression_display.config(text=self.full_expression + self.current_expression)
        self.result_display.config(text=self.current_expression or "0")
    
    def calculate_result(self):
        try:
            expression = self.full_expression + self.current_expression
            if not expression:
                return
            
            expression = expression.replace('π', 'math.pi')
            # expression = expression.replace('math.sin(math.radians', 'math.sin')
            # expression = expression.replace('math.cos(math.radians', 'math.cos')
            # expression = expression.replace('math.tan(math.radians', 'math.tan')
            
            result = eval(expression, {"__builtins__": None}, {
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "sqrt": math.sqrt,
                # "pi": math.pi,
                "radians": math.radians
            })
            
            self.full_expression = expression + " = "
            self.current_expression = str(result)
            self.update_displays()
            
            
            self.full_expression = ""
        except Exception as e:
            messagebox.showerror("Error", "Invalid Expression")
            self.current_expression = ""
            self.full_expression = ""
            self.update_displays()

if __name__ == "__main__":
    # # Let’s say you want to evaluate this expression:
    # expression = "sin(radians(8))"  # Converting degrees to radians
    #
    # # eval() needs access to the math functions, so pass them as globals
    # result = eval(expression, {"__builtins__": None}, {
    #     "sin": math.sin,
    #     "cos": math.cos,
    #     "tan": math.tan,
    #     "sqrt": math.sqrt,
    #     "pi": math.pi,
    #     "radians": math.radians
    # })
    #
    # print(result)

    root = tk.Tk()
    app = AdvancedCalculatorApp(root)
    root.mainloop()
