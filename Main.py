
import tkinter as tk
import sqlite3
import os

# Create a connection to the SQLite database
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
db_path = os.path.join(data_dir, 'my_database.db')
conn = sqlite3.connect(db_path)
# to add a table use this codez
#cur.execute("ALTER TABLE table)name ADD COLUMN column_name INT")
#cur.execute("ALTER TABLE doc_table ADD COLUMN Seller_id TEXT AFTER customer_id")
#cur.execute("ALTER TABLE setting CHANGE COLUMN user_name User_id INT")
# Create a table to store the document records

cur = conn.cursor()

#query = f"DROP TABLE IF EXISTS setting"
#cur.execute(query)
#cur.execute("ALTER TABLE setting ADD COLUMN Get_printer INT")
cur.execute('''CREATE TABLE IF NOT EXISTS setting 
                (id INTEGER PRIMARY KEY,
                User_id INT,
                barcode_count INT,
                printer TEXT,
                Items_type TEXT,
                Get_seller INT,
                Get_printer INT
                )''')

#query = f"DROP TABLE IF EXISTS upload_doc"
#cur.execute(query)

cur.execute('''CREATE TABLE IF NOT EXISTS upload_doc 
                (id INTEGER PRIMARY KEY, 
                doc_barcode TEXT, 
                extension_barcode TEXT, 
                user_id TEXT, 
                customer_id TEXT,  
                Seller_id TEXT,
                type TEXT, 
                item TEXT, 
                qty REAL,  
                price REAL, 
                discount REAL, 
                tax REAL, 
                payments TEXT,
                pid INT,
                doc_created_date TEXT, 
                doc_expire_date TEXT, 
                doc_updated_date TEXT)''')

#cur.execute('INSERT INTO upload_doc (doc_barcode, extension_barcode, user_id, customer_id, type, item, qty, price, discount, tax, payments, doc_created_date, doc_expire_date, doc_updated_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', ("23-200-", "extension_barcode", "self.user"," self.custemr", "type", "item", 0, 1, 2, 3, "payments_", "doc_created_date", "doc_expire_date", "doc_updated_date"))
#query = f"DROP TABLE IF EXISTS pre_doc_table"
#cur.execute(query)

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
                States TEXT,
                exitems_doc_barcode TEXT,
                expayment_doc_barcode TEXT)''')

#query = f"DROP TABLE IF EXISTS upload_doc"
#cur.execute(query)
# TODO add 'pid' column on doc_table
#cur.execute("ALTER TABLE doc_table ADD COLUMN Seller_id TEXT AFTER customer_id")

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
                doc_updated_date TEXT,
                pid INT,
                Seller_id TEXT)''')

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


cur.execute('''CREATE TABLE IF NOT EXISTS Shops
             (Shop_id INTEGER PRIMARY KEY AUTOINCREMENT,
              Shop_name TEXT,
              Shop_brand_name TEXT,
              Shop_type TEXT,
              Shop_oweners_id TEXT,
              Shop_link TEXT,
              Shop_email TEXT,
              Shop_phone_num TEXT,
              Shop_country TEXT,
              Shop_location TEXT,
              Shop_about TEXT,
              Shop_rate TEXT,
              Shop_likes TEXT,
              Shop_items TEXT,
              Shop_workers TEXT,
              Shop_password TEXT,
              Shop_sittings TEXT,
              Shop_profile_img TEXT,
              Shop_banner_imgs TEXT,
              Shop_payment_r TEXT,
              Shop_balance TEXT,
              Shop_payment_info TEXT,
              Shop_isenabled TEXT)''')

#query = f"DROP TABLE IF EXISTS Users"
#cur.execute(query)

cur.execute('''CREATE TABLE IF NOT EXISTS Users
             (User_id INTEGER PRIMARY KEY AUTOINCREMENT,
              User_fname TEXT,
              User_Lname TEXT,
              User_name TEXT,
              User_gender TEXT,
              User_country TEXT,
              User_phone_num TEXT,
              User_email TEXT,
              User_address TEXT,
              User_id_pp_num TEXT,
              User_home_no TEXT,
              User_type TEXT,
              User_password TEXT,
              User_about TEXT,
              User_shop TEXT,
              User_work_shop TEXT,
              User_likes TEXT,
              User_following_shop TEXT,
              User_favoraite_items TEXT,
              User_rate TEXT,
              User_access TEXT,
              User_pimg TEXT)''')

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

cur.execute('SELECT * FROM Users')
users = cur.fetchall()
'''
cur.execute('INSERT INTO Users (User_id, User_fname, User_Lname, User_name, User_gender,
              User_country,
              User_phone_num,
              User_email,
              User_address,
              User_id_pp_num,
              User_home_no,
              User_type,
              User_password,
              User_about,
              User_shop,
              User_work_shop,
              User_likes,
              User_following_shop,
              User_favoraite_items,
              User_rate,
              User_access,
              User_pimg) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
(name, addres, id_num, phone_num, email, typ, password, acsess))

'''
'''

cur.execute('UPDATE USERS SET name=?, address=?, id_num=?, phone_num=?, email=?, type=?, password=?, access=? WHERE id=?', (name, addres, id_num, phone_num, email, typ, password, acsess, item_id))
'''

from Login import Loging_Frame

conn.commit()
conn.close()
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

        self.display_frame = None

        # create the second frame and add it to the container
        lofing_frame = Loging_Frame(self)
        lofing_frame.grid(row=0, column=0, sticky="nsew")
        self.frames["LogingFrame"] = lofing_frame
        
        
        self.bind("<Escape>", self.change_focus)
        self.bind("<KeyPress-d>", self.crtl_d_focus)
        self.bind("<KeyPress-D>", self.crtl_d_focus)
        # show the first frame by default
        
        self.show_frame("LogingFrame")
        
    def crtl_d_focus(self, event):
        print("crtl+D pressed " + str(event))
        if "Control" in str(event) or event.state == 14:
            self.frames["DisplayFrame"].open_drower()
            print("crtl+D pressed " + str(event.state))
        
    def change_focus(self, event):
        self.frames["DisplayFrame"].search_entry.focus_set()
        
    def show_frame(self, frame_name):
        # hide all frames except the one to be shown
        for frame in self.frames.values():
            frame.grid_remove()
        self.frames[frame_name].grid()
        #if frame_name == "DisplayFrame":
        #    self.frames[frame_name].search_entry.focus_set()
        

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
