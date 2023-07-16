import tkinter as tk
from tkinter import ttk
import sqlite3, os

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

class UserManagementApp(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.user_details = {}

        self.username_var = tk.StringVar()
        self.username_var.trace('w', self.entry_changed)

        username_label = tk.Label(self, text="Username", font=("Arial", 14))
        username_label.grid(row=0, column=0, padx=10, pady=10)

        self.username_entry = tk.Entry(self, textvariable=self.username_var, font=("Arial", 14))
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        self.user_listbox = tk.Listbox(self, font=("Arial", 14), width=30)
        self.user_listbox.grid(row=1, column=0, rowspan=5, padx=10, pady=10)
        self.user_listbox.bind("<<ListboxSelect>>", self.on_user_select)

        search_button = tk.Button(self, text="Search", command=self.search, font=("Arial", 14))
        search_button.grid(row=2, column=1, sticky="w", padx=10, pady=10)

        self.create_user_button = tk.Button(self, text="Create User", command=self.create_user_dialog, font=("Arial", 14))
        self.create_user_button.grid(row=3, column=1, sticky="w", padx=10, pady=10)

        self.details_panel = tk.Frame(self)
        self.details_panel.grid(row=1, column=2, rowspan=5, padx=10, pady=10, sticky="n")

        self.fill_user_listbox()
        self.minsize(800, 600)  # Set the minimum window size

        # TODO: show this user info
        # TODO: user can change name, or password in this form
        # TODO: user can add sub user depending on its usertype
        
        # show the Payment Form window
        self.transient(self.master)
        self.grab_set()
        self.master.wait_window(self)

    def show_user_details(self, username):
        cursor.execute("SELECT * FROM USERS WHERE name = ?", (username,))
        row = cursor.fetchone()

        self.clear_details_panel()

        if row:
            user_id = row[0]
            name  = row[1]
            addres  = row[2]
            id_num  = row[3]
            phone_num  = row[4]
            email  = row[5]
            type  = row[6]
            password  = row[7]
            acsess= row[8]

            user_id_label = tk.Label(self.details_panel, text="User ID: " + str(user_id), font=("Arial", 14))
            user_id_label.grid(row=0, column=0, sticky="w")

            username_label = tk.Label(self.details_panel, text="Username: " + str(name), font=("Arial", 14))
            username_label.grid(row=1, column=0, sticky="w")

            first_name_label = tk.Label(self.details_panel, text="First Name: " + str(user_id), font=("Arial", 14))
            first_name_label.grid(row=2, column=0, sticky="w")

            last_name_label = tk.Label(self.details_panel, text="phone number: " + str(phone_num), font=("Arial", 14))
            last_name_label.grid(row=3, column=0, sticky="w")

            email_label = tk.Label(self.details_panel, text="Email: " + str(email), font=("Arial", 14))
            email_label.grid(row=4, column=0, sticky="w")

            self.user_details = {
                "id": user_id,
                "name": name,
                "addres": addres,
                "id_num": id_num,
                "phone_num": phone_num,
                "Email": email,
                "type": type,
                "password": password,
                "acsess": acsess
            }

    def fill_user_listbox(self):
        self.user_listbox.delete(0, tk.END)
        cursor.execute("SELECT name FROM users")
        rows = cursor.fetchall()
        for row in rows:
            self.user_listbox.insert(tk.END, row[0])

    def clear_details_panel(self):
        for widget in self.details_panel.winfo_children():
            widget.destroy()

    def on_user_select(self, event):
        selected_username = self.user_listbox.get(self.user_listbox.curselection())
        if self.user_details:
            if selected_username == self.user_details["name"]:
                self.destroy()
        else:
            self.show_user_details(selected_username)

    def entry_changed(self, *args):
        username = self.username_var.get()
        cursor.execute("SELECT name FROM users WHERE name LIKE ?", (f'%{username}%',))
        rows = cursor.fetchall()
        self.user_listbox.delete(0, tk.END)
        for row in rows:
            self.user_listbox.insert(tk.END, row[0])

    def search(self):
        username = self.username_var.get()
        cursor.execute("SELECT name FROM users WHERE name LIKE ?", (f'%{username}%',))
        rows = cursor.fetchall()
        self.user_listbox.delete(0, tk.END)
        for row in rows:
            self.user_listbox.insert(tk.END, row[0])

    def create_user_dialog(self):
        CreateUserDialog(self)

    def close_connection(self):
        cursor.close()
        conn.close()

class CreateUserDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.name_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.id_num_var = tk.StringVar()
        self.phone_num_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.type_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.access_var = tk.StringVar()

        name_label = tk.Label(self, text="Name", font=("Arial", 14))
        name_label.grid(row=0, column=0, padx=10, pady=10)

        name_entry = tk.Entry(self, textvariable=self.name_var, font=("Arial", 14))
        name_entry.grid(row=0, column=1, padx=10, pady=10)

        address_label = tk.Label(self, text="Address", font=("Arial", 14))
        address_label.grid(row=1, column=0, padx=10, pady=10)

        address_entry = tk.Entry(self, textvariable=self.address_var, font=("Arial", 14))
        address_entry.grid(row=1, column=1, padx=10, pady=10)

        id_num_label = tk.Label(self, text="ID Number", font=("Arial", 14))
        id_num_label.grid(row=2, column=0, padx=10, pady=10)

        id_num_entry = tk.Entry(self, textvariable=self.id_num_var, font=("Arial", 14))
        id_num_entry.grid(row=2, column=1, padx=10, pady=10)

        phone_num_label = tk.Label(self, text="Phone Number", font=("Arial", 14))
        phone_num_label.grid(row=3, column=0, padx=10, pady=10)

        phone_num_entry = tk.Entry(self, textvariable=self.phone_num_var, font=("Arial", 14))
        phone_num_entry.grid(row=3, column=1, padx=10, pady=10)

        email_label = tk.Label(self, text="Email", font=("Arial", 14))
        email_label.grid(row=4, column=0, padx=10, pady=10)

        email_entry = tk.Entry(self, textvariable=self.email_var, font=("Arial", 14))
        email_entry.grid(row=4, column=1, padx=10, pady=10)

        type_label = tk.Label(self, text="Type", font=("Arial", 14))
        type_label.grid(row=5, column=0, padx=10, pady=10)

        type_entry = tk.Entry(self, textvariable=self.type_var, font=("Arial", 14))
        type_entry.grid(row=5, column=1, padx=10, pady=10)

        password_label = tk.Label(self, text="Password", font=("Arial", 14))
        password_label.grid(row=6, column=0, padx=10, pady=10)

        password_entry = tk.Entry(self, textvariable=self.password_var, font=("Arial", 14))
        password_entry.grid(row=6, column=1, padx=10, pady=10)

        access_label = tk.Label(self, text="Access", font=("Arial", 14))
        access_label.grid(row=7, column=0, padx=10, pady=10)

        access_entry = tk.Entry(self, textvariable=self.access_var, font=("Arial", 14))
        access_entry.grid(row=7, column=1, padx=10, pady=10)

        create_button = tk.Button(self, text="Create", command=self.create_user, font=("Arial", 14))
        create_button.grid(row=8, column=0, padx=10, pady=10)

        cancel_button = tk.Button(self, text="Cancel", command=self.destroy, font=("Arial", 14))
        cancel_button.grid(row=8, column=1, padx=10, pady=10)

        self.transient(self.master)
        self.grab_set()
        self.master.wait_window(self)

    def create_user(self):
        name = self.name_var.get()
        address = self.address_var.get()
        id_num = self.id_num_var.get()
        phone_num = self.phone_num_var.get()
        email = self.email_var.get()
        user_type = self.type_var.get()
        password = self.password_var.get()
        access = self.access_var.get()

        cursor.execute("INSERT INTO users (name, address, id_num, phone_num, email, type, password, access) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (name, address, id_num, phone_num, email, user_type, password, access))
        conn.commit()

        self.parent.fill_user_listbox()
        self.destroy()



'''if __name__ == "__main__":
    root = tk.Tk()
    app = UserManagementApp(root)

    if app.user_details:
        print(app.user_details)
    root.mainloop()
    app.close_connection()'''
