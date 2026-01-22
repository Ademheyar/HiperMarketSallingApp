import tkinter as tk
from tkinter import ttk
import sqlite3
import shutil
import datetime
import os
import atexit
import sys
import random

current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(current_dir, '..')
sys.path.append(MAIN_dir)
from D.Getdate import GetDateForm

import os

def create_random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return f'#{r:02x}{g:02x}{b:02x}'

# self.chart_canvas_Frame : give main fram to display
# self.graph_value0 : give value to compare
#  : tall wiche value to use
#  : give style of chart 1: streag line 2: circle 3: line 
def draw_cart(parent, main_values, deff_which, deff_style):
    for items in parent.winfo_children():
        items.destroy()
    parent_fram = tk.Frame(parent)
    parent_fram.pack(fill=tk.BOTH, expand=1)
    
    chart_canvas_Frame = tk.Frame(parent_fram)
    chart_canvas_Frame.pack(side=tk.TOP, fill=tk.X)
    chart_canvas = tk.Canvas(chart_canvas_Frame)
    chart_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    xscrollbar = tk.Scrollbar(chart_canvas.master, orient='horizontal', command=chart_canvas.xview)
    xscrollbar.pack(fill=tk.X)
        
    chart_canvas.configure(xscrollcommand=xscrollbar.set)
    #self.New_item_contener_canvas.bind('<Configure>', lambda e: self.New_item_contener_canvas.configure(scrollregion=self.New_item_contener_canvas.bbox("all")))

    #self.item_List_frame = tk.Frame(self.item_List_canvas)
    #self.item_List_canvas.create_window((0, 0), window=self.item_List_frame, anchor=tk.NW)
    chart_canvas.bind('<Configure>', lambda e: chart_canvas.configure(scrollregion=chart_canvas.bbox("all")))

    
    def on_style_selected(canvas, style_var, which_var):
        canvas.delete("all")
        canvas.configure(scrollregion=canvas.bbox("all"))
        style = int(style_var.get())
        print("main_values ", main_values)
        _values = []
        if main_values:
            _values = main_values[0]
        print("_values ", _values)
        mv_index = int(which_var.get())
        if not mv_index < len(_values):
            mv_index = 1
        print("mv_index ", mv_index)
        
        values = [main_value[mv_index] for main_value in _values]
        print("values ", values)
        total_sum = sum(values)
        print("total_sum ", total_sum)
        max_value = 0
        if values:
            max_value = max(values)
        color = [create_random_color() for _ in values]
        
        if style == 1:
            bar_width = 20
            gap = 10
            total_width = len(values) * (bar_width + gap)
            x_offset = (bar_width + gap)
            for i, value in enumerate(_values):
                x_offset += (bar_width + gap)
                print("value ", value)
                x0 = x_offset + (i * (bar_width + gap))
                y0 = int(canvas.cget('height')) - 20
                scaled_value = values[i] * (int(canvas.cget('height'))-40) /max_value
                x1 = x_offset + (i + 1) * bar_width + (i * gap) - (bar_width + gap)
                y1 = int(canvas.cget('height')) - scaled_value - 20
                txt_angle = 90
                if int(canvas.cget('height'))-40 == scaled_value or (int(canvas.cget('height'))+((y1/10)+len(str(value[1]))))-40 >= scaled_value:
                    txt_angle = 0
                
                canvas.create_text((x0 + x1) / 2, y1 - ((y1/10)+len(str(value[1]))), text=str(value[1]), anchor="center", angle=txt_angle)
                canvas.create_text((x0 + x1) / 2, y0 + 10, text=str(value[1]), anchor="center")
                canvas.create_rectangle(x0, y0, x1, y1, fill=color[i])            
        elif style == 2:
            
            bar_width = 20
            gap = 10
            start_angle = 0
            for i, value in enumerate(_values):
                angle = 360 * values[i] / total_sum
                print("values[i] ", values[i])
                print("start_angle ", start_angle)
                print("angle ", angle)

                canvas.create_arc(50, 50, 250, 250, start=start_angle, extent=angle-0.1, fill=color[i])

                start_angle += angle

                canvas.create_rectangle(260, 50+i*20, 280, 70 + i *20, fill=color[i])
                canvas.create_text(285, 60 + i * 20, text=str(value[1])+" : " + str(value[1]), anchor="center")
                
        elif style == 3:
            bar_width = 20
            gap = 10
            total_width = len(_values) * (bar_width + gap)
            x_offset = (bar_width + gap)
            offset = (int(canvas.cget('width')) - total_width)
            scroll_by = x_offset+(offset/(len(values)-1))
            
            for i, value in enumerate(_values):
                v_index0 = v_index if v_index <= len(value)-1 else 1
                x_offset += (bar_width + gap)
                x0 = x_offset + (i * (bar_width + gap))
                y0 = int(canvas.cget('height')) - 20

                scaled_value = value[1] * (int(canvas.cget('height'))-40) /max_value
                
                x1 = x_offset + (i + 1) * bar_width + (i * gap) - (bar_width + gap)
                y1 = int(canvas.cget('height')) - scaled_value - 20
                txt_angle = 90
                if int(canvas.cget('height'))-40 == scaled_value or (int(canvas.cget('height'))+((y1/10)+len(str(value[1]))))-40 >= scaled_value:
                    txt_angle = 0
                
                canvas.create_text((x0 + x1) / 2, y1 - ((y1/10)+len(str(value[1]))), text=str(value[1]), anchor="center", angle=txt_angle)
                canvas.create_text((x0 + x1) / 2, y0 + 10, text=str(value[1]), anchor="center")
                canvas.create_line(x0, y0, x1, y1, fill=color[i])
        elif style == 4:
            bar_width = 20
            gap = 30
            total_width = len(values)
            x_offset = 30
            offset = (int(canvas.cget('width')) - total_width)
            scroll_by = x_offset+(offset/(len(values)-1))
            for i, value in enumerate(values):
                v_index0 = v_index if v_index <= len(value)-1 else 1
                x_offset += (gap)
                x0 = x_offset + (i)
                y0 = int(canvas.cget('height')) - 20

                scaled_value = value[1] * (int(canvas.cget('height'))-40) /max_value
                x1 = x_offset + (i + 1) * + (i)
                y1 = int(canvas.cget('height')) - scaled_value - 20

                j =i
                if i+1 < len(values):
                    j = i+1
                scaled_value2 = values[j][v_index0] * (int(canvas.cget('height'))-40) /max_value
                x2 = x_offset + gap + (j + 1) * j
                y2 = int(canvas.cget('height')) - scaled_value2 - 20
                txt_angle = 90
                if int(canvas.cget('height'))-40 == scaled_value or (int(canvas.cget('height'))+((y1/10)+len(str(value[1]))))-40 >= scaled_value:
                    txt_angle = 0
                
                canvas.create_text((x0 + x1) / 2, y1 - ((y1/10)+len(str(value[1]))), text=str(value[1]), anchor="center", angle=txt_angle)
                canvas.create_text((x0 + x1) / 2, y0 + 10, text=str(value[0]), anchor="center")
                canvas.create_line(x1, y1, x2, y2, fill=color[i], width=2) # color "blue"

    
    style_var = tk.StringVar()
    style_var.set(deff_style)

    which_var = tk.StringVar()
    which_var.set(deff_which)
    
    which_var.trace("w", lambda *arg, c=chart_canvas, s=style_var, w=which_var: on_style_selected(chart_canvas, s, w))
    which_dropdown = tk.OptionMenu(parent_fram, which_var, "1", "2", "3")
    which_dropdown.pack(side=tk.LEFT)
        
    style_var.trace("w", lambda *arg, c=chart_canvas, s=style_var, w=which_var: on_style_selected(chart_canvas, s, w))
    style_dropdown = tk.OptionMenu(parent_fram, style_var, "1", "2", "3", "4")
    style_dropdown.pack(side=tk.RIGHT)
    
    on_style_selected(chart_canvas, style_var, which_var)
        
def make_list(node_names):
    rr_dict = {}

    r_list = []
    r_dict = {}
    def set_value(vlist, vname, v):
        for vl in vlist:
            if vl[0] == vname:
                vl[1] += v
                vl[2] += 1
                return vl[1]
        return None
    def sub_list(on, read_on, key):
        if not read_on[on]:
            return None
        if isinstance(read_on[on], float):
            return read_on[on]
        elif isinstance(read_on[on], str):
            if on+1 == len(read_on):
                return None
            else:
                r = sub_list(on+1, read_on, key + "~" + str(read_on[on]))
                if r and isinstance(r, float):
                    if on not in rr_dict:
                        rr_dict[on] = [[key + "~" + str(read_on[on]), r, 1]]
                    else:
                        vr = set_value(rr_dict[on], key + "~" + str(read_on[on]), r)
                        if vr == None:
                            rr_dict[on].append([key + "~" + str(read_on[on]), r, 1])
                            
                    return r
                
    for q, n_n in enumerate(node_names):

        r = sub_list(1, n_n, str(n_n[0]))
        if r and isinstance(r, float):
            if 0 not in rr_dict:
                rr_dict[0] = [[n_n[0], r, 1]]
            else:
                #TODO chack on list if there is same key as this one 
                rr_dict[0].append([n_n[0], r, 1])
                #TODO after chacking the list get the total value

    title = ""
    print("rr_dict :" + str(rr_dict))
    return rr_dict, rr_dict, title

def make_list0(node_names):


    r_list = []
    r_dict = {}
    for q, n_n in enumerate(node_names):
        sub_dict = {}
        cu = sub_dict
        f = None
        for r, sub_n_n in enumerate(n_n):
            if f == None:
                #print("f = " + str(sub_n_n))
                f = sub_n_n
                continue
            if not isinstance(sub_n_n, float) and (str(sub_n_n) not in cu or not isinstance(cu[str(sub_n_n)], dict)):
                #print("subn = " + str(sub_n_n))
                if r+1 != len(n_n) and isinstance(n_n[r+1], float):
                    cu[str(sub_n_n)] = float(n_n[r+1])
                else:
                    cu[str(sub_n_n)] = {}
                cu = cu[str(sub_n_n)]
                
            else:
                #print("sub value = " + str(sub_n_n))
                w = 0
                #print("sub value cu = " + str(cu))
                if isinstance(cu, float):
                    w = float(cu)
                cu = w + float(sub_n_n)
                #print("sub value cu = " + str(cu))
        if q+1 != len(node_names) and isinstance(node_names[q+1], float):
            r_dict[str(f)] = float(node_names[q+1])
        else:
            if sub_dict == {} and cu != {}:
                r_dict[str(f)] = cu
            else:
                r_dict[str(f)] = sub_dict
            
    title = ""
    print("r_dict :" + str(r_dict))
    def sub_list(read_on, key, isfirst):
        if not isinstance(read_on, dict):
            if isfirst:
                if isinstance(read_on, float):
                    r_list.append([key, read_on, 1])
            else:
                return read_on
        elif len(read_on) > 1:
            v = 0
            count = 0
            for m in list(enumerate(read_on)):
                r = sub_list(read_on[m[1]], m[1], 1) if key in [m[1], ""] else sub_list(read_on[m[1]], m[1], 0)
                if r:
                    v += r
                    count += 1
            if v:
                r_list.append([key, r, count])
        else:
            k = str(list(enumerate(read_on))[0][1])
            r = sub_list(read_on[k], k, 0)
            if r:
                r_list.append([key, r, 1])
    sub_list(r_dict, "", 1)
    print("r_list :" + str(r_list))
    return r_dict, r_list, title
