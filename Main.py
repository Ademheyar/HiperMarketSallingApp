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


cur.execute('''CREATE TABLE IF NOT EXISTS setting 
                (id INTEGER PRIMARY KEY,
                User_id INT,
                barcode_count INT,
                printer TEXT,
                Items_type TEXT,
                Get_seller INT,
                Get_printer INT,
                Slip_orders TEXT,
                Slip_width INT
                )''')


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

#query = f"DROP TABLE IF EXISTS setting"
#cur.execute(query)
#cur.execute("ALTER TABLE setting ADD COLUMN Get_printer INT")
cur.execute('''CREATE TABLE IF NOT EXISTS COUNT_SELL 
                (id INTEGER PRIMARY KEY,
                SELLER_ID INT,
                SELLER_NAME TEXT,
                DOC_BARCODE TEXT,
                ITEM_COUNTED INT,
                DATE TEXT
                )''')

#query = f"DROP TABLE IF EXISTS upload_doc"
#cur.execute(query)

cur.execute('''CREATE TABLE IF NOT EXISTS upload_doc 
                (id INTEGER PRIMARY KEY, 
                doc_barcode TEXT, 
                extension_barcode TEXT,
                At_Shop_Id TEXT, 
                user_id TEXT, 
                Seller_id TEXT,
                customer_id TEXT, 
                pid INT,
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

#query = f"DROP TABLE IF EXISTS Actions"
#cur.execute(query)

cur.execute('''CREATE TABLE IF NOT EXISTS Actions 
                (Actions_Id INTEGER PRIMARY KEY, 
                Product_Id TEXT, 
                Product_Name TEXT, 
                Product_Code TEXT, 
                Product_Shop_ TEXT,  
                Product_Color_is TEXT,
                Product_Size_is TEXT, 
                Product_Qty_is TEXT, 
                Product_Price_is REAL,  
                Product_Total_price_is REAL, 
                Product_Add_New REAL, 
                Product_Make_price REAL, 
                Product_Make_Total_price TEXT,
                Product_Make_Discount INT,
                Product_Make_Total_Disc TEXT,
                Enabel INT,
                Remove_When_Expires TEXT, 
                From_Date TEXT, 
                TO_Date TEXT)''')

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

#query = f"DROP TABLE IF EXISTS doc_table"
#cur.execute(query)
# TODO add 'pid' column on doc_table
#cur.execute("ALTER TABLE doc_table ADD COLUMN Profite REAL AFTER price")

cur.execute('''CREATE TABLE IF NOT EXISTS doc_table 
                (id INTEGER PRIMARY KEY, 
                doc_barcode TEXT, 
                extension_barcode TEXT,
                At_Shop_Id TEXT, 
                user_id TEXT, 
                Seller_id TEXT,
                customer_id TEXT, 
                pid INT,
                type TEXT, 
                item TEXT, 
                qty REAL,  
                price REAL, 
                Profite REAL,
                discount REAL, 
                tax REAL, 
                payments TEXT,
                doc_created_date TEXT, 
                doc_expire_date TEXT, 
                doc_updated_date TEXT)''')

#sq = "DELETE FROM doc_table WHERE id=(SELECT MAX(id) FROM doc_table)"
#cur.execute(sq)
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
#query = f"DROP TABLE IF EXISTS Shops"
#cur.execute(query)

#`Shop_name`, `Shop_brand_name`, `Shop_oweners_id`, `shop_type`, `Shop_location`, `shop_email`, 
# `Shop_contact`, `Shop_password`, `Shop_Page`, `Shop_rate`, `Shop_items`, `Shop_followers`, 
# `Shop_workers`,  `Shop_Payment_Tools`, `Shop_about`, `Shop_Security_Levels`,
# `Company_Started_Date`, `Shop_likes`, `Shop_rules`, `Shop_link`, `Shop_Settings`,
# `Shop_profile_img`, `Shop_banner_imgs`, `Shop_payment_info`, `Shop_isenabled`,
#  `Shop_Slip_Settings`, `Shop_Expenses`, `Shop_Actions`
#cur.execute('ALTER TABLE Shops RENAME COLUMN Shop_id TO Shop_Id')
#cur.execute('ALTER TABLE Shops ADD COLUMN Id INTEGER')
cur.execute('''CREATE TABLE IF NOT EXISTS Shops
             (Id INTEGER PRIMARY KEY AUTOINCREMENT,
              Shop_Id INTEGER,
              Shop_name TEXT,
              Shop_brand_name TEXT,
              Shop_oweners_id TEXT,
              Shop_type TEXT,
              Shop_location TEXT,
              Shop_email TEXT,
              Shop_contact TEXT,
              Shop_password TEXT,
              Shop_Page TEXT,
              Shop_rate TEXT,
              Shop_items TEXT,
              Shop_followers TEXT,
              Shop_workers TEXT,
              Shop_Payment_Tools TEXT,
              Shop_about TEXT,
              Shop_Security_Levels TEXT,
              Company_Started_Date TEXT,
              Shop_likes TEXT,
              Shop_rules TEXT,
              Shop_link TEXT,
              Shop_Settings TEXT,
              Shop_profile_img TEXT,
              Shop_banner_imgs TEXT,
              Shop_payment_info TEXT,
              Shop_isenabled TEXT,
              Shop_Slip_Settings TEXT,
              Shop_Expenses TEXT,
              Shop_Actions TEXT,

              
              Shop_Items_type TEXT,
              Shop_country TEXT,
              Shop_payment_r TEXT,
              Shop_Access_levels TEXT)''')
              

#cur.execute("ALTER TABLE Id ADD COLUMN Shop_Settings TEXT AFTER Shop_link")

#cur.execute("""
#   INSERT INTO Shops (Shop_name, Shop_brand_name, Shop_oweners_id)
#    VALUES ('FLAG_SQUARE', 'FLAG_SQUARE', '1');
#    """)

#query = f"DROP TABLE IF EXISTS Users"
#cur.execute(query)

#cur.execute("ALTER TABLE Users ADD COLUMN Id INTEGER BEFORE User_id")

cur.execute('''CREATE TABLE IF NOT EXISTS Users
             (Id INTEGER PRIMARY KEY AUTOINCREMENT,
              User_id INTEGER,
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


conn.commit()
conn.close()

#from Login import Loging_Frame
from M.Display import DisplayFrame

from tkinter import ttk

class MainApplication(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.state('zoomed')  # Full screen on Windows
        self.overrideredirect(True)  # Remove title bar and borders
        self.title("Hiper Market")
        
        # Android-style dark blue color scheme
        self.bg_dark = "#0d47a1"      # Deep blue
        self.bg_light = "#1565c0"     # Darker blue
        self.accent_blue = "#1976d2"  # Medium blue
        self.text_light = "#ffffff"   # White text
        
        # Modern battery/energy-inspired color scheme
        bg_dark = "#0d47a1"      # Dark navy 1a1a2e
        bg_medium = "#16213e"    # Medium navy
        accent_green = "#0f3460" # Deep blue-green
        accent_yellow = "#e94560" # Energy red
        text_light = "#eaeaea"   # Light gray
        text_secondary = "#b0b0b0" # Secondary text
        
        # Configure style for battery-inspired theme
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=bg_dark, borderwidth=1, relief='flat')
        style.configure('TNotebook.Tab', padding=[10, 5], background=bg_medium, foreground=text_light, borderwidth=0)
        style.map('TNotebook.Tab', background=[('selected', accent_green)], foreground=[('selected', 'white')])
        style.configure('TFrame', background=bg_dark)
        style.configure('COSTUM.LISTSELECTED', background='#1a1a2e')
        style.configure('COSTUM.LISTS', background=bg_dark)
        style.configure('TButton', forground=self.bg_light)
        style.configure('TButton', background=self.text_light)
        style.configure('TLabel', background=bg_dark, foreground=text_light)
        
        # Configure main window styling
        self.configure(bg=self.bg_dark)
        
        # create the container frame to hold the other frames
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # create the first frame and add it to the container
        self.frames = {}
        self.display_frame = None

        # create the display frame with Android styling
        self.display_frame = DisplayFrame(self, None, None, None, None)
        # self.display_frame.configure(bg=self.bg_dark)
        # self.display_frame.grid(row=0, column=0, sticky="nsew")
        self.frames["DisplayFrame"] = self.display_frame

        self.frames["Select_User_Company_State_Frame"] = None
        
        #self.show_frame("DisplayFrame")

    def login(self, i, Shops, User_data, User_work_shops):
            # hide all frames except the one to be shown
            Shops_info = {'Selected_Shop': Shops[i], 'Shops': Shops, 'User': User_data, 'User_Shops_List': User_work_shops, 'Shop_items': [], 'Shop_Actions': ""}
            #print("User11 : " + str(user[15]))
            self.display_frame = DisplayFrame(self, Shops_info, User_data, User_work_shops, Shops)
            self.display_frame.grid(row=0, column=0, sticky="nsew")
            self.frames["DisplayFrame"] = self.display_frame
            self.frames["DisplayFrame"].user = User_data
            self.frames["DisplayFrame"].Shops_info = Shops_info
            self.frames["DisplayFrame"].Shops = Shops
            self.frames["DisplayFrame"].User_Shops_List = User_work_shops
            #self.master.frames["DisplayFrame"].load()
            #self.master.show_frame("DisplayFrame")
            
    def self_focus(self):
        #print("focus main window")
        self.grab_set()
        self.focus_set()
        
    def show_frame(self, frame_name):
        # hide all frames except the one to be shown
        for frame in self.frames.values():
            if frame:
                frame.grid_remove()
        if frame_name in self.frames and self.frames[frame_name]:
            self.frames[frame_name].grid()
        #if frame_name == "DisplayFrame":
        #    self.frames[frame_name].search_entry.focus_set()

        # this will chaek if frame called is user create or show info
        # than it will display result of connection
        if frame_name == "User_Info_Frame" and self.frames[frame_name]:
            self.frames[frame_name].link_label.config(text="Link : " + self.link_entry.get())
            self.frames[frame_name].islinked_label.config(text=self.islinked_label.cget("text") , bg=self.islinked_label.cget("bg"))
            

        

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
