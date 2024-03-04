import tkinter as tk
from tkinter import ttk
import sqlite3

class ContactBookApp:
    def __init__(self, root):
        self.root = root
        self.connection = sqlite3.connect("final.db")
        self.cursor = self.connection.cursor()

        self.root.title("Contact Book")
        self.root.geometry("500x600")  # Increased width size

        # Set background color to dual-tone purple and black mix
        self.root.configure(bg="#A020F0")

        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Set button styles
        self.style.configure("Rounded.TButton",
                             background="#4B0082",  # Dual-tone purple and black mix
                             foreground="#FFFFFF",  # Text color
                             borderwidth=0,  # No border
                             font=("Helvetica", 12),  # Font
                             padding=10,  # Padding
                             relief="flat")  # Flat relief for rounded appearance

        self.style.map("Rounded.TButton",
                       background=[("active", "#483D8B")],  # Dark slate blue on button click
                       foreground=[("active", "#FFFFFF")])  # Text color on button click

        self.main_frame = ttk.Frame(root, padding=(20, 20, 20, 0), style="Rounded.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.pack(fill=tk.BOTH, padx=10, pady=10)

        self.name_label = ttk.Label(self.input_frame, text="Name:", style="Rounded.TLabel")
        self.name_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.name_entry = ttk.Entry(self.input_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.phone_label = ttk.Label(self.input_frame, text="Phone Number:", style="Rounded.TLabel")
        self.phone_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.phone_entry = ttk.Entry(self.input_frame, width=30)
        self.phone_entry.grid(row=1, column=1, padx=10, pady=10)

        # Add rounded buttons
        self.add_button = ttk.Button(self.input_frame, text="Add Contact", style="Rounded.TButton", command=self.add_contact)
        self.add_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.delete_button = ttk.Button(self.input_frame, text="Delete Contact", style="Rounded.TButton", command=self.delete_contact)
        self.delete_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.search_frame = ttk.Frame(self.main_frame)
        self.search_frame.pack(fill=tk.BOTH, padx=10, pady=10)

        self.search_label = ttk.Label(self.search_frame, text="Search Name:", style="Rounded.TLabel")
        self.search_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.search_entry = ttk.Entry(self.search_frame, width=30)
        self.search_entry.grid(row=0, column=1, padx=10, pady=10)

        self.search_button = ttk.Button(self.search_frame, text="Search Contact", style="Rounded.TButton", command=self.search_contact)
        self.search_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Added Treeview widget to display contacts
        self.tree_frame = ttk.Frame(self.main_frame)
        self.tree_frame.pack(fill=tk.BOTH, padx=10, pady=10)

        self.tree = ttk.Treeview(self.tree_frame, columns=("Name", "Phone Number"), show="headings", height=10)
        self.tree.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.tree.heading("Name", text="Name")
        self.tree.heading("Phone Number", text="Phone Number")

        self.tree_scroll = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree_scroll.grid(row=0, column=2, sticky="ns")
        self.tree.configure(yscrollcommand=self.tree_scroll.set)

    def add_contact(self):
        name = self.name_entry.get().strip()
        phone_number = self.phone_entry.get().strip()
        
        if name and phone_number:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS Users(name TEXT, number TEXT)")
            self.cursor.execute("INSERT INTO Users(name, number) VALUES (?, ?)", (name, phone_number))
            self.connection.commit()

            self.name_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
            print("Contact added successfully!")

        # Refresh the tree view to display the updated contacts
            self.refresh_tree_view()
        else:
            print("Please enter both name and phone number.")

    def refresh_tree_view(self):
    # Clear the tree view
        self.tree.delete(*self.tree.get_children())

    # Fetch all contacts from the database
        self.cursor.execute("SELECT * FROM Users")
        result = self.cursor.fetchall()

    # Populate the tree view with the fetched contacts
        if result:
            for row in result:
                self.tree.insert("", "end", values=row)

    def search_contact(self):
        name = self.search_entry.get().strip()

        self.cursor.execute("SELECT * FROM Users WHERE name LIKE ?", ('%' + name + '%',))
        result = self.cursor.fetchall()

        self.tree.delete(*self.tree.get_children())  # Clear previous search results

        if result:
            for row in result:
                self.tree.insert("", "end", values=row)
        else:
            print("Sorry, no matching contact.")

    def delete_contact(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_id = selected_item[0]
            name = self.tree.item(item_id, "values")[0]
            self.cursor.execute("DELETE FROM Users WHERE name=?", (name,))
            self.connection.commit()
            self.tree.delete(item_id)
            print("Contact deleted successfully!")
        else:
            print("Please select a contact to delete.")

    def update_contact(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_id = selected_item[0]
            name = self.tree.item(item_id, "values")[0]
            new_phone_number = self.phone_entry.get().strip()

            if new_phone_number:
                self.cursor.execute("UPDATE Users SET number=? WHERE name=?", (new_phone_number, name))
                self.connection.commit()

                self.phone_entry.delete(0, tk.END)
                print("Contact updated successfully!")
            else:
                print("Please enter a new phone number.")
        else:
            print("Please select a contact to update.")

def main():
    root = tk.Tk()
    app = ContactBookApp(root)

    root.mainloop()

if __name__ == "__main__":
    main()

