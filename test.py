<<<<<<< HEAD
import tkinter as tk

class ItemSelectorWidget(tk.Tk):
    def __init__(self, parent, list, ischange_qty, given_qty):
        self.master = parent
        self.list = list
        self.ischange_qty = ischange_qty
        self.given_qty = given_qty

        self.getvalue_form = tk.Toplevel(self.master)
        self.getvalue_form.title("Selector Form")

        self.item_list = self.read_code(self.list, "", "", "")[3]
        print(str(self.item_list))
        self.current_form = 0
        self.forms = [
            self.display_shop_buttons,
            self.display_color_buttons,
            self.display_size_buttons,
            self.display_quantity_entry,
            self.show_selected_items
        ]
        self.selected_shop = ""
        self.selected_color = ""
        self.selected_size = ""
        self.selected_qty = 0
        self.selected_items = []
        self.form_frame = None

        self.next_form()
        
        #self.show_selected_items()

    def read_code(self, vs_info, shop_s, color_s, size_s):
        a_u_list = []
        shops = []
        colors = []
        sizes = []

        t = vs_info.replace("\"", "") + ","
        main_info = t.split("},")

        for m in range(len(main_info)-1):
            main_value = main_info[m].split(",(")
            shop_name = main_value[0].replace("{", "").strip()

            if shop_s == "" or shop_s == shop_name:
                shops.append(shop_name)

            shop = [shop_name]
            shop_node = []

            t = main_value[1].replace(")", "") + ","
            f_info = t.split(">,")
            
            for c in range(len(f_info)-1):
                f_value = f_info[c].split(",[")
                color_txt = f_value[0].replace("<", "").strip()

                if (not shop_s == "" and shop_s == shop_name) and \
                (color_s == "" or color_s == color_txt):
                    colors.append(color_txt)

                color = [color_txt]
                color_node = []

                t = f_value[1].replace("]", "") + ","
                s_info = t.split("|,")

                for s in range(len(s_info)-1):
                    s_value = s_info[s].split(", ")

                    if len(s_value) <= 1:
                        s_value = s_info[s].split(",")

                    s_n = []
                    for si in range(len(s_value)-1):
                        if (not shop_s == "" and shop_s == shop_name) and \
                        (not color_s == "" and color_s == color_txt) and \
                        (size_s == "" or size_s == s_value[si].replace("|", "").strip()):
                            if si == 0:
                                sizes.append(s_value[si].replace("|", "").strip())
                            elif si == 1:
                                self.selected_barcode.set(s_value[si].strip())

                        s_n.append(s_value[si].replace("|", "").strip())

                    color_node.append(s_n)
                
                color.append(color_node)
                shop_node.append(color)

            shop.append(shop_node)
            a_u_list.append(shop)

        return shops, colors, sizes, a_u_list
    
    def create_form_frame(self):
        self.form_frame = tk.Frame(self.getvalue_form)
        self.form_frame.pack()

    def next_form(self):
        if self.current_form < len(self.forms) and self.current_form < 4:
            if self.current_form > 0:
                self.form_frame.destroy()
                self.create_form_frame()
            else:
                self.create_form_frame()
            print("current_form : " + str(self.current_form))
            self.forms[self.current_form]()
            print("out forms: " + str(self.current_form))
            self.current_form += 1
        else:
            self.add_to_cart()

    def prev_form(self):
        if self.current_form > 1:
            self.selected_qty = 0
            self.current_form -= 2
            self.next_form()

    def display_shop_buttons(self):
        tk.Label(self.form_frame, text="Select Shop:").pack()
        txt = ""
        for shop in self.item_list:
            txt = shop[0]
            tk.Button(
                self.form_frame,
                text=shop[0],
                command=lambda s=shop[0]: self.select_shop(s)
            ).pack()
        if len(self.form_frame.winfo_children()) == 2:
            self.current_form += 1
            self.select_shop(txt)

    def select_shop(self, shop):
        self.selected_shop = shop
        self.next_form()

    def display_color_buttons(self):
        tk.Label(self.form_frame, text="Select Color:").pack()
        txt = ""
        for color in self.get_colors():
            txt=color
            tk.Button(
                self.form_frame,
                text=color,
                command=lambda c=color: self.select_color(c)
            ).pack()
        tk.Button(
            self.form_frame,
            text="Previous",
            command=self.prev_form
        ).pack()
        if len(self.form_frame.winfo_children()) == 3:
            self.current_form += 1
            self.select_color(txt)

    def select_color(self, color):
        self.selected_color = color
        self.next_form()

    def display_size_buttons(self):
        txt = ""
        tk.Label(self.form_frame, text="Select Size:").pack()
        for size in self.get_sizes():
            txt = size
            tk.Button(
                self.form_frame,
                text=size[0],
                command=lambda s=size[0]: self.select_size(s)
            ).pack()
        tk.Button(
            self.form_frame,
            text="Previous",
            command=self.prev_form
        ).pack()
        if len(self.form_frame.winfo_children()) == 3:
            print("txt :" + str(txt[3]))
            if txt[3] == '1' or txt[3] == "1.0":
                self.selected_qty = 1
                self.selected_size = txt
                self.add_to_cart()
            else:
                self.current_form += 1
                self.select_size(txt)

    def select_size(self, size):
        self.selected_size = size
        self.next_form()

    def display_quantity_entry(self):
        tk.Label(self.form_frame, text="Enter Quantity:").pack()
        self.qty_entry = tk.Entry(self.form_frame)
        self.selected_qty = 0
        self.qty_entry.insert(0, "1")
        self.qty_entry.pack()
        tk.Button(
            self.form_frame,
            text="Previous",
            command=self.prev_form
        ).pack()
        tk.Button(
            self.form_frame,
            text="Add to Cart",
            command=self.add_to_cart
        ).pack()

    def add_to_cart(self):
        print("add_to_cart :")
        if self.selected_shop and self.selected_color and self.selected_size:
            print("add_to_cart :")
            if self.selected_qty == 0:
                self.selected_qty = self.qty_entry.get()
            item = [self.selected_shop, self.selected_color, self.selected_size, self.selected_qty]
            self.selected_items.append(item)
            print("true :" + str(self.selected_items[0]))
            self.getvalue_form.destroy()
        else:
            tk.messagebox.showerror("Error", "Please complete the selection.")

    def get_colors(self):
        for shop in self.item_list:
            if shop[0] == self.selected_shop:
                return [color[0] for color in shop[1]]
        return []

    def get_sizes(self):
        for shop in self.item_list:
            if shop[0] == self.selected_shop:
                for color in shop[1]:
                    if color[0] == self.selected_color:
                        return color[1]
        return []

    def show_selected_items(self):
        self.form_frame.destroy()
        result_frame = tk.Frame(self.master)
        result_frame.pack()
        tk.Label(result_frame, text="Selected Items:").pack()
        for item in self.selected_items:
            tk.Label(result_frame, text=str(item)).pack()

    def cancel_selection(self):
        self.master.quit()

if __name__ == "__main__":
    #"\"{shopname1,(<color11,[|size111,barcode111, 30, 27.0, , |, |size112,barcode112, 30, 27.0, , |]>, <color12,[|size121,barcode121, 30, 27.0, , |, |size122,barcode122, 30, 27.0, , |]>)},{shopname2,(<color21,[|size211,barcode211, 30, 27.0, , |, |size212,barcode212, 30, 27.0, , |]>)}\""
    #"[[shopname1, [[color11, [[size111, barcode111, 30, 27.0, , ], [size112, barcode112, 30, 27.0, , ]]], [color12, [[size121, barcode121, 30, 27.0, , ], [size122, barcode122, 30, 27.0, , ]]]]], [shopname2, [[color21, [[size211, barcode211, 30, 27.0, , ], [size212, barcode212, 30, 27.0, , ]]]]]]"

    list = "\"{FLAG_SQUARE,(<FRUATE,[|1X30, , 30, 27.0, , |]>)},\""

    root = tk.Tk()
    item_selector = ItemSelectorWidget(root, list, False, None)
    root.mainloop()

'''
import tkinter as tk

class ItemSelectorWidget(tk.Tk):
    def __init__(self, parent, list, ischange_qty, given_qty):
        self.master = parent
        self.list = list
        self.ischange_qty = ischange_qty
        self.given_qty = given_qty

        self.getvalue_form = tk.Toplevel(self.master)
        self.getvalue_form.title("Selector Form")
        # calculate the center coordinates of the screen
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width / 2) - (500 / 2)  # 500 is the width of the Payment Form window
        y = (screen_height / 2) - (500 / 2)  # 500 is the height of the Payment Form window

        # set the position of the Payment Form window to center
        self.getvalue_form.geometry(f"200x200+{int(x)}+{int(y)}")

        self.selected_shop = tk.StringVar()
        self.selected_color = tk.StringVar()
        self.selected_size = tk.StringVar()
        self.selected_qty = tk.StringVar()
        self.selected_barcode = tk.StringVar()
        self.selected_items = []

        # Create the shop label and dropdown menu
        tk.Label(self.getvalue_form, text="Shop:").grid(row=0, column=0)
        self.shop_dropdown = tk.OptionMenu(self.getvalue_form, self.selected_shop, '')
        self.shop_dropdown.grid(row=0, column=1)
        self.shop_dropdown.bind('<Button-1>', self.get_shop)

        # Create the color label and dropdown menu
        tk.Label(self.getvalue_form, text="Color:").grid(row=1, column=0)
        self.color_dropdown = tk.OptionMenu(self.getvalue_form, self.selected_color, '')
        self.color_dropdown.grid(row=1, column=1)
        self.color_dropdown.bind('<Button-1>', self.get_color)

        # Create the size label and dropdown menu
        tk.Label(self.getvalue_form, text="Size:").grid(row=2, column=0)
        self.size_dropdown = tk.OptionMenu(self.getvalue_form, self.selected_size, '')
        self.size_dropdown.grid(row=2, column=1)
        self.size_dropdown.bind('<Button-1>', self.get_size)

        # Create the quantity label and entry field
        tk.Label(self.getvalue_form, text="Qty:").grid(row=3, column=0)
        self.qty_entry = tk.Entry(self.getvalue_form, textvariable=self.selected_qty)
        self.qty_entry.grid(row=3, column=1)

        # Create the Add to Cart button
        tk.Button(self.getvalue_form, text="Add to Cart", command=self.add_to_cart).grid(row=4, column=1)

        # show the Selector Form window
        self.get_auto()
    
    def get_auto(self):
        f = self.read_code(self.list, "", "", "")
        self.selected_shop.set(f[0][0])
        print("shop :" + str(f[0])[0])
        if len(f[0]) == 1: 
            s = self.read_code(self.list, f[0][0], "", "")
            print("color list :" + str(s))
            print("color :" + str(s[1])[0])
            self.selected_color.set(s[1][0])
            if len(s[1]) == 1: 
                t = self.read_code(self.list, f[0][0], s[1][0], "")
                print("list size :" + str(t))
                self.selected_size.set(t[2][0])
                print("size :" + str(t[2][0]))
                if len(t[2]) == 1 and self.ischange_qty or self.given_qty:
                    if not self.given_qty: 
                        self.selected_qty.set(1)
                        # TODO: get deffalute value
                    else:
                        self.selected_qty.set(self.given_qty)
                    item = [self.selected_shop.get(), self.selected_color.get(), self.selected_size.get(), self.selected_qty.get()]            
                    print("Item added to cart00:", item)
                    self.getvalue_form.destroy()
        
    def get_shop(self, t):
        ret = self.read_code(self.list, "", "", "")
        print("shop list :" + str(ret))
        print("shop :" + str(ret[0]))
        self.shop_dropdown['menu'].delete(0, 'end')
        for value in ret[0]:
            self.selected_shop.set(ret[0][0])
            self.shop_dropdown['menu'].add_command(label=value, command=tk._setit(self.selected_shop, value))
        print("shop value :" + self.selected_shop.get())
         
    def get_color(self, t):
        ret = self.read_code(self.list, self.selected_shop.get(), "", "")
        print("color list :" + str(ret))
        print("color :" + str(ret[1]))
        self.color_dropdown['menu'].delete(0, 'end')
        for value in ret[1]:
            self.selected_color.set(ret[1][0])
            self.color_dropdown['menu'].add_command(label=value, command=tk._setit(self.selected_color, value))
    
    def get_size(self, t):
        ret = self.read_code(self.list, self.selected_shop.get(), self.selected_color.get(), "")
        print("list size :" + str(ret))
        print("size :" + str(ret[2]))
        self.size_dropdown['menu'].delete(0, 'end')
        for value in ret[2]:
            self.selected_size.set(ret[2][0])
            self.size_dropdown['menu'].add_command(label=value, command=tk._setit(self.selected_size, value))
        #if len(ret[0]) == 1: 
            

    def read_code(self, vs_info, shop_s, color_s, size_s):
        a_u_list = []
        shops = []
        colors = []
        sizes  = []
        t = vs_info.replace("\"", "") + ","
        main_info = t.split("},")
        for m in range(len(main_info)-1):
            main_value = main_info[m].split(",(")
            shop_name = main_value[0].replace("{", "")
            if shop_s == "" or shop_s == shop_name:
                shops.append(shop_name)
            shop = [shop_name]
            shop_node = []
            t = main_value[1].replace(")", "") + ","
            f_info = t.split(">,")
            for c in range(len(f_info)-1):
                f_value = f_info[c].split(",[")
                color_txt = f_value[0].replace("<", "")
                if not shop_s == "" and shop_s == shop_name and \
                   color_s == "" or color_s == color_txt:
                    colors.append(color_txt)
                color = [color_txt]
                color_node = []
                t = f_value[1].replace("]", "") + ","
                s_info = t.split("|,")
                for s in range(len(s_info)-1):
                    s_value = s_info[s].split(", ")
                    if len(s_value) <= 1:
                        s_value = s_info[s].split(",")
                    s_n = []
                    si = 0
                    for s_v in s_value:
                        if not shop_s == "" and shop_s == shop_name and \
                        not color_s == "" and color_s == color_txt and \
                        size_s == "" or size_s == s_v.replace("|", ""):
                            if si == 0:
                                sizes.append(s_v.replace("|", ""))
                            elif si == 1:
                                self.selected_barcode.set(s_v.replace("|", ""))
                        print("value : " + s_v.replace("|", ""))
                        s_n.append(s_v.replace("|", ""))
                        color_node.append(s_n)
                        si += 1
                color.append(color_node)
                shop_node.append(color)
            shop.append(shop_node)
            a_u_list.append(shop)
        return shops, colors, sizes, a_u_list
    
    def add_to_cart(self):
        item = [self.selected_shop.get(), self.selected_color.get(), self.selected_size.get(), self.selected_qty.get()]
        print("Item added to cart:", item)
        self.selected_items.append(item)
        self.getvalue_form.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    list = "\"{FLAG_SQUER,(<NONE,[|1X10, 8906046682441, 21, 20.0, , |]>)},\""
    #list = "\"{Shop 1},({Color 1},[Size 1, Size 2]),({Color 2},[Size 1, Size 2])}\",\"{Shop 2},({Color 1},[Size 1, Size 2]),({Color 2},[Size 1, Size 2])}\""
    item_selector = ItemSelectorWidget(root, list, False, None)
    root.wait_window(item_selector.getvalue_form)
    print("Selected Items:", item_selector.selected_items)

'''
=======
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile
import os
import win32print
import tkinter as tk
from tkinter.simpledialog import Dialog

class PrinterDialog(Dialog):
    def __init__(self, parent, printers):
        self.printers = printers
        super().__init__(parent)

    def body(self, master):
        self.result = None
        tk.Label(master, text="Select a printer:").pack()
        self.printer_var = tk.StringVar()
        self.printer_var.set(self.printers[0])  # Default printer
        self.printer_menu = tk.OptionMenu(master, self.printer_var, *self.printers)
        self.printer_menu.pack()

    def apply(self):
        self.result = self.printer_var.get()

def generate_pdf(pdf_path):
    c = canvas.Canvas(pdf_path, pagesize=letter)

    # Add your content to the PDF here
    c.drawString(100, 700, "Product Name: Sample Product")
    c.drawString(100, 680, "Price: $10.99")
    # ... Add more content as needed

    c.save()

def print_pdf(pdf_path, printer_name):
    printer_handle = win32print.OpenPrinter(printer_name)

    try:
        win32print.StartDocPrinter(printer_handle, 1, ("PDF Document", None, "RAW"))
        win32print.StartPagePrinter(printer_handle)

        with open(pdf_path, "rb") as f:
            
            pdf_data = f.read()
        print(str(pdf_data))
        #win32print.WritePrinter(printer_handle, pdf_data)  # Remove len(pdf_data)

        win32print.EndPagePrinter(printer_handle)
        win32print.EndDocPrinter(printer_handle)
    finally:
        win32print.ClosePrinter(printer_handle)


def main():
    # Get available printer names
    printer_names = [printer[2] for printer in win32print.EnumPrinters(2)]

    if not printer_names:
        print("No printers available.")
        return

    # Display the printer selection dialog
    root = tk.Tk()
    dialog = PrinterDialog(root, printer_names)
    root.mainloop()
    
    if dialog.result:
        # Generate a temporary PDF file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_pdf_path = temp_file.name

        generate_pdf(temp_pdf_path)

        # Print the generated PDF using the selected printer
        print_pdf(temp_pdf_path, dialog.result)

        os.remove(temp_pdf_path)  # Clean up the temporary PDF file

if __name__ == "__main__":
    main()
>>>>>>> db9ae79 (adding seller)
