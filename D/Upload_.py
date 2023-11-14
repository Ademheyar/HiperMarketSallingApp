import tkinter as tk
from tkinter import ttk
import sqlite3, os
import base64
import json

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

<<<<<<< HEAD
import requests
=======
#import requests
>>>>>>> db9ae79 (adding seller)

class UploadingForm(tk.Tk):
    def __init__(self, master):
        self.master = master
        
        # create a Toplevel window for the payment form
        self.getvalue_form = tk.Toplevel(self.master)
        self.getvalue_form.title("Uploading Form")
        self.update()
        
        
    
    def update(self):
<<<<<<< HEAD
        #'''
=======
        '''
>>>>>>> db9ae79 (adding seller)
        # Fetch data from the database
        url = 'http://localhost/Adot/update-api-endpoint.php'
        cursor.execute("SELECT * FROM upload_doc")
        b = cursor.fetchall()
        if len(b) > 0:
            ind = -1
            # Convert the fetched data to a list of dictionaries
            for row in b:
                ind += 1
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
                print("\n\nentry : " + str(entry))
                #print("\n\nentry : " + str(entry['item']))
                try:
                    # Send the data to the API
                    response = requests.post(url, json=entry)

                    if response.status_code == 200:
                        print('Data sent successfully.')
                        response_data = response.json()
                        if response_data['status'] == 'Get_Items_image':
                            new_row = response_data['row']
                            print('Get_Items_image:', str(new_row))
                            new_row.replace(" ", "")
                            items_path = new_row.split(",")
                            for path in items_path:
                                if path == "":
                                    break
                                image_data = None
                                with open(path, 'rb') as file:
                                    image_data = file.read()
                                if not image_data == None:
                                    encoded_image_data = base64.b64encode(image_data).decode('utf-8')
                                    print('image_data:', str("encoded_image_data"))
                                    image_entry = {'type': 'Update_Image', 'image': encoded_image_data}
                                    image_response = requests.post(url, json=image_entry)
                                    try:
                                        image_response_data = image_response.json()
                                        if image_response.status_code == 200:
                                            print('Saved data:', image_response_data['message'])
                                            imahe_new_row = response_data['row']
                                            print('Data sent successfully.')
                                            print('Newly added row:', imahe_new_row)
                                        else:
                                            print('Failed to save image:', image_response_data['message'])
                                    except json.JSONDecodeError as e:
                                        print('Error: Response is not valid JSON.', str(e))

                        elif response_data['status'] == 'success':
                            print('Saved data:', response_data['message'])
                            new_row = response_data['row']
                            print('row:', new_row)
                            if ind != len(b) -1:
                                cursor.execute("DELETE FROM upload_doc WHERE id=?", (row[0],))
                                
                                # Commit the changes to the database
                                conn.commit()
                                print('Newly added row:', new_row)
                            
                        else:
                            print('Failed to save data:', response_data['message'])
                            break;
                    else:
                        print('Failed to retrieve data from the website.')
                except requests.exceptions.RequestException as e:
                    print('Failed to send data:', e)
                print('\n\n\n')
            
        # set the position of the Payment Form window to center
        # TODO: list z report for current day and history z reports for pev days but in notbook 
        # TODO: TO Print dayly, weekly, monthly and yearly report as user whats
        # show the Payment Form window
        #'''
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = UploadingForm(root)
<<<<<<< HEAD
    root.mainloop()
=======
    root.mainloop()
>>>>>>> db9ae79 (adding seller)
