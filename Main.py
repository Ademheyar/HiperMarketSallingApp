import tkinter as tk
import sqlite3
import os

# Create a connection to the SQLite database
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
db_path = os.path.join(data_dir, 'my_database.db')
conn = sqlite3.connect(db_path)

# Create a table to store the document records
cur = conn.cursor()
# Define the SQL statement to delete the table

cur.execute('''CREATE TABLE IF NOT EXISTS pre_doc_table 
                (id INTEGER PRIMARY KEY, 
                doc_created_date TEXT, 
                doc_expire_date TEXT, 
                doc_updated_date TEXT,
                AT_SHOP TEXT,
                user_id TEXT, 
                customer_id TEXT, 
                type TEXT, 
                ITEM TEXT,
                PRICE REAL,
                Disc REAL,
                TAX REAL,
                States TEXT
                )''')

#query = f"DROP TABLE IF EXISTS doc_table"
#cur.execute(query)

cur.execute('''CREATE TABLE IF NOT EXISTS doc_table 
                (id INTEGER PRIMARY KEY, 
                doc_barcode TEXT, 
                extension_barcode TEXT, 
                user_id TEXT, 
                customer_id TEXT, 
                type TEXT, 
                item TEXT, 
                qty REAL,  
                price REAL, 
                discount REAL, 
                tax REAL, 
                payments TEXT, 
                doc_created_date TEXT, 
                doc_expire_date TEXT, 
                doc_updated_date TEXT)''')

# Example usage:
# Add a new document record to the doc_table SQLite database table

# Connect to the database or create it if it does not exist
cur.execute('''CREATE TABLE IF NOT EXISTS product
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT,
              code TEXT,
              type TEXT,
              barcode TEXT,
              at_shop TEXT,
              quantity INTEGER,
              cost REAL,
              tax REAL,
              price REAL,
              include_tax INTEGER,
              price_change INTEGER,
              more_info TEXT,
              images TEXT,
              description TEXT,
              service TEXT,
              default_quantity INTEGER,
              active INTEGER)''')
#query = f"DROP TABLE IF EXISTS USERS"
#cur.execute(query)

cur.execute('''CREATE TABLE IF NOT EXISTS USERS
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT,
              addres TEXT,
              id_num TEXT,
              phone_num TEXT,
              email TEXT,
              type TEXT,
              password TEXT,
              acsess TEXT)''')

cur.execute('''CREATE TABLE IF NOT EXISTS tools
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT,
              code TEXT,
              type TEXT,
              short_key TEXT,
              acsess TEXT,
              enabel INTEGER,
              quick_pay INTEGER,
              customer_required INTEGER,
              printslip REAL,
              change_allowed REAL,
              markpad REAL,
              open_drower REAL)''')

conn.commit()
conn.close()

from M.Display import DisplayFrame
from Login import Loging_Frame


class MainApplication(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (screen_width, screen_height))
        self.title("Main Application")
        
        # create the container frame to hold the other frames
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # create the first frame and add it to the container
        self.frames = {}

        display_frame = DisplayFrame(self, "")
        display_frame.grid(row=0, column=0, sticky="nsew")
        self.frames["DisplayFrame"] = display_frame
        

        # create the second frame and add it to the container
        lofing_frame = Loging_Frame(self)
        lofing_frame.grid(row=0, column=0, sticky="nsew")
        self.frames["LogingFrame"] = lofing_frame
        
        
        # show the first frame by default
        self.show_frame("LogingFrame")
    
    def show_frame(self, frame_name):
        # hide all frames except the one to be shown
        for frame in self.frames.values():
            frame.grid_remove()
        self.frames[frame_name].grid()
        

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()