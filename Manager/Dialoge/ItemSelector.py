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

        # show the Payment Form window
        #self.getvalue_form.transient(self.master)
        #self.getvalue_form.grab_set()
        #self.master.wait_window(self.getvalue_form)
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
                print("size :" + str(t[2][0]))
                self.selected_size.set(t[2][0])
                if len(t[2]) == 1 and self.ischange_qty or self.given_qty:
                    if not self.given_qty: 
                        self.selected_qty.set(1)
                        # TODO: get deffalute value
                    else:
                        self.selected_qty.set(self.given_qty)
                    item = [self.selected_shop.get(), self.selected_color.get(), self.selected_size.get(), self.selected_qty.get()]            
                    print("Item added to cart:", item)
                    self.getvalue_form.destroy()
                else:
                    self.master.wait_window(self.getvalue_form)
        
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
    
    #def get_shop_names(self, vs_info):
        
    #def get_colors_names(self):

    #def get_size_names(self):

    def add_to_cart(self):
        item = [self.selected_shop.get(), self.selected_color.get(), self.selected_size.get(), self.selected_qty.get()]
        '''
        self.selected_items.append(item)
        self.selected_shop.set("")
        self.selected_color.set("")
        self.selected_size.set("")
        self.selected_qty.set("")
        '''
        print("Item added to cart:", item)
        self.getvalue_form.destroy()

'''
# Example usage:
root = tk.Tk()

# Define the shop, color, and size lists
list = "\"{shop1,(<color11,[|size,4,4,4,,|]>, <color11,[|3,4,4,4,,|]>)}, {shop2,(<color,[|size,4,4,4,,|]>)}\""
# Create the ItemSelectorWidget and add it to the root window
item_selector = ItemSelectorWidget(root, list)
item_selector.pack()

root.mainloop()
'''