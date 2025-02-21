import tkinter as tk
from tkinter import messagebox

# Function for menu commands
def new_file():
    messagebox.showinfo("New File", "Create a new file")

def open_file():
    messagebox.showinfo("Open File", "Open an existing file")

def exit_app():
    root.quit()

# Create main application window
root = tk.Tk()
root.title("Tkinter Menu Example")
root.geometry("400x300")

# Create Menu Bar
menu_bar = tk.Menu(root)

# Create File Menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_separator()  # Add a separator line
file_menu.add_command(label="Exit", command=exit_app)

# Create Edit Menu
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Undo")
edit_menu.add_command(label="Redo")

# Add Menus to Menu Bar
menu_bar.add_cascade(label="File", menu=file_menu)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

# Configure the window to use this menu bar
root.config(menu=menu_bar)

# Run the application
root.mainloop()
