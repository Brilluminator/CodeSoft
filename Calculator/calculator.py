# Importing the tkinter module
import tkinter as tk

# Function to add text to the entry field
def add_text_to_entry(text):
    current_text = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current_text + text)

# Function to calculate the result
def calculate():
    expression = entry.get()
    try:
        result = eval(expression)
        entry.delete(0, tk.END)
        entry.insert(0, str(result))
    except:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")

# Function to clear the entry field
def clear_entry():
    entry.delete(0, tk.END)

# Function to delete the last character in the entry field
def backspace():
    current_text = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current_text[:-1])

# Creating the main window
root = tk.Tk()
root.title("My Calculator")

# Setting the window size
root.geometry("322x534")

# Creating the entry field
entry = tk.Entry(root, font=("Arial", 40), bd=5, justify="right", relief="flat")
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

# Define colors
bg_color = "#333333"
btn_color = "#4d4d4d"
btn_hover_color = "#666666"
btn_active_color = "#999999"
btn_text_color = "#ffffff"

# Creating buttons for numbers
for i in range(1, 10):
    btn = tk.Button(root, text=str(i), font=("Arial", 24), bd=0, bg=btn_color, fg=btn_text_color, relief="flat",
                    activebackground=btn_hover_color, activeforeground=btn_text_color,
                    command=lambda i=i: add_text_to_entry(str(i)))
    btn.grid(row=(4 - (i-1) // 3), column=((i-1) % 3), padx=5, pady=5, sticky="nsew")

# Creating the zero button
btn_zero = tk.Button(root, text="0", font=("Arial", 24), bd=0, bg=btn_color, fg=btn_text_color, relief="flat",
                    activebackground=btn_hover_color, activeforeground=btn_text_color,
                    command=lambda: add_text_to_entry("0"))
btn_zero.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

# Creating the decimal point button
decimal_btn = tk.Button(root, text=".", font=("Arial", 24), bd=0, bg=btn_color, fg=btn_text_color, relief="flat",
                        activebackground=btn_hover_color, activeforeground=btn_text_color,
                        command=lambda: add_text_to_entry("."))
decimal_btn.grid(row=5, column=2, padx=5, pady=5, sticky="nsew")

# Creating buttons for arithmetic operations
operations = ['+', '-', '*', '/']
for i, op in enumerate(operations):
    btn = tk.Button(root, text=op, font=("Arial", 24), bd=0, bg=btn_color, fg=btn_text_color, relief="flat",
                    activebackground=btn_hover_color, activeforeground=btn_text_color,
                    command=lambda op=op: add_text_to_entry(op))
    btn.grid(row=i+1, column=3, padx=5, pady=5, sticky="nsew")

# Creating the equals sign button
equals_btn = tk.Button(root, text="=", font=("Arial", 20), bd=0, bg="#ff8800", fg=btn_text_color, relief="flat",
                       activebackground="#ff7700", activeforeground=btn_text_color,
                       command=calculate)
equals_btn.grid(row=5, column=3, padx=5, pady=5, sticky="nsew")

# Creating the clear button
clear_btn = tk.Button(root, text="C", font=("Arial", 24), bd=0, bg="#ff0000", fg=btn_text_color, relief="flat",
                      activebackground="#cc0000", activeforeground=btn_text_color,
                      command=clear_entry)
clear_btn.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

# Creating the backspace button
backspace_btn = tk.Button(root, text="←", font=("Arial", 24), bd=0, bg=btn_color, fg=btn_text_color, relief="flat",
                          activebackground=btn_hover_color, activeforeground=btn_text_color,
                          command=backspace)
backspace_btn.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")

# Configure row and column weights
for i in range(6):
    root.grid_rowconfigure(i, weight=1)
for i in range(4):
    root.grid_columnconfigure(i, weight=1)

# Setting the background color
root.configure(bg=bg_color)

# Running the main loop
root.mainloop()