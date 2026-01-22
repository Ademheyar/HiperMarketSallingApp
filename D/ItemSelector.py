
import os
import atexit
import sys
import tkinter as tk

current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(current_dir, '..')
sys.path.append(MAIN_dir)

from D.GetVALUE import GetvalueForm
from D.iteminfo import *
from C.List import *

#TODO IF USER DONT WHAT TO DISPLAY QTY NEXT TO BUTTONS
class ItemSelectorWidget(tk.Tk):
    def __init__(self, parent, def_code, list, ischange_qty, given_qty):
        self.master = parent
        self.list = list.replace(" ", "")
        self.ischange_qty = ischange_qty
        self.given_qty = given_qty
        self.btns = []
        self.def_value = 0
        self.focused_btn_index = 0
        #print("given_qty ::" + str(given_qty))
        self.getvalue_form = tk.Toplevel(self.master)
        self.getvalue_form.bind("<Up>", self.select_button)
        self.getvalue_form.bind("<Down>", self.select_button)
        self.getvalue_form.bind("<Escape>", lambda _: self.getvalue_form.destroy())
        self.getvalue_form.title("Selector Form")
        #print("list ::" + str(self.list))
        if self.list == "":
            return
        elif "\"{" in self.list:
            def_code_ = str(def_code).replace(",", "|")
            self.item_list = read_code(self.list, "", def_code_, "", "")[4]
        else:
            self.item_list = load_list(self.list)
        #print("item_list ::" + str(self.item_list))
        self.current_form = 0
        self.forms = [
            self.display_shop_buttons,
            self.display_code_buttons,
            self.display_color_buttons,
            self.display_size_buttons,
            self.display_quantity_entry
        ]
        self.selected_shop = ""
        self.selected_code = ""
        self.selected_color = ""
        self.elected_size = ""
        self.selected_value = None
        self.selected_qty = 0
        self.selected_items = []
        self.star()
        
    def select_button(self, event):
        child_buttons = self.form_frame.winfo_children()
        focused_widget = event.widget
        next_index = 0
        if self.focused_btn_index < len(self.btns):
            if event.keysym == "Up":
                if self.focused_btn_index-1 >= 0:
                    next_index = self.focused_btn_index-1
                else:
                    next_index = len(self.btns)-1
            elif event.keysym == "Down":
                if self.focused_btn_index+1 < len(self.btns):
                    next_index = self.focused_btn_index+1
                else:
                    next_index = 0
            else:
                return
            next_button = self.btns[next_index][1]
            self.focused_btn_index = next_index
            next_button.focus_set()
            for btn in child_buttons:
                if btn.winfo_class() == "Button":
                    btn.configure(bg="white")
            next_button.configure(bg="lightblue")
        
    def star(self):
        self.form_frame = None
        self.current_form = 0
        self.next_form()

    def create_form_frame(self):
        self.form_frame = tk.Frame(self.getvalue_form)
        self.form_frame.pack()

    def next_form(self):
        #print("self.current_form < len(self.forms) :"+str(len(self.forms)))
        if self.current_form < len(self.forms):
            if self.current_form > 0:
                self.form_frame.destroy()
                self.create_form_frame()
            else:
                self.current_form = 0
                self.create_form_frame()
            #print("current_form : " + str(self.current_form))
            self.forms[self.current_form]()
            #print("out forms: " + str(self.current_form))

    def prev_form(self):
        if self.current_form > 0:
            self.current_form -= 1
            self.form_frame.destroy()
            if self.current_form-1 > 0:
                print("going prev greter 0")
                self.getvalue_form.bind("<Escape>", lambda _: self.prev_form())
            else:
                print("going prev less 0")
                self.getvalue_form.bind("<Escape>", lambda _: self.getvalue_form.destroy())
            self.next_form()

    def display_shop_buttons(self):
        self.selected_shop = ""
        self.selected_code = ""
        self.selected_color = ""
        self.selected_value = None
        self.selected_size = None
        tk.Label(self.form_frame, text="Shop : " +  str(len(self.item_list))).pack()
        tk.Label(self.form_frame, text="code:" + str(len(self.get_codes()))).pack()
        tk.Label(self.form_frame, text="Color:" + str(len(self.get_colors()))).pack()
        tk.Label(self.form_frame, text="Size : "+ str(len(self.get_sizes()))).pack()
        tk.Label(self.form_frame, text="Quantity : " + str((self.get_qtys()))).pack()
        tk.Label(self.form_frame, text="Select Shop:").pack()
        out = ""
        self.btns = []
        for shop in self.item_list:
            self.selected_shop = shop[0]
            print("shop :"+str(shop[0]))
            ifqty = str(self.get_qtys())
            self.selected_shop = ""
            print("ifqty in shop :"+str(ifqty))
            txt = shop[0]+"("+str(ifqty)+")"
            out = shop[0]
            b=tk.Button(self.form_frame, text=txt, command=lambda s=shop[0]: self.select_shop(s))
            #b.pack()
            self.btns.append((float(ifqty), b))
            b.bind("<Return>", lambda _, s=shop[0]: self.select_shop(s))
        self.btns.sort(key=lambda x:x[0], reverse=True)
        u = 0
        for _, btn in self.btns:
            btn.pack()
            if u == 0:
                u = 1
                btn.focus_set()
                btn.configure(bg="lightblue")
            else:
                btn.configure(bg="white")
                
        self.form_frame.winfo_children()[0].focus_set()    
        button_count = sum(isinstance(child, tk.Button) for child in self.form_frame.winfo_children())
        if button_count == 1:
            self.select_shop(out)

    def select_shop(self, shop):
        self.selected_shop = shop
        self.current_form += 1
        self.next_form()

    def display_code_buttons(self):
        self.selected_code = ""
        self.selected_color = ""
        self.selected_value = ""
        self.selected_size = None
        tk.Label(self.form_frame, text="Code:" + str(len(self.get_codes()))).pack()
        tk.Label(self.form_frame, text="Color:" + str(len(self.get_colors()))).pack()
        tk.Label(self.form_frame, text="Size : "+ str(len(self.get_sizes()))).pack()
        tk.Label(self.form_frame, text="Quantity : " + str(self.get_qtys())).pack()
        tk.Label(self.form_frame, text="Select Color:").pack()
        out = ""
        self.btns = []
        for code in self.get_codes():
            self.selected_code = code
            #print("code :"+str(code))
            ifqty = str(self.get_qtys())
            #print("ifqty in code :"+str(ifqty))
            self.selected_code = ""
            txt = code+"("+str(ifqty)+")"
            out = code
            b = tk.Button(self.form_frame, text=txt, command=lambda c=code: self.select_code(c))
            #b.pack()
            self.btns.append((float(ifqty), b))
            b.bind("<Return>", lambda _, c=code: self.select_code(c))

        self.btns.sort(key=lambda x:x[0], reverse=True)
        u = 0
        for _, btn in self.btns:
            btn.pack()
            if u == 0:
                u = 1
                btn.focus_set()
                btn.configure(bg="lightblue")
            else:
                btn.configure(bg="white")
        p=tk.Button(
            self.form_frame,
            text="Previous",
            command=self.prev_form
        )
        p.pack()
        p.bind("<Return>", lambda _: self.prev_form())
        
        self.form_frame.winfo_children()[0].focus_set()
        button_count = sum(isinstance(child, tk.Button) for child in self.form_frame.winfo_children())
        if self.selected_qty != None and button_count == 2:
            self.select_code(out)

    def select_code(self, code):
        self.selected_code = code
        self.current_form += 1
        self.next_form()
        
    def display_color_buttons(self):
        self.selected_color = ""
        self.selected_value = ""
        self.selected_size = None
        tk.Label(self.form_frame, text="Color:" + str(len(self.get_colors()))).pack()
        tk.Label(self.form_frame, text="Size : "+ str(len(self.get_sizes()))).pack()
        tk.Label(self.form_frame, text="Quantity : " + str((self.get_qtys()))).pack()
        tk.Label(self.form_frame, text="Select Color:").pack()
        out = ""
        self.btns = []
        for color in self.get_colors():
            self.selected_color = color
            #print("color :"+str(color))
            ifqty = str(self.get_qtys())
            #print("ifqty in color :"+str(ifqty))
            self.selected_color = ""
            txt = color+"("+str(ifqty)+")"
            out = color
            b = tk.Button(self.form_frame, text=txt, command=lambda c=color: self.select_color(c))
            #b.pack()
            self.btns.append((float(ifqty), b))
            b.bind("<Return>", lambda _, c=color: self.select_color(c))

        self.btns.sort(key=lambda x:x[0], reverse=True)
        u = 0
        for _, btn in self.btns:
            btn.pack()
            if u == 0:
                u = 1
                btn.focus_set()
                btn.configure(bg="lightblue")
            else:
                btn.configure(bg="white")
        p=tk.Button(
            self.form_frame,
            text="Previous",
            command=self.prev_form
        )
        p.pack()
        p.bind("<Return>", lambda _: self.prev_form())
        
        self.form_frame.winfo_children()[0].focus_set()
        button_count = sum(isinstance(child, tk.Button) for child in self.form_frame.winfo_children())
        if self.selected_qty != None and button_count == 2:
            self.select_color(out)

    def select_color(self, color):
        self.selected_color = color
        self.current_form += 1
        self.next_form()

    def display_size_buttons(self):
        self.selected_size = None
        self.selected_value = ""
        out = None
        tk.Label(self.form_frame, text="Size : "+ str(len(self.get_sizes()))).pack()
        tk.Label(self.form_frame, text="Quantity : " + str(self.get_qtys())).pack()
        tk.Label(self.form_frame, text="Select Size:").pack()
        self.btns = []
        for size in self.get_sizes():
            self.selected_size = size
            #print("size :"+str(size))
            ifqty = str(self.get_value())
            value = self.get_values()
            self.selected_size = ""
            txt = size+"("+str(ifqty)+")"
            out = size
            b=tk.Button(self.form_frame,text=txt,command=lambda s=size, v=value[0]: self.select_size(s, v))
            
            self.btns.append((float(ifqty), b))
            b.bind("<Return>", lambda _, s=size, v=value[0]: self.select_size(s, v))

        self.btns.sort(key=lambda x:x[0], reverse=True)
        u = 0
        for _, btn in self.btns:
            btn.pack()
            if u == 0:
                u = 1
                btn.focus_set()
                btn.configure(bg="lightblue")
            else:
                btn.configure(bg="white")
                
        p=tk.Button(
            self.form_frame,
            text="Previous",
            command=self.prev_form
        )
        p.pack()
        p.bind("<Return>", lambda _: self.prev_form())
        self.form_frame.winfo_children()[0].focus_set()
        button_count = sum(isinstance(child, tk.Button) for child in self.form_frame.winfo_children())
        if self.selected_qty != None and button_count == 2 and out:
            self.select_size(out, None)

    def select_size(self, size, value):
        self.selected_size = size
        if value == None:
            value = self.get_values()[0]
        self.selected_value = value
        self.current_form += 1
        self.next_form()

    def display_quantity_entry(self):
        if self.selected_qty == None:
            self.selected_qty = 0
        tk.Label(self.form_frame, text="Quantity : " + str(str(self.get_qtys()))).pack()
        tk.Label(self.form_frame, text="").pack()
        #print("self.selected_value[2] : " +str(self.selected_value))
        #print("self.ischange_qty : " +str(self.ischange_qty))
        
        #print("self.given_qty : " +str(self.given_qty))
        if self.given_qty > 1 and self.def_value == 0:
            self.selected_qty = self.given_qty
            self.add_to_cart()
            self.def_value = 1
            return
        
        if self.def_value == 0 and (float(self.selected_value[2]) == 1 or self.ischange_qty):
            self.selected_qty = 1
            self.add_to_cart()
            self.def_value = 1
            return
        
        i = GetvalueForm(self.getvalue_form, "1", "Enter Quantity")
        if i.value and float(i.value) > 0:
            self.selected_qty = float(i.value)
            self.add_to_cart()
        else:
            self.selected_qty = None
            self.prev_form()
        
        #      button_count = sum(isinstance(child, tk.Button) for child in self.form_frame.winfo_children())
        #       if button_count == 2:
        #            self.select_size(txt)
        

    def add_to_cart(self):
        #print("add_to_cart :")
        if self.selected_shop and self.selected_color and self.selected_size:
            #print("add_to_cart :")
            if self.selected_qty == 0:
                self.selected_qty = self.qty_entry.get()
            item = [self.selected_shop, self.selected_code, self.selected_color, self.selected_size, self.selected_value, self.selected_qty]
            self.selected_items.append(item)
            #print("true :" + str(self.selected_items[0]))
            #tk.messagebox.showerror("Error", "Please complete the selection.")
            self.show_selected_items()

    def get_codes(self):
        codes = []
        for shop in self.item_list:
            if shop[0] == self.selected_shop:
                return [code[0] for code in shop[1]]
            for code in shop[1]:
                if not code[0] in codes:
                    codes.append(code[0])
        return codes
    
    def get_colors(self):
        colors = []
        for shop in self.item_list:
            if shop[0] == self.selected_shop:
                for codes in shop[1]:
                    if codes[0] == self.selected_code:
                        return [color[0] for color in codes[1]]

            for code in shop[1]:
                for color in code[1]:
                    if not color[0] in colors:
                        colors.append(color[0])
        return colors

    def get_sizes(self):
        sizes = []
        q = None
        qq = -1
        for shop in self.item_list:
            if shop[0] == self.selected_shop:
                for codes in shop[1]:
                    if codes[0] == self.selected_code:
                        for color in codes[1]:
                            if color[0] == self.selected_color:
                                for size in color[1]:
                                    if size[0] == self.selected_size:
                                        return size[1]
                                if q == None:
                                    q=0
                                    for size in color[1]:
                                        if not size[0] in sizes:
                                            sizes.append(size[0])   
                                    if qq == 0 and q == None:
                                        q = 0
                                    break
                        if q == None:
                            q=0
                            for color in codes[1]:
                                for size in color[1]:
                                    if not size[0] in sizes:
                                        sizes.append(size[0])
                            break
            if q == None:
                q=0
                for code in shop[1]:
                    for color in code[1]:
                        for size in color[1]:
                            if not size[0] in sizes:
                                sizes.append(size[0])
                if qq == 0 and q == None:
                    q = 0
                break
        if q == None:
            q=0
            for shop in self.item_list:
                for code in shop[1]:
                    for color in code[1]:
                        for size in color[1]:
                            if not size[0] in sizes:
                                sizes.append(size[0])
        return sizes

    def get_values(self):
        values = []
        for shop in self.item_list:
            if shop[0] == self.selected_shop:
                for codes in shop[1]:
                    if codes[0] == self.selected_code:
                        for color in codes[1]:
                            if color[0] == self.selected_color:
                                for size in color[1]:
                                    if size[0] == self.selected_size:
                                        return size[1]
                if q == None:
                    q=0
                    for color in shop[1]:
                        for sizes in color[1]:
                            if not size[0] in sizes:
                                values.append(size[0])
                break
        if values == []:
            for shop in self.item_list:
                for color in shop[1]:
                    for size in color[1]:
                        if not size[0] in sizes:
                            values.append(size[0])
        return values
    
    def get_qtys(self):
        q = None
        qq = -1
        for shop in self.item_list:
            if shop[0] == self.selected_shop:
                for codes in shop[1]:
                    if codes[0] == self.selected_code:
                        for color in codes[1]:
                            if color[0] == self.selected_color:
                                for size in color[1]:
                                    if self.selected_size == size[0]:
                                        return size[1][0][2]
                                if q == None:
                                    q=0
                                    #print("gettting color values :"+str(color))
                                    for size in color[1]: 
                                        for value in size[1]:
                                            #print("qty1 : " + str(value) + " | " + str(value[2]) + "+" + str(q) + "="+ str(q + float(value[2])))
                                            if q != None and float(value[2]) > 0:
                                                q += float(value[2])
                                            elif float(value[2]) > 0:
                                                q = float(value[2])
                                            else:
                                                qq = 0    
                                    if qq == 0 and q == None:
                                        q = 0
                                    break
                        if q == None:
                            q=0
                            for color in codes[1]:
                                for size in color[1]:
                                    for value in size[1]:
                                        if float(value[2]) > 0:
                                            #print("qty2 : " + str(value) + " | " + str(value[2]) + "+" + str(q) + "="+ str(q + float(value[2])))
                                            q += float(value[2])
                            break
            if q == None:
                q=0
                for code in shop[1]:
                    for color in code[1]:
                        for size in color[1]:
                            for value in size[1]:
                                if float(value[2]) > 0:
                                   # print("qty3 : " + str(value) + " | " + str(value[2]) + "+" + str(q) + "="+ str(q + float(value[2])))
                                    q += float(value[2])
                if qq == 0 and q == None:
                    q = 0
                break
        if q == None:
            q=0
            for shop in self.item_list:
                for code in shop[1]:
                    for color in code[1]:
                        for size in color[1]:
                            for value in size[1]:
                                if float(value[2]) > 0:
                                    #print("qty4 : " + str(value) + " | " + str(value[2]) + "+" + str(q) + "="+ str(q + float(value[2])))
                                    q += float(value[2])
        #print("ggghggggggggQTY q : " + str(q))      
        return q

    def get_value(self):
        q = None
        qq = -1
        for shop in self.item_list:
            if shop[0] == self.selected_shop:
                for codes in shop[1]:
                    if codes[0] == self.selected_code:
                        for color in codes[1]:
                            if color[0] == self.selected_color:
                                for size in color[1]:
                                    if size[0] == self.selected_size:
                                        return size[1][0][2]
                        
                        for size in color[1]: 
                            for value in size[1]:
                                if q != None and float(value[2]) > 0:
                                    q += float(value[2])
                                elif float(value[2]) > 0:
                                    q = float(value[2])
                                else:
                                    qq = 0
                            #print("qty1 : " + str(size) + " | " + str(size[3]) + "+" + str(q) + "="+ str(q + float(size[3])))
                            if qq == 0 and q == None:
                                q = 0
                            break
                        break
                if q == None:
                    q=0
                    for color in shop[1]:
                        for size in color[1]:
                            for value in size[1]:
                                if float(value[2]) > 0:
                                    q += float(value[2])
                                #print("qty2 : " + str(size) + " | " + str(size[3]) + "+" + str(q) + "="+ str(q + float(size[3])))
                if qq == 0 and q == None:
                    q = 0
                break
        if q == None:
            q=0
            for shop in self.item_list:
                for code in shop[1]:
                    for color in code[1]:
                        for size in color[1]:
                            for value in size[1]:
                                if float(value[2]) > 0:
                                    q += float(value[2])
                            #print("qty3 : " + str(size) + " | " + str(size[3]) + "+" + str(q) + "="+ str(q + float(size[3])))
        #print("q : " + str(q))
                            
        return q
    
    def show_selected_items(self):
        self.form_frame.destroy()
        self.create_form_frame()
        result_frame = tk.Frame(self.form_frame)
        result_frame.pack()
        tk.Label(result_frame, text="Selected Items:").pack()
        for item in self.selected_items:
            tk.Label(result_frame, text=str(item)).pack()
        a=tk.Button(
            self.form_frame,
            text="Add(ESC)",
            command=lambda:self.add()
        )
        a.configure(bg="white")
        a.pack()
        self.getvalue_form.bind("<Return>", lambda _: self.add())
        d=tk.Button(
            self.form_frame,
            text="Done(Enter)",
            command=lambda: self.cancel_selection()
        )
        
        d.focus_set()
        d.configure(bg="lightblue")
        self.btns = []
        self.btns.append((1, a))
        self.btns.append((2, d))
        self.focused_btn_index = 1        
        d.pack()
        d.bind("<Return>", lambda _: self.cancel_selection())
        self.form_frame.winfo_children()[0].focus_set()
        def pp():
            self.current_form = 1
            self.prev_form()
        self.getvalue_form.bind("<Escape>", lambda _: pp())
        #if float(self.selected_value[2]) == 1 or self.ischange_qty or self.given_qty > 1:
        #    self.cancel_selection()

    def add(self):
        self.form_frame.destroy()
        self.current_form = 0
        self.star()

    def cancel_selection(self):
        self.getvalue_form.destroy()

    '''
if __name__ == "__main__":
    list = "\"{FLAG_SQUER,(<BROWN,[|XL, , 1, 0.0, , |]>)},\""

    root = tk.Tk()
    item_selector = ItemSelectorWidget(root, list, False, 1)
    root.mainloop()#'''
