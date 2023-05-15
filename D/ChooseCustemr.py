import tkinter as tk
import sqlite3
import os

def open_search_dialog():
    dialog = tk.Toplevel()

    username_label = tk.Label(dialog, text="Username")
    username_label.pack()

    username_entry = tk.Entry(dialog)
    username_entry.pack()

    user_id_label = tk.Label(dialog, text="User ID:")
    user_id_label.pack()
    
    username_label = tk.Label(dialog, text="Username:")
    username_label.pack()
    
    first_name_label = tk.Label(dialog, text="First Name:")
    first_name_label.pack()
    
    last_name_label = tk.Label(dialog, text="Last Name:")
    last_name_label.pack()
    
    email_label = tk.Label(dialog, text="Email:")
    email_label.pack()

    # Create a listbox to display the search results
    listbox = tk.Listbox(dialog)
    listbox.pack()
    
    search_button = tk.Button(dialog, text="Search", command=lambda: search_user(username_entry.get()))
    search_button.pack()

    def show_user_details(username):
        connection = sqlite3.connect("mydb.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        # Clear the details panel before showing new details
        clear_details_panel()

        if row:
            user_id = row[0]
            first_name = row[2]
            last_name = row[3]
            email = row[4]

            # Display the details of the selected item in the main window
            user_id_label.config(text="User ID: " + str(user_id))
            username_label.config(text="Username: " + username)
            first_name_label.config(text="First Name: " + first_name)
            last_name_label.config(text="Last Name: " + last_name)
            email_label.config(text="Email: " + email)



    def search_user(search_value):
        connection = sqlite3.connect("mydb.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? OR first_name = ? OR last_name = ? OR email = ?", 
                       (search_value, search_value, search_value, search_value))
        results = cursor.fetchall()
        cursor.close()
        connection.close()

        if not results:
            tk.messagebox.showerror("Error", "No user found with that search value")
        else:
            listbox.delete(0, tk.END)  # Clear the listbox before adding new results
            for row in results:
                user_id = row[0]
                username = row[1]
                listbox.insert(tk.END, username)

                
    # Function to handle the selection of an item from the listbox
    def on_select(event):
        selected_index = listbox.curselection()
        if selected_index:
            # Get the selected item from the listbox
            selected_item = listbox.get(selected_index)
            # Extract the user ID from the selected item
            # Show the details of the selected item in the main window
            show_user_details(selected_item)

    # Bind the on_select function to the listbox selection event
    listbox.bind('<<ListboxSelect>>', on_select)

    dialog.mainloop()

def clear_details_panel():
    # Clear all widgets from the details panel
    for widget in details_panel.winfo_children():
        widget.destroy()

root = tk.Tk()

search_button = tk.Button(root, text="Search", command=open_search_dialog)
search_button.pack()

details_panel = tk.Frame(root)
details_panel.pack()

# Check if the database file exists
if not os.path.isfile("mydb.db"):
    # Create the database file
    connection = sqlite3.connect("mydb.db")
    cursor = connection.cursor()

    # Create the users table
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            email TEXT
        )
    """)

    # Add sample user information for testing
    sample_user = ("JohnDoe", "John", "Doe", "johndoe@example.com")
    cursor.execute("INSERT INTO users (username, first_name, last_name, email) VALUES (?, ?, ?, ?)", sample_user)

    # Commit the changes and close the cursor and connection
    connection.commit()
    cursor.close()
    connection.close()

# Start the main loop
root.mainloop()
