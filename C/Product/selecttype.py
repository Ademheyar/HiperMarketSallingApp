import tkinter as tk
from tkinter import ttk


import random
import os
import atexit
import sys
import json
import ast

from C.List import *
import os

nodes = [["a"]]

nodes = "[['MANS', [['ACCESSORIES', []], ['TROUSER', []], ['SHOES', []], ['TOP', [['T-SHIRT', []], ['SHIRT', []], ['BLOUSES', []], ['POLO SHIRT', []], ['TANK', []], ['SWEATER', []], ['HOODIES', []], ['JACKET', []], ['BLAZER', []]]], ['BOTTOM', [['JEAN', []], ['PANT', []], ['SHORT', []], ['SKIRT', []], ['LEGGING', []], ['CULOTTE', []]]], ['OUTERWEAR', [['COAT', []], ['TRENCH COAT', []], ['RIN COAT', []], ['PARKA', []], ['WINDBREAKER', []]]], ['ACTIVEWEAR', [['ATHLETICSHORTS', []], ['JOGGINGPANT', []], ['SPORTJACKET', []], ['YOGAPANT', []], ['PREFORMANCETOP', []]]]]], ['WOMANS', [['ACCESSORIES', []], ['TROUSER', []], ['SHOES', []], ['TOP', [['T-SHIRT', []], ['SHIRT', []], ['BLOUSES', []], ['POLO SHIRT', []], ['TANK', []], ['SWEATER', []], ['HOODIES', []], ['JACKET', []], ['BLAZER', []]]], ['BOTTOM', [['JEAN', []], ['PANT', []], ['SHORT', []], ['SKIRT', []], ['LEGGING', []], ['CULOTTE', []]]], ['DRESS', [['SUNDRESS', []], ['COCKTAIL', []], ['MAXI', []], ['SHIFT', []], ['BODYCON', []], ['A-LINE', []]]], ['OUTERWEAR', [['COAT', []], ['TRENCH COAT', []], ['RIN COAT', []], ['PARKA', []], ['WINDBREAKER', []]]], ['ACTIVEWEAR', [['SPORTBRA', []], ['ATHLETICSHORTS', []], ['JOGGINGPANT', []], ['SPORTJACKET', []], ['YOGAPANT', []], ['PREFORMANCETOP', []]]]]], ['KIDS', [['ACCESSORIES', []], ['GIRLS', [['TROUSER', []], ['SHOES', []], ['TOP', [['T-SHIRT', []], ['SHIRT', []], ['BLOUSES', []], ['POLO SHIRT', []], ['TANK', []], ['SWEATER', []], ['HOODIES', []], ['JACKET', []], ['BLAZER', []]]], ['BOTTOM', [['JEAN', []], ['PANT', []], ['SHORT', []], ['SKIRT', []], ['LEGGING', []], ['CULOTTE', []]]], ['DRESS', [['SUNDRESS', []], ['COCKTAIL', []], ['MAXI', []], ['SHIFT', []], ['BODYCON', []], ['A-LINE', []]]], ['OUTERWEAR', [['COAT', []], ['TRENCH COAT', []], ['RIN COAT', []], ['PARKA', []], ['WINDBREAKER', []]]], ['ACTIVEWEAR', [['SPORTBRA', []], ['ATHLETICSHORTS', []], ['JOGGINGPANT', []], ['SPORTJACKET', []], ['YOGAPANT', []], ['PREFORMANCETOP', []]]]]], ['BOYS', [['TROUSER', []], ['SHOES', []], ['TOP', [['T-SHIRT', []], ['SHIRT', []], ['BLOUSES', []], ['POLO SHIRT', []], ['TANK', []], ['SWEATER', []], ['HOODIES', []], ['JACKET', []], ['BLAZER', []]]], ['BOTTOM', [['JEAN', []], ['PANT', []], ['SHORT', []], ['SKIRT', []], ['LEGGING', []], ['CULOTTE', []]]], ['OUTERWEAR', [['COAT', []], ['TRENCH COAT', []], ['RIN COAT', []], ['PARKA', []], ['WINDBREAKER', []]]], ['ACTIVEWEAR', [['ATHLETICSHORTS', []], ['JOGGINGPANT', []], ['SPORTJACKET', []], ['YOGAPANT', []], ['PREFORMANCETOP', []]]]]], ['FORKIDS', [['TROUSER', []], ['SHOES', []], ['TOP', [['T-SHIRT', []], ['SHIRT', []], ['BLOUSES', []], ['POLO SHIRT', []], ['TANK', []], ['SWEATER', []], ['HOODIES', []], ['JACKET', []], ['BLAZER', []]]], ['BOTTOM', [['JEAN', []], ['PANT', []], ['SHORT', []], ['SKIRT', []], ['LEGGING', []], ['CULOTTE', []]]], ['OUTERWEAR', [['COAT', []], ['TRENCH COAT', []], ['RIN COAT', []], ['PARKA', []], ['WINDBREAKER', []]]], ['ACTIVEWEAR', [['ATHLETICSHORTS', []], ['JOGGINGPANT', []], ['SPORTJACKET', []], ['YOGAPANT', []], ['PREFORMANCETOP', []]]]]]]], ['FOREVERYONE', [['ACCESSORIES', []], ['SHOES', []], ['TROUSER', []], ['TOP', [['T-SHIRT', []], ['SHIRT', []], ['BLOUSES', []], ['POLO SHIRT', []], ['TANK', []], ['SWEATER', []], ['BLAZER', []]]], ['BOTTOM', [['JEAN', []], ['PANT', []], ['SHORT', []], ['SKIRT', []], ['LEGGING', []], ['CULOTTE', []]]], ['OUTERWEAR', [['COAT', []], ['RIN COAT', []], ['PARKA', []], ['WINDBREAKER', []], ['TRENCHCOAT', []]]], ['ACTIVEWEAR', [['ATHLETICSHORTS', []], ['JOGGINGPANT', []], ['SPORTJACKET', []], ['YOGAPANT', []], ['PREFORMANCETOP', []]]]]]]"

from C.API.Get import *
from C.API.API import *
from C.API.Set import *

class NodeSelectorApp():
    def __init__(self, frame, user_info):
        self.root = frame
        
        self.node_combobox = ttk.Combobox(self.root, state="readonly")
        self.node_combobox.pack(fill=tk.X, pady=10)
        self.node_combobox.bind("<<ComboboxSelected>>", self.update_node_selection)
        sitting = None
        if not user_info or 'User_id' not in user_info:
            sitting = Get_Setting(user_info, ['User_id'], [user_info['User_id']])[0]
            if len(sitting) <= 0:
                Set_Setting(user_info, ["User_id", "barcode_count", "printer"], [user_info['User_id'], 0, ""])
                sitting = Get_Setting(user_info, ['User_id'], [user_info['User_id']])[0]
            sitting = sitting[0]
            print("sitting Types :"+ str(sitting[0]))
        if sitting and sitting[4] and sitting[4] != "":
            print("Users Types :"+ str(sitting[4]))
            self.nodes = load_list(sitting[4])
        else:
            print("Deff Types :" + str(nodes))
            self.nodes = load_list(nodes)

        #self.nodes = [['MANS', [['ACCESSORIES', []], ['TROUSER', []], ['SHOES', []], ['TOP', [['T-SHIRT', []], ['SHIRT', []], ['BLOUSES', []], ['POLO SHIRT', []], ['TANK', []], ['SWEATER', []], ['HOODIES', []], ['JACKET', []], ['BLAZER', []]]], ['BOTTOM', [['JEAN', []], ['PANT', []], ['SHORT', []], ['SKIRT', []], ['LEGGING', []], ['CULOTTE', []]]], ['OUTERWEAR', [['COAT', []], ['TRENCH COAT', []], ['RIN COAT', []], ['PARKA', []], ['WINDBREAKER', []]]], ['ACTIVEWEAR', [['ATHLETICSHORTS', []], ['JOGGINGPANT', []], ['SPORTJACKET', []], ['YOGAPANT', []], ['PREFORMANCETOP', []]]]]], ['WOMANS', [['ACCESSORIES', []], ['TROUSER', []], ['SHOES', []], ['TOP', [['T-SHIRT', []], ['SHIRT', []], ['BLOUSES', []], ['POLO SHIRT', []], ['TANK', []], ['SWEATER', []], ['HOODIES', []], ['JACKET', []], ['BLAZER', []]]], ['BOTTOM', [['JEAN', []], ['PANT', []], ['SHORT', []], ['SKIRT', []], ['LEGGING', []], ['CULOTTE', []]]], ['DRESS', [['SUNDRESS', []], ['COCKTAIL', []], ['MAXI', []], ['SHIFT', []], ['BODYCON', []], ['A-LINE', []]]], ['OUTERWEAR', [['COAT', []], ['TRENCH COAT', []], ['RIN COAT', []], ['PARKA', []], ['WINDBREAKER', []]]], ['ACTIVEWEAR', [['SPORTBRA', []], ['ATHLETICSHORTS', []], ['JOGGINGPANT', []], ['SPORTJACKET', []], ['YOGAPANT', []], ['PREFORMANCETOP', []]]]]], ['KIDS', [['ACCESSORIES', []], ['GIRLS', [['TROUSER', []], ['SHOES', []], ['TOP', [['T-SHIRT', []], ['SHIRT', []], ['BLOUSES', []], ['POLO SHIRT', []], ['TANK', []], ['SWEATER', []], ['HOODIES', []], ['JACKET', []], ['BLAZER', []]]], ['BOTTOM', [['JEAN', []], ['PANT', []], ['SHORT', []], ['SKIRT', []], ['LEGGING', []], ['CULOTTE', []]]], ['DRESS', [['SUNDRESS', []], ['COCKTAIL', []], ['MAXI', []], ['SHIFT', []], ['BODYCON', []], ['A-LINE', []]]], ['OUTERWEAR', [['COAT', []], ['TRENCH COAT', []], ['RIN COAT', []], ['PARKA', []], ['WINDBREAKER', []]]], ['ACTIVEWEAR', [['SPORTBRA', []], ['ATHLETICSHORTS', []], ['JOGGINGPANT', []], ['SPORTJACKET', []], ['YOGAPANT', []], ['PREFORMANCETOP', []]]]]], ['BOYS', [['TROUSER', []], ['SHOES', []], ['TOP', [['T-SHIRT', []], ['SHIRT', []], ['BLOUSES', []], ['POLO SHIRT', []], ['TANK', []], ['SWEATER', []], ['HOODIES', []], ['JACKET', []], ['BLAZER', []]]], ['BOTTOM', [['JEAN', []], ['PANT', []], ['SHORT', []], ['SKIRT', []], ['LEGGING', []], ['CULOTTE', []]]], ['OUTERWEAR', [['COAT', []], ['TRENCH COAT', []], ['RIN COAT', []], ['PARKA', []], ['WINDBREAKER', []]]], ['ACTIVEWEAR', [['ATHLETICSHORTS', []], ['JOGGINGPANT', []], ['SPORTJACKET', []], ['YOGAPANT', []], ['PREFORMANCETOP', []]]]]], ['FORKIDS', [['TROUSER', []], ['SHOES', []], ['TOP', [['T-SHIRT', []], ['SHIRT', []], ['BLOUSES', []], ['POLO SHIRT', []], ['TANK', []], ['SWEATER', []], ['HOODIES', []], ['JACKET', []], ['BLAZER', []]]], ['BOTTOM', [['JEAN', []], ['PANT', []], ['SHORT', []], ['SKIRT', []], ['LEGGING', []], ['CULOTTE', []]]], ['OUTERWEAR', [['COAT', []], ['TRENCH COAT', []], ['RIN COAT', []], ['PARKA', []], ['WINDBREAKER', []]]], ['ACTIVEWEAR', [['ATHLETICSHORTS', []], ['JOGGINGPANT', []], ['SPORTJACKET', []], ['YOGAPANT', []], ['PREFORMANCETOP', []]]]]]]], ['FOREVERYONE', [['ACCESSORIES', []], ['SHOES', []], ['TROUSER', []], ['TOP', [['T-SHIRT', []], ['SHIRT', []], ['BLOUSES', []], ['POLO SHIRT', []], ['TANK', []], ['SWEATER', []], ['BLAZER', []]]], ['BOTTOM', [['JEAN', []], ['PANT', []], ['SHORT', []], ['SKIRT', []], ['LEGGING', []], ['CULOTTE', []]]], ['OUTERWEAR', [['COAT', []], ['RIN COAT', []], ['PARKA', []], ['WINDBREAKER', []], ['TRENCHCOAT', []]]], ['ACTIVEWEAR', [['ATHLETICSHORTS', []], ['JOGGINGPANT', []], ['SPORTJACKET', []], ['YOGAPANT', []], ['PREFORMANCETOP', []]]]]]]
        
        self.get_value = None
        self.selected_nodes = []
        
        self.node_hierarchy = None
        self.listed_nodes_parents = []

        # Create main frame to display selected nodes and parents
        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.pack(fill=tk.X)

        self.focused_group = 0
        
    def update_combobox_values(self):
        #print("ss "+ str([";"] + [name[0] for name in self.node_hierarchy]))
        self.node_combobox["values"] = [";"] + [name[0] for name in self.node_hierarchy]

    def update_list(self):
        # Clear previous widgets in the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.selected_nodes = []
        for i2, lists in enumerate(self.get_value):
            if not lists:
                continue
            fcolor = None
            if self.focused_group == i2:
                fcolor = "blue"
            g_frame = tk.Frame(self.main_frame, bg=fcolor)
            g_frame.pack(fill="x")
            g_frame.bind("<Button-1>", lambda _, a=g_frame: self.foucsed_main(a))
            g_frame.bind("<Button-3>", lambda _, a=g_frame: self.exit_main(a))
            g_ = []
            for i3, value in enumerate(lists):
                if value == '':
                    continue
                print("i3 " + str(i3))
                color = "white"
                if self.isthere(i3, value):
                    color = "Green"
                elif not self.isthere(-1, value):
                    color = "orange"
                else:
                    color = "white"
                g_.append(self.get_index(i3, value))
                #todo make def color giving
                parent_button = tk.Button(g_frame, text=str(value), bg=color, fg="white")
                parent_button.bind("<Button-3>", lambda _, a=parent_button: self.exit_childe(a))
                parent_button.grid(row=0, column=len(g_frame.winfo_children())+1)
            if len(g_) > 0:
                self.selected_nodes.append(g_)
                #print("parantes : " + str(g_))
                 
    def load(self, def_value):
        get_nodes = self.nodes
        #txt = json.dumps(self.nested_list)
        if def_value == "":
            def_value = "[]"
        self.get_value = json.loads(def_value)
        self.selected_nodes = []
        
        self.node_hierarchy = get_nodes
        self.listed_nodes_parents = []

        self.focused_group = 0

        self.update_combobox_values()
        self.update_list()
        
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
            #print("chacking value " + str(value) + "on list " + str(i))
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
            
       
    def update_values(self):
        main_value = []
        for j, widget in enumerate(self.main_frame.winfo_children()):
            new_v = []
            for widget_c in widget.winfo_children():
                new_v.append(widget_c.cget('text'))
            main_value.append(new_v)
                
        self.get_value = main_value
        print("self.get_value = ", self.get_value)
        self.update_list()
            
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

'''if __name__ == "__main__":
    root = tk.Tk()
    root.title("Node Selector")
    seroot = tk.Frame(root, bg="white")
    seroot.pack(fill=tk.X)
    app = NodeSelectorApp(seroot, "a+a1+a11+a111;b+b1+b11+b111;")
    root.mainloop()'''
