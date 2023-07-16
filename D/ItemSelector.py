import tkinter as tk

#TODO IF USER DONT WHAT TO DISPLAY QTY NEXT TO BUTTONS
class ItemSelectorWidget(tk.Tk):
    def __init__(self, parent, list, ischange_qty, given_qty):
        self.master = parent
        self.list = list
        self.ischange_qty = ischange_qty
        self.given_qty = given_qty

        self.getvalue_form = tk.Toplevel(self.master)
        self.getvalue_form.title("Selector Form")
        print("list ::" + str(self.list))

        self.item_list = self.read_code(self.list, "", "", "")[3]
        print("item_list ::" + str(self.item_list))
        self.current_form = 0
        self.forms = [
            self.display_shop_buttons,
            self.display_color_buttons,
            self.display_size_buttons,
            self.display_quantity_entry
        ]
        self.selected_shop = ""
        self.selected_color = ""
        self.selected_size = None
        self.selected_qty = 0
        self.selected_items = []
        self.star()   

    def star(self):
        self.form_frame = None
        self.current_form = 0
        self.next_form()

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

    def prev_form(self):
        if self.current_form > 0:
            self.current_form -= 1
            self.form_frame.destroy()
            self.next_form()

    def display_shop_buttons(self):
        self.selected_shop = ""
        self.selected_color = ""
        self.selected_size = None
        self.selected_qty = 0
        tk.Label(self.form_frame, text="Shop : " +  str(len(self.item_list))).pack()
        tk.Label(self.form_frame, text="Color:" + str(len(self.get_colors()))).pack()
        tk.Label(self.form_frame, text="Size : "+ str(len(self.get_sizes()))).pack()
        tk.Label(self.form_frame, text="Quantity : " + str((self.get_qtys()))).pack()
        tk.Label(self.form_frame, text="Select Shop:").pack()
        out = ""

        for shop in self.item_list:
            self.selected_shop = shop[0]
            ifqty = str(self.get_qtys())
            self.selected_shop = ""
            txt = shop[0]+"("+str(ifqty)+")"
            out = shop[0]
            tk.Button(self.form_frame, text=txt, command=lambda s=shop[0]: self.select_shop(s)).pack()
        button_count = sum(isinstance(child, tk.Button) for child in self.form_frame.winfo_children())
        if button_count == 1:
            self.select_shop(out)

    def select_shop(self, shop):
        self.selected_shop = shop
        self.current_form += 1
        self.next_form()

    def display_color_buttons(self):
        self.selected_color = ""
        self.selected_size = None
        self.selected_qty = 0
        tk.Label(self.form_frame, text="Color:" + str(len(self.get_colors()))).pack()
        tk.Label(self.form_frame, text="Size : "+ str(len(self.get_sizes()))).pack()
        tk.Label(self.form_frame, text="Quantity : " + str((self.get_qtys()))).pack()
        tk.Label(self.form_frame, text="Select Color:").pack()
        out = ""
        for color in self.get_colors():
            self.selected_color = color
            ifqty = str(self.get_qtys())
            self.selected_color = ""
            txt = color+"("+str(ifqty)+")"
            out = color
            tk.Button(self.form_frame, text=txt, command=lambda c=color: self.select_color(c)).pack()
        tk.Button(
            self.form_frame,
            text="Previous",
            command=self.prev_form
        ).pack()
        button_count = sum(isinstance(child, tk.Button) for child in self.form_frame.winfo_children())
        if button_count == 2:
            self.select_color(out)

    def select_color(self, color):
        self.selected_color = color
        self.current_form += 1
        self.next_form()

    def display_size_buttons(self):
        self.selected_size = None
        self.selected_qty = 0
        out = None
        tk.Label(self.form_frame, text="Size : "+ str(len(self.get_sizes()))).pack()
        tk.Label(self.form_frame, text="Quantity : " + str(self.get_qtys())).pack()
        tk.Label(self.form_frame, text="Select Size:").pack()
        for size in self.get_sizes():
            txt = size[0]+"("+str(size[3])+")"
            out = size
            tk.Button(self.form_frame,text=txt,command=lambda s=size: self.select_size(s)).pack()
        tk.Button(
            self.form_frame,
            text="Previous",
            command=self.prev_form
        ).pack()
        button_count = sum(isinstance(child, tk.Button) for child in self.form_frame.winfo_children())
        if button_count == 2 and out:
            self.select_size(out)

    def select_size(self, size):
        self.selected_size = size
        self.current_form += 1
        self.next_form()

    def display_quantity_entry(self):
        self.selected_qty = 0
        tk.Label(self.form_frame, text="Quantity : " + str(str(self.get_qtys()))).pack()
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
        
        #      button_count = sum(isinstance(child, tk.Button) for child in self.form_frame.winfo_children())
        #       if button_count == 2:
        #            self.select_size(txt)
        if float(self.selected_size[3]) == 1 and self.ischange_qty or self.given_qty > 1:
            self.selected_qty = self.given_qty
            self.add_to_cart()

    def add_to_cart(self):
        print("add_to_cart :")
        if self.selected_shop and self.selected_color and self.selected_size:
            print("add_to_cart :")
            if self.selected_qty == 0:
                self.selected_qty = self.qty_entry.get()
            item = [self.selected_shop, self.selected_color, self.selected_size, self.selected_qty]
            self.selected_items.append(item)
            print("true :" + str(self.selected_items[0]))

            self.show_selected_items()
        else:
            tk.messagebox.showerror("Error", "Please complete the selection.")

    def get_colors(self):
        colors = []
        for shop in self.item_list:
            if shop[0] == self.selected_shop:
                return [color[0] for color in shop[1]]
            for color in shop[1]:
                if not color[0] in colors:
                    colors.append(color[0])
        return colors

    def get_sizes(self):
        sizes = []
        for shop in self.item_list:
            if shop[0] == self.selected_shop:
                for color in shop[1]:
                    if color[0] == self.selected_color:
                        return color[1]
                for color in shop[1]:
                    for size in color[1]:
                        if not size[0] in sizes:
                            sizes.append(size[0])
                break
        if sizes == []:
            for shop in self.item_list:
                for color in shop[1]:
                    for size in color[1]:
                        if not size[0] in sizes:
                            sizes.append(size[0])
        return sizes
    
    def get_qtys(self):
        q = 0
        for shop in self.item_list:
            if shop[0] == self.selected_shop:
                for color in shop[1]:
                    if color[0] == self.selected_color:
                        for size in color[1]:
                            if self.selected_size == size:
                                return size[3]
                        for size in color[1]:
                            if size and float(size[3]) > 0:
                                print("qty1 : " + str(size) + " | " + str(size[3]) + "+" + str(q) + "="+ str(q + float(size[3])))
                                q += float(size[3])
                        break
                if q == 0:
                    for color in shop[1]:
                        for size in color[1]:
                            if size and float(size[3]) > 0:
                                print("qty2 : " + str(size) + " | " + str(size[3]) + "+" + str(q) + "="+ str(q + float(size[3])))
                                q += float(size[3])
                break
        if q == 0:
            for shop in self.item_list:
                for color in shop[1]:
                    for size in color[1]:
                        if size and float(size[3]) > 0:
                            print("qty3 : " + str(size) + " | " + str(size[3]) + "+" + str(q) + "="+ str(q + float(size[3])))
                            q += float(size[3])
        return q

    def show_selected_items(self):
        self.form_frame.destroy()
        self.create_form_frame()
        result_frame = tk.Frame(self.form_frame)
        result_frame.pack()
        tk.Label(result_frame, text="Selected Items:").pack()
        for item in self.selected_items:
            tk.Label(result_frame, text=str(item)).pack()
        tk.Button(
            self.form_frame,
            text="Add",
            command=lambda:self.add()
        ).pack()
        tk.Button(
            self.form_frame,
            text="Done",
            command=lambda: self.cancel_selection()
        ).pack()
        

    def add(self):
        self.form_frame.destroy()
        self.current_form = 0
        self.star()

    def cancel_selection(self):
        self.getvalue_form.destroy()

    #'''
if __name__ == "__main__":
    list = "\"{FLAG_SQUER,(<BROWN,[|XL, , 1, 0.0, , |]>)},\""

    root = tk.Tk()
    item_selector = ItemSelectorWidget(root, list, False, 1)
    root.mainloop()#'''
