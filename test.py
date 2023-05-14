import tkinter as tk
import tkinter.ttk as ttk
import sqlite3
import os


class App:
    def __init__(self, master):
        self.master = master
        master.title("Database Copier")

        self.db_paths = []

        # Create buttons to add source and destination database paths
        self.source_button = tk.Button(master, text="Add Source DB", command=self.add_source)
        self.destination_button = tk.Button(master, text="Add Destination DB", command=self.add_destination)

        # Create a Treeview to show source database information
        self.source_treeview = ttk.Treeview(master, columns=("table", "column"))
        self.source_treeview.heading("#0", text="Database")
        self.source_treeview.heading("table", text="Table")
        self.source_treeview.heading("column", text="Column")

        # Create a Treeview to show destination database information
        self.destination_treeview = ttk.Treeview(master, columns=("table", "column"))
        self.destination_treeview.heading("#0", text="Database")
        self.destination_treeview.heading("table", text="Table")
        self.destination_treeview.heading("column", text="Column")

        # Create a Treeview to show copying information
        self.copy_treeview = ttk.Treeview(master, columns=("source_db", "source_table", "source_column", "destination_db", "destination_table", "destination_column"))
        
        self.copy_treeview.heading("#0", text="Copy")
        self.copy_treeview.heading("source_db", text="Source DB")
        self.copy_treeview.heading("source_table", text="Source Table")
        self.copy_treeview.heading("source_column", text="Source Column")
        self.copy_treeview.heading("destination_db", text="Destination DB")
        self.copy_treeview.heading("destination_table", text="Destination Table")
        self.copy_treeview.heading("destination_column", text="Destination Column")

        # Create labels and entry boxes for copying information
        self.source_db_label = tk.Label(master, text="Source Database:")
        self.source_db_entry = tk.Entry(master)
        self.source_db_entry.insert(0, "source.db")
        self.source_table_label = tk.Label(master, text="Source Table:")
        self.source_table_entry = tk.Entry(master)
        self.source_table_entry.insert(0, "source_table")
        self.source_column_label = tk.Label(master, text="Source Column:")
        self.source_column_entry = tk.Entry(master)
        self.source_column_entry.insert(0, "source_column")
        self.destination_db_label = tk.Label(master, text="Destination Database:")
        self.destination_db_entry = tk.Entry(master)
        self.destination_db_entry.insert(0, "destination.db")
        self.destination_table_label = tk.Label(master, text="Destination Table:")
        self.destination_table_entry = tk.Entry(master)
        self.destination_table_entry.insert(0, "destination_table")
        self.destination_column_label = tk.Label(master, text="Destination Column:")
        self.destination_column_entry = tk.Entry(master)
        self.destination_column_entry.insert(0, "destination_column")

        # Create a button to start copying
        self.copy_button = tk.Button(master, text="Copy", command=self.copy_)

                # Grid layout for widgets
        self.source_db_label.grid(row=3, column=0, sticky="W")
        self.source_db_entry.grid(row=3, column=1, padx=5, pady=5)
        self.source_button.grid(row=3, column=2, padx=5, pady=5)
        self.source_table_label.grid(row=4, column=0, sticky="W")
        self.source_table_entry.grid(row=4, column=1, padx=5, pady=5)
        self.source_column_label.grid(row=5, column=0, sticky="W")
        self.source_column_entry.grid(row=5, column=1, padx=5, pady=5)
        self.destination_db_label.grid(row=6, column=0, sticky="W")
        self.destination_db_entry.grid(row=6, column=1, padx=5, pady=5)
        self.destination_button.grid(row=6, column=2, padx=5, pady=5)
        self.destination_table_label.grid(row=7, column=0, sticky="W")
        self.destination_table_entry.grid(row=7, column=1, padx=5, pady=5)
        self.destination_column_label.grid(row=8, column=0, sticky="W")
        self.destination_column_entry.grid(row=8, column=1, padx=5, pady=5)
        self.copy_button.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

        self.copy_treeview.grid(row=11, column=0, columnspan=4, padx=5, pady=5)
        self.source_treeview.grid(row=14, column=0, columnspan=2, padx=5, pady=5)
        self.destination_treeview.grid(row=14, column=2, columnspan=2, padx=5, pady=5)

    def add_source(self):
        db_path = self.source_db_entry.get()
        if db_path:
            self.db_paths.append(db_path)
            self.update_source_treeview()

    def add_destination(self):
        db_path = self.destination_db_entry.get()
        if db_path:
            self.db_paths.append(db_path)
            self.update_destination_treeview()

    def update_source_treeview(self):
        self.source_treeview.delete(*self.source_treeview.get_children())
        for db_path in self.db_paths:
            # Connect to the database and fetch source table and column information
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            for table in tables:
                cursor.execute(f"PRAGMA table_info({table[0]})")
                columns = cursor.fetchall()
                for column in columns:
                    self.source_treeview.insert("", "end", text=db_path, values=(table[0], column[1]))
            conn.close()

    def update_destination_treeview(self):
        self.destination_treeview.delete(*self.destination_treeview.get_children())
        for db_path in self.db_paths:
            # Connect to the database and fetch destination table and column information
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            for table in tables:
                cursor.execute(f"PRAGMA table_info({table[0]})")
                columns = cursor.fetchall()
                for column in columns:
                    self.destination_treeview.insert("", "end", text=db_path, values=(table[0], column[1]))
            conn.close()
    
    def create_database(self, db_path, table_name, column_name, column_values):
        if not os.path.isfile(db_path):
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({column_name} TEXT)")
            for value in column_values:
                cursor.execute(f"INSERT INTO {table_name} ({column_name}) VALUES ('{value}')")
            conn.commit()
            conn.close()
            print(f"{db_path} created.")
    
    def copy_(self):
        source_db = self.source_db_entry.get()
        destination_db = self.destination_db_entry.get()
        source_table = self.source_table_entry.get()
        source_column = self.source_column_entry.get()
        destination_table = self.destination_table_entry.get()
        destination_column = self.destination_column_entry.get()

        if not all([source_db, destination_db, source_table, source_column, destination_table, destination_column]):
            print("Error: Please fill in all the fields.")
            return

        # Create the source database if it doesn't exist
        self.create_database(source_db, source_table, source_column, ["Value 1", "Value 2", "Value 3"])

        # Create the destination database if it doesn't exist
        self.create_database(destination_db, destination_table, destination_column, ["Value A", "Value B"])

        # Copy the column
        self.copy_column(source_db, destination_db, source_table, source_column, destination_table, destination_column)



    def copy_column(self, source_db, destination_db, source_table, source_column, destination_table, destination_column):
        # Connect to the source database
        source_conn = sqlite3.connect(source_db)
        source_cursor = source_conn.cursor()

        # Connect to the destination database
        destination_conn = sqlite3.connect(destination_db)
        destination_cursor = destination_conn.cursor()

        try:
            # Check if the source table exists
            source_cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{source_table}'")
            if not source_cursor.fetchone():
                print(f"Error: Source table '{source_table}' does not exist.")
                return

            # Check if the source column exists
            source_cursor.execute(f"PRAGMA table_info({source_table})")
            columns = [column[1] for column in source_cursor.fetchall()]
            if source_column not in columns:
                print(f"Error: Source column '{source_column}' does not exist in '{source_table}'.")
                return

            # Fetch data from the source table
            source_cursor.execute(f"SELECT {source_column} FROM {source_table}")
            data = source_cursor.fetchall()

            # Check if the destination table exists
            destination_cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{destination_table}'")
            if not destination_cursor.fetchone():
                print(f"Error: Destination table '{destination_table}' does not exist.")
                return

            # Check if the destination column exists
            destination_cursor.execute(f"PRAGMA table_info({destination_table})")
            columns = [column[1] for column in destination_cursor.fetchall()]
            if destination_column not in columns:
                print(f"Error: Destination column '{destination_column}' does not exist in '{destination_table}'.")
                return

            # Check if the value already exists in the destination column
            destination_cursor.execute(f"SELECT {destination_column} FROM {destination_table}")
            existing_values = destination_cursor.fetchall()
            existing_values = [value[0] for value in existing_values]
            data = [value for value in data if value[0] not in existing_values]

            # Print the before results
            print("Before copying:")
            print(f"Source Database - Source Table ({source_table}) - Source Column ({source_column}):")
            print(data)
            print(f"Destination Database - Destination Table ({destination_table}) - Destination Column ({destination_column}):")
            destination_cursor.execute(f"SELECT {destination_column} FROM {destination_table}")
            print(destination_cursor.fetchall())
            print()

            # Start a transaction
            destination_conn.execute("BEGIN TRANSACTION")

            # Insert data into the destination table
            destination_cursor.executemany(f"INSERT INTO {destination_table} ({destination_column}) VALUES (?)", data)

            # Commit the transaction
            destination_conn.execute("COMMIT")
            print("Column copied successfully!")
            print()

            # Print the after results
            print("After copying:")
            print(f"Source Database - Source Table ({source_table}) - Source Column ({source_column}):")
            print(data)
            print(f"Destination Database - Destination Table ({destination_table}) - Destination Column ({destination_column}):")
            destination_cursor.execute(f"SELECT {destination_column} FROM {destination_table}")
            print(destination_cursor.fetchall())

        except Exception as e:
            # Roll back the transaction on error
            destination_conn.execute("ROLLBACK")
            print(f"Error: {e}")

        finally:
            # Close the connections
            source_conn.close()
            destination_conn.close()



root = tk.Tk()
app = App(root)
root.mainloop()



'''
def create_databases():
    
import sqlite3

# Create the databases and tables
create_databases()

# Example usage
copy_column('source.db', 'destination.db', 'source_table', 'source_column', 'destination_table', 'destination_column')
'''