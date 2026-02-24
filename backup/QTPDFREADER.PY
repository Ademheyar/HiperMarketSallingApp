import tkinter as tk
from tkinter import ttk

import random


nodes = [["a"]]
class NodeSelectorApp():
    def __init__(self, frame, def_value, get_nodes_t):
        self.root = frame
        
        get_nodes = self.load_list(get_nodes_t)[0]
        print("nodes : "+str(get_nodes))
        self.node_combobox = ttk.Combobox(self.root, state="readonly")
        self.node_combobox.pack(fill=tk.X, pady=10)
        self.node_combobox.bind("<<ComboboxSelected>>", self.update_node_selection)
        self.nodes = get_nodes
        self.get_value = def_value
        self.selected_nodes = []
        
        self.node_hierarchy = get_nodes
        self.listed_nodes_parents = []

        # Create main frame to display selected nodes and parents
        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.pack(fill=tk.X)

        self.focused_group = 0

        
        self.update_combobox_values()
        self.update_list()
        
    def load_list(self, text):
        def sub_list(t, i):
            print("\n reding next t = " +str(t)+"on line "+str(i))
            rv = ''
            pp = ""
            rl = []
            while i < len(t):
                if t[i] == '\'':
                    i+=1
                if t[i] == "[":
                    i+=1
                    i, v = sub_list(t, i)
                    rl.append(v)
                    continue
                
                if t[i] == "]":
                    if t[i+1] == "]" or t[i+1] == ",":
                        if rv != "":
                            rl.append(rv)
                            pp += str(rv) + "2"
                        i+=1
                        return i, rl
                    i+=1
                    continue
                
                if t[i] == ",":
                    if rv != "":
                        rl.append(rv)
                    i+=1
                    rv = ""
                    continue
                
                if rv != "" and (t[i+1] == "," or t[i+1] == "]"):
                    rv += t[i]
                    rl.append(rv)
                    pp += str(rv) + "3"
                    i+=1
                    rv = ""
                    if t[i+1] == "]":
                        return i, rl
                else:
                    rv += t[i]
                    i+=1
            return i, rl
        return sub_list(text+",", 0)[1]
    def load_type(self, type_str):
        loaded_str = ""
        ts = type_str.split(";")
        for tps in ts:
            loaded_n = nodes
            s_l = []
            tpsl = tps.split(",")
            for tp in tpsl:
                if int(tp) < len(loaded_n) and loaded_n[int(tp)]:
                    loaded_n = loaded_n[int(tp)]
                    s_l.append(int(tp))
                else:
                    break
            self.selected_nodes.append(s_l)
        #self.update_selected()
    def update_selected(self):
        self.update_selected()

        
    def isthere(self, i, value):
        if i == -1:
            def sub(l):
                for it in l:
                    if it[0] == value:
                        return True
                    elif it[1]:
                        if sub(it[1]):
                            return True
            return sub(self.nodes)
        elif i >= 0:
            print("chacking value " + str(value) + "on list " + str(i))
            def sub(l, j):
                for it in l:
                    if j < 0 or j > i:
                        return False
                    elif j == i and it[0] == value:
                        return True
                    elif it[1] and sub(it[1], j+1):
                        return True
            return sub(self.nodes, 0)
        return False
    
    def get_index(self, i, value):
        def sub(l):
                for j, it in enumerate(l):
                    if it[0] == value:
                        return j
                    elif it[1]:
                        return sub(it[1])
        return sub(self.nodes)
    
    def exit_childe(self, event):
        if event.cget('bg') == "red":
            event.destroy()
            m = self.nodes
            if len(self.selected_nodes) > self.focused_group:
                self.selected_nodes[self.focused_group].remove(self.selected_nodes[self.focused_group][len(self.selected_nodes[self.focused_group])-1])
                s = 0
                for i, j in enumerate(self.selected_nodes[self.focused_group]):
                    m = m[j][1]
            self.node_hierarchy = m
            self.update_combobox_values()
            self.update_values()
        else:
            event.config(bg="red")
            
    def update_list(self):
        # Clear previous widgets in the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.selected_nodes = []
        for i2, spand in enumerate((self.get_value + ';#').split(';')):
            if spand == '#':
                continue
            fcolor = None
            if self.focused_group == i2:
                fcolor = "blue"
            g_frame = tk.Frame(self.main_frame, bg=fcolor)
            g_frame.pack(fill="x")
            g_frame.bind("<Button-1>", lambda _, a=g_frame: self.foucsed_main(a))
            g_frame.bind("<Button-3>", lambda _, a=g_frame: self.exit_main(a))
            g_ = []
            for i3, spluse in enumerate((spand + '+').split('+')):
                if spluse == '':
                    continue
                print("i3 " + str(i3))
                color = "white"
                if self.isthere(i3, spluse):
                    color = "Green"
                elif not self.isthere(-1, spluse):
                    color = "orange"
                else:
                    color = "white"
                g_.append(self.get_index(i3, spluse))
                #todo make def color giving
                parent_button = tk.Button(g_frame, text=str(spluse), bg=color, fg="white")
                parent_button.bind("<Button-3>", lambda _, a=parent_button: self.exit_childe(a))
                parent_button.grid(row=0, column=len(g_frame.winfo_children())+1)
            if len(g_) > 0:
                self.selected_nodes.append(g_)
                print("parantes : " + str(g_))
                    
    def update_values(self):
        new_v = ""
        for j, widget in enumerate(self.main_frame.winfo_children()):
            if new_v != "":
                new_v += ";"
            n_chiled = ""
            for widget_c in widget.winfo_children():
                if not n_chiled == "":
                    n_chiled += "+"
                n_chiled += widget_c.cget('text')
            new_v += n_chiled
                
        self.get_value = new_v
        print("self.get_value = " + str(self.get_value))
        self.update_list()
            
    def update_combobox_values(self):
        print("ss "+ str([";"] + [name[0] for name in self.node_hierarchy]))
        self.node_combobox["values"] = [";"] + [name[0] for name in self.node_hierarchy]

    def get_all_subnodes(self, parent_node_dict, parent_nodes, node):
        subnodes = []
        for subnode, subnode_dict in node.items():
            self.listed_nodes_parents.append((parent_node_dict, parent_nodes))
            subnodes.append(subnode)
            subnodes.extend(self.get_all_subnodes(subnode_dict, parent_nodes + [subnode], subnode_dict))
        return subnodes
    
    def foucsed_main(self, event):
        for j, widget in enumerate(self.main_frame.winfo_children()):
            if widget == event:
                self.focused_group = j
                event.config(bg="blue")
            else:
                widget.config(bg="white")
        
    def exit_main(self, event):
        event.destroy()
        
    def update_node_selection(self, event):
        selected_node = self.node_combobox.get()
        selected_index = self.node_combobox.current()
        if selected_node:
            if (selected_index == 0):
                t = tk.Frame(self.main_frame, bg="blue")
                t.pack(fill="x")
                t.bind("<Button-1>", lambda _, a=t: self.foucsed_main(a))
                t.bind("<Button-3>", lambda _, a=t: self.exit_main(a))
                self.focused_group = len(self.main_frame.winfo_children())-1
                self.node_hierarchy = self.nodes
                
            else:
                self.node_hierarchy = self.node_hierarchy[selected_index-1][1]
                fcolor = None
                if self.focused_group == self.selected_nodes:
                    fcolor = "blue"
                        
                color = "gray"
                if self.isthere(len(self.selected_nodes), str(selected_node)):
                    color = "Green"
                elif not self.isthere(-1, str(selected_node)):
                    color = "orange"
                else:
                    color = "white"
                        
                g_frame = None
                if self.focused_group < len(self.main_frame.winfo_children()) and selected_index > 0:
                    g_frame = self.main_frame.winfo_children()[self.focused_group]
                else:
                    g_frame = tk.Frame(self.main_frame, bg=fcolor)
                    g_frame.pack(fill="x")
                    g_frame.bind("<Button-1>", lambda _, a=g_frame: self.foucsed_main(a))
                    g_frame.bind("<Button-3>", lambda _, a=g_frame: self.exit_main(a))
                    
                parent_button = tk.Button(g_frame, text=str(selected_node), bg=color, fg="white")
                parent_button.bind("<Button-3>", lambda _, a=parent_button: self.exit_childe(a))
                parent_button.grid(row=0, column=len(g_frame.winfo_children())+1)
        self.update_combobox_values()
        self.update_values()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Node Selector")
    seroot = tk.Frame(root, bg="white")
    seroot.pack(fill=tk.X)
    app = NodeSelectorApp(seroot, "a+a1+a11+a111;b+b1+b11+b111;", "[['Shop_name1',[['Item_code1',[['Item_color1',[['item_size1',[]]]]]],['Item_code12',[['Item_color21',[['item_size21',[]]]]]]]],['Shop_name2',[['Item_code2',[['Item_color2',[['item_size2',[]]]]]],['Item_code22',[['Item_color21',[['item_size21',[]]]]]]]")
    root.mainloop()
