import tkinter as tk
from tkinter import ttk
import sqlite3, os

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

import requests

class UploadingForm(tk.Tk):
    def __init__(self, master):
        self.master = master
        
        # create a Toplevel window for the payment form
        self.getvalue_form = tk.Toplevel(self.master)
        self.getvalue_form.title("Uploading Form")
        self.update()
        
        
    
    def update(self):
        #'''
        # Fetch data from the database
        cursor.execute("SELECT * FROM upload_doc")
        b = cursor.fetchall()
        if len(b) > 0:
            # Convert the fetched data to a list of dictionaries
            for row in b:
                entry = {
                    'id': row[0],
                    'doc_barcode': str(row[1]),
                    'extension_barcode': str(row[2]),
                    'user_id': str(row[3]),
                    'customer_id': str(row[4]),
                    'type': str(row[5]),
                    'item': str(row[6]),
                    'qty': str(row[7]),
                    'price': str(row[8]),
                    'discount': str(row[9]),
                    'tax': str(row[10]),
                    'payments': str(row[11]),
                    'doc_created_date': str(row[12]),
                    'doc_expire_date': str(row[13]),
                    'doc_updated_date': str(row[14])
                }
                #print("row : " + str(row))
                #print("entry : " + str(entry))
                try:
                    # Send the data to the API
                    response = requests.post('http://localhost/Adot/update-api-endpoint.php', json=entry)

                    if response.status_code == 200:
                        print('Data sent successfully.')
                        updated_data = response.json()
                        if updated_data:
                            print("Updated data:", updated_data)
                        else:
                            print('Failed to retrieve data from the website.')
                except requests.exceptions.RequestException as e:
                    print('Failed to send data:', e)
            
        pass

        # set the position of the Payment Form window to center
        # TODO: list z report for current day and history z reports for pev days but in notbook 
        # TODO: TO Print dayly, weekly, monthly and yearly report as user whats
        # show the Payment Form window
        #'''
