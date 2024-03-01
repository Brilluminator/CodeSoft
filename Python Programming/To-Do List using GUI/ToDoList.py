import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3 as sql


# main function  
if __name__ == "__main__":
    interface = tk.Tk()
    interface.title("Sudeepa's To-Do List")
    interface.geometry("400x450")  # Set size and position
    interface.resizable(0, 0)  
    interface.configure(bg="#FFC0CB")  # Set background color to light pink

# Define tasks list
tasks = []

# Define SQLite database connection and cursor
conn = sql.connect('tasks.db')
the_cursor = conn.cursor()

# Create tasks table if not exists
the_cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    title TEXT)''')
conn.commit()

# Add a task to the list
def add_task():
    task_string = task_bar.get()
    if len(task_string) == 0:
        messagebox.showinfo('Error', 'Entry is empty')
    else:
        tasks.append(task_string)
        the_cursor.execute('INSERT INTO tasks (title) VALUES (?)', (task_string,))
        conn.commit()
        list_update()
        task_bar.delete(0, 'end')

# Update the task list
def list_update():
    clear_list()
    for task in tasks:
        task_listbox.insert('end', task)

# Delete a selected task
def delete_task():
    try:
        the_value = task_listbox.get(task_listbox.curselection())
        if the_value in tasks:
            tasks.remove(the_value)
            the_cursor.execute('DELETE FROM tasks WHERE title = ?', (the_value,))
            conn.commit()
            list_update()
    except:
        messagebox.showinfo('Error', 'No Task Selected. Cannot Delete')

# Delete all tasks
def delete_all_tasks():
    if messagebox.askyesno('Delete All', 'Are you sure?'):
        tasks.clear()
        the_cursor.execute('DELETE FROM tasks')
        conn.commit()
        list_update()

# Clear the task list
def clear_list():
    task_listbox.delete(0, 'end')

# Close the application
def close():
    interface.destroy()

# Retrieve data from the database
def retrieve_database():
    clear_list()
    for row in the_cursor.execute('SELECT title FROM tasks'):
        tasks.append(row[0])
    list_update()

# Entry bar
task_bar = ttk.Entry(interface, width=50)  # Adjusted width
task_bar.grid(row=0, column=0, padx=5, pady=5)

# Add Task button
add_button = ttk.Button(interface, text="Add Task", command=add_task, width=10)  # Adjusted width
add_button.grid(row=0, column=1, padx=5, pady=5)

# Frame for task list
list_frame = tk.Frame(interface, bg="#FFC0CB", width=480, height=300)  # Adjusted width and height
list_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

# Task Listbox
task_listbox = tk.Listbox(list_frame, width=58, height=15)  # Adjusted width and height
task_listbox.pack(padx=5, pady=5)

# Buttons frame
button_frame = tk.Frame(interface, bg="#FFC0CB", width=480)  # Adjusted width
button_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# Delete Task button
delete_button = ttk.Button(button_frame, text="Delete Task", command=delete_task, width=20)  # Adjusted width
delete_button.grid(row=0, column=0, padx=5, pady=5)

# Delete All Tasks button
delete_all_button = ttk.Button(button_frame, text="Delete All", command=delete_all_tasks, width=20)  # Adjusted width
delete_all_button.grid(row=0, column=1, padx=5, pady=5)

# Retrieve from Database button
retrieve_button = ttk.Button(button_frame, text="Retrieve from Database", command=retrieve_database, width=41)  # Adjusted width
retrieve_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

# Close button
close_button = ttk.Button(interface, text="Close", command=close, width=41)  # Adjusted width
close_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Run the main loop
interface.mainloop()

# Close the database connection
conn.close()
