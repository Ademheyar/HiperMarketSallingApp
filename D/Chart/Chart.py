import tkinter as tk
from tkinter import ttk
import sqlite3
import shutil
import datetime
import os
import atexit
import sys
import random, math

current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(current_dir, '..')
sys.path.append(MAIN_dir)
from D.Getdate import GetDateForm

import os

from collections import defaultdict

def create_random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return f'#{r:02x}{g:02x}{b:02x}'

def get_with_date(main_values):
    _yearly = []
    _monthly = []
    _weekly = []
    _daily = []
    _hourly = []
    _half_hour= []
    
    for data in main_values:
        # parse function
        def parse_date(s):
            s = s.strip()
            # try multiple formats
            for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H", "%Y-%m-%d"):
                
                try:
                    #print("fmt ", fmt)
                    #print("s ", s)
                    
                    return datetime.datetime.strptime(s, fmt)
                except:
                    pass
            return None
        #print("chaking dates list ", data)
        yearly = defaultdict(float)
        monthly = defaultdict(float)
        weekly = defaultdict(float)
        daily = defaultdict(float)
        hourly = defaultdict(float)
        half_hour = defaultdict(float)

        for row in data:
            if len(row)!= 2:
                continue
            date_str, value = row
            dt = parse_date(str(date_str))
            #print("chaking dt", str(dt))
            if not dt:
                continue
            #print("chaking row", row)

            val = float(value)

            # Keys
            yearly[dt.year] += val
            #print("chaking dates year")

            month_key = dt.strftime("%b %y") # March 2026
            monthly[month_key] += val
            #print("chaking dates month_key")

            day_key = dt.strftime("%d %b %y") # 22 March 26
            daily[day_key] += val
            #print("chaking dates day_key")

            # Week: Monday to Sunday
            week_key = f"Week {dt.isocalendar()[1]} - {dt.strftime('%b %y')}"
            weekly[week_key] += val
            #print("chaking dates week_key")

            hour_key = dt.strftime("%Y-%b-%d %H:00")
            hourly[hour_key] += val
            print("chaking dates hour_key")

            # 30 min bucket: 10:00 or 10:30
            minute = 0 if dt.minute < 30 else 30
            half_key = dt.strftime(f"%Y-%b-%d %H:{minute:02d}")
            half_hour[half_key] += val
            #print("chaking dates half_key")

        # Convert to your required list format [[title, sum],...] sorted

        def to_sorted_list(d, sort_by_date=False):
            # sort by key
            return sorted([[k, v] for k, v in d.items()], key=lambda x: x[0])
        _yearly.append(sorted([[k, v] for k, v in yearly.items()]))
        _monthly.append(to_sorted_list(monthly))
        _weekly.append(to_sorted_list(weekly))
        _daily.append(to_sorted_list(daily))
        _hourly.append(to_sorted_list(hourly))
        _half_hour.append(to_sorted_list(half_hour))
            
    return _yearly, _monthly, _weekly, _daily, _hourly, _half_hour


    '''# --- TEST WITH YOUR DATA ---
    data = [
        ["2026-04-22 10:00", 50],
        ["2026-04-22 10:30", 70],
        ["2026-04-22 11:00", 10],
        ["2026-04-23 10:00", 30],
        ["2026-05-22 10:30", 70],
        ["2027-07-22 10:00", 60],
    ]

    out = group_datetime_values(data)

    print("Yearly =", out["Yearly"])
    # [[2026, 230.0], [2027, 60.0]]

    print("\nMonthly =", out["Monthly"])
    # [['April 2026', 160.0], ['July 2027', 60.0], ['May 2026', 70.0]]

    print("\nDaily =", out["Daily"])
    # [['22 April 26', 130.0], ['23 April 26', 30.0],...]

    print("\n30 Mints =", out["30 Mints"])'''
    
# self.chart_canvas_Frame : give main fram to display
# self.graph_value0 : give value to compare
#  : tall wiche value to use
#  : give style of chart 1: streag line 2: circle 3: line 
def draw_cart(parent, tools_styel, main_values, deff_which, deff_style):
    for items in parent.winfo_children():
        items.destroy()
    parent_fram = tk.Frame(parent, bg=tools_styel['Main_Frame_color'])
    parent_fram.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    mainu_frame = tk.Frame(parent_fram, bg=tools_styel['Main_Frame_color'])
    mainu_frame.pack(side=tk.TOP, fill=tk.X, expand=1)

    
    yearly, monthly, weekly, daily, hour, haf_hour = get_with_date(main_values)
    bydate = [""]
    if haf_hour:
        bydate.append("By 30 Min")
        deff_which = "By 30 Min"
    if hour:
        bydate.append("By hour")
        deff_which = "By hour"
    if daily:
        bydate.append("By daily")
        deff_which = "By daily"
    if weekly:
        bydate.append("By weekly")
        deff_which = "By weekly"
    if monthly:
        bydate.append("By monthly")
        deff_which = "By monthly"
    if yearly:
        bydate.append("By year")
        deff_which = "By year"
        
    which_var = tk.StringVar()
    
    Connectby_Line_change_var = tk.IntVar()
    Connectby_Line_change_Checkbutton = tk.Checkbutton(mainu_frame, text='Connect By Line', variable=Connectby_Line_change_var)
    Connectby_Line_change_Checkbutton.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    Connectby_Line_change_var.set(1)

    Show_Line_change_var = tk.IntVar()
    Show_Line_change_Checkbutton = tk.Checkbutton(mainu_frame, text='Show Line', variable=Show_Line_change_var)
    Show_Line_change_Checkbutton.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
    Show_Line_change_var.set(1)

    Show_list_var = tk.IntVar()
    Show_list_Checkbutton = tk.Checkbutton(mainu_frame, text='Show List', variable=Show_list_var)
    Show_list_Checkbutton.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
    Show_list_var.set(0)
    
    style_var = tk.StringVar()
    style_var.set(deff_style)
    style_dropdown = tk.OptionMenu(mainu_frame, style_var, "Bar Chart", "Scatter Plot Chart", "Pie Chart", "Line Chart")
    style_dropdown.grid(row=1, column=0, sticky=tk.W)
    
    which_var.set(bydate[0])
    which_dropdown = tk.OptionMenu(mainu_frame, which_var, *bydate)
    which_dropdown.grid(row=1, column=1, sticky=tk.W)
    
    
    text_style_var = tk.StringVar()
    text_style_var.set("Bottom")
    text_style_dropdown = tk.OptionMenu(mainu_frame, text_style_var,  "Top Of The Ege", "In Middle", "Oposite", "Bottom")
    text_style_dropdown.grid(row=1, column=2, sticky=tk.W)
    
    chart_canvas_Frame = tk.Frame(parent_fram, bg=tools_styel['Main_Frame_color'])
    chart_canvas_Frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    chart_canvas = tk.Canvas(chart_canvas_Frame, bg=tools_styel['Main_Frame_color'])
    chart_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    xscrollbar = tk.Scrollbar(chart_canvas_Frame.master, orient='horizontal', command=chart_canvas.xview)
    xscrollbar.pack(side=tk.TOP, fill=tk.X)
    yscrollbar = tk.Scrollbar(chart_canvas_Frame, orient='vertical', command=chart_canvas.yview)
    yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    chart_canvas.configure(xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
    chart_canvas.bind('<Configure>', lambda e: chart_canvas.configure(scrollregion=chart_canvas.bbox("all")))
    
    list_fram = tk.Frame(parent, bg=tools_styel['Main_Frame_color'])
    list_fram.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    product_list = tk.Listbox(list_fram, selectmode=tk.SINGLE, width=30, bg=tools_styel['Main_Frame_color'], fg=tools_styel['Text_color'], font=("Arial", 10)) # , highlightbackground=accent_green)

    def on_style_selected(canvas, style_var, which_var, Connectbyline, Show_Line_var, text_style_var):
        canvas.delete("all")
        _values = []
        if which_var.get() == "By year":
            main_values0 = yearly
            #print("yearly ", yearly)
        elif which_var.get() == "By monthly":
            main_values0 = monthly
            #print("monthly ", monthly)
        elif which_var.get() == "By weekly":
            main_values0 = weekly
            #print("weekly ", weekly)
        elif which_var.get() == "By daily":
            main_values0 = daily
            #print("daily ", daily)
        elif which_var.get() == "By hour":
            main_values0 = hour
            #print("hour ", hour)
        elif which_var.get() == "By 30 Min":
            main_values0 = haf_hour
            #print("haf_hour ", haf_hour)
        else:
            main_values0 = main_values
            #print("main_values ", main_values)
            
        if main_values :
            _values = main_values0[0]
        if not _values or len(_values)== 0:
            return
        style = style_var.get()
        #print("_values ", _values)
        v_index = 1

        values = [main_value[1] for main_value in _values] # get only choosen value only
        #print("values ", values)
        
        
        
        max_value = 0
        if values:
            max_value = max(values)
        # geting max value to sent the top and the low

        product_list.delete(0, tk.END)
        if Show_list_var.get() == 1:
            product_list.grid(row=0, column=0, rowspan=4, sticky="nsew", padx=5, pady=5)
            for product in _values:
                product_list.insert(tk.END, f"{product[0]}  {product[1]}")
        else:
            product_list.grid_forget()

        color = [create_random_color() for _ in values]
        # generating rondom color for each values
        x_offset = 0 # space to start the value draw
        y_offset = 0 # space to star4t drow texts
        y_gap = 50
        x_gap = 50
        max_y = max(sorted(values))
        min_y = min(sorted(values))
        bar_width = 20 # bar body aria size
            
        if  Show_Line_var.get() == 1 and (style == "Scatter Plot Chart" or style == "Bar Chart" or style == "Line Chart"):
            # first Leftside show and bottom informations
            x_offset = 40 # space to start the value draw
            y_offset = 50 # space to star4t drow texts

            y_gap = 20
            count = 20
            gap = (max_y-min_y) / (count-1)
            result = []
            for i in range(count):
                value = min_y + (i*gap)
                result.append(round(value, 1))
            q = 0
            for i, val in enumerate(_values):

                y = (int(canvas.cget('height')) - y_offset/2) - (i*y_gap)

                if q < len(result):
                    scaled_value = result[q] * (int(canvas.cget('height'))-y_offset) /max_value
                    txt_angle = 90
                    if int(canvas.cget('height'))-y_offset == scaled_value or (int(canvas.cget('height'))+((y/10)+len(str(result[q]))))-y_offset >= scaled_value:
                        txt_angle = 0
                    canvas.create_text(0+15, y - (len(str(result[q]))+1), text=str(result[q]), anchor="center", angle=txt_angle, fill=tools_styel['Text_color'])
                
                canvas.create_line(x_offset, y, x_offset + (len(_values)-1) *((bar_width+5))+bar_width, y, fill="black") # X-axis
                
                canvas.create_line(x_offset+(i*(bar_width+5))+bar_width, int(canvas.cget('height'))-y_offset/2, x_offset+(i*(bar_width+5))+bar_width, 0, fill="black") # Y_asiss
                
                q+=1
                
            # X and Y line to Sparate the text and y value from the drawing graph
            canvas.create_line(x_offset, 0, x_offset, int(canvas.cget('height')), fill="black")
            canvas.create_line(0, int(canvas.cget('height'))-y_offset/2, int(canvas.cget('width')), int(canvas.cget('height'))-y_offset/2, fill="black")
            
        if style == "Scatter Plot Chart": # Dot style chart if it is choosen one
            total_width = len(values) * (bar_width + x_gap)
            offset = (int(canvas.cget('width')) - total_width) # use this if dont what to use scroing bar 
            
            W, H = int(canvas.cget('width')), int(canvas.cget('height'))
            padding = 50
            range_y = max_y - min_y if max_y != min_y else 1
            zero_y = H-y_offset/2 - ((-min_y) / range_y * (H-y_offset*2))
            
            point = []
                
                
            for i, val in enumerate(_values):
                x = x_offset + i *(bar_width+5)
                scaled_value = values[i] * (int(canvas.cget('height'))-y_offset) /max_value
                y = int(canvas.cget('height')) - scaled_value -  (y_offset/2 )

                point.append((x,y-y_gap))

                canvas.create_oval(x-3, y-y_gap-3, x+3, y-y_gap+3, fill=color[i])

                txt_angle = 90
                if int(canvas.cget('height'))-y_offset == scaled_value or (int(canvas.cget('height'))+((int(canvas.cget('height')) - y_offset/10)+len(str(val[1]))))-y_offset >= scaled_value:
                    txt_angle = 0
                    text_style_var

                #"In Middle", "A side"
                if i % 3 == 0 and text_style_var.get() == "Oposite" or i % 2 == 0 and text_style_var.get() == "Oposite" or text_style_var.get() == "Top Of The Ege"  or text_style_var.get() ==  "In Middle":
                    canvas.create_text(x + bar_width//2, y-(y_gap+10), text=str(val[1]), anchor="center", angle=txt_angle, fill=tools_styel['Text_color'])

                canvas.create_text(x + bar_width//2, int(canvas.cget('height')) - y_offset/2 + 15, text=str(val[0]), anchor="center", angle=txt_angle, fill=tools_styel['Text_color'])

                point.append((x + bar_width//2, y))

            # if piont is allowd to draw
            if Connectbyline.get() == 1:
                for j in range(len(point)-1):
                    canvas.create_line(point[j], point[j+1], fill="black", width=2)
                    
        elif style == "Bar Chart": # ragtangel style chart if it is choosen one
            
            total_width = len(values) * (bar_width + x_gap)
            offset = (int(canvas.cget('width')) - total_width) # use this if dont what to use scroing bar 
            point = []
                
            for i, val in enumerate(_values):
                x = x_offset + i *(bar_width+5)
                scaled_value = values[i] * (int(canvas.cget('height'))-y_offset) /max_value
                y = int(canvas.cget('height')) - scaled_value -  (y_offset/2 )

                


                txt_angle = 90
                if int(canvas.cget('height'))-y_offset == scaled_value or (int(canvas.cget('height'))+((int(canvas.cget('height')) - y_offset/10)+len(str(val[1]))))-y_offset >= scaled_value:
                    txt_angle = 0

                canvas.create_rectangle(x, y-y_gap, x+bar_width, int(canvas.cget('height')) - y_offset/2, fill=color[i])
                barhight = (int(canvas.cget('height')) - y_offset/2) - (y-y_gap)
                
                if i % 3 == 0 and text_style_var.get() == "Oposite" or text_style_var.get() == "Bottom" or \
                    i % 2 == 0 and text_style_var.get() == "Oposite" or text_style_var.get() == "Top Of The Ege":
                    canvas.create_text(x + bar_width//2, y-(y_gap+10), text=str(val[1]), anchor="center", angle=txt_angle, fill=tools_styel['Text_color'])

                canvas.create_text(x + bar_width//2, int(canvas.cget('height')) - y_offset/2 + 15, text=str(val[0]), anchor="center", angle=txt_angle, fill=tools_styel['Text_color'])
                    
                if text_style_var.get() == "In Middle":
                    canvas.create_text(x + bar_width/2, y+7+barhight if not y+7+barhight >= int(canvas.cget('height')) - y_offset/2 else y-7, text=str(val[1]), anchor="center", angle=90, fill=tools_styel['Text_color'])

                point.append((x + bar_width//2, y))

            # if piont is allowd to draw
            if Connectbyline.get() == 1:
                for j in range(len(point)-1):
                    canvas.create_line(point[j], point[j+1], fill="black", width=2)
                
        elif style == "Pie Chart":
            total_sum = sum(values) # it is getting Total of all values
            #print("total_sum ", total_sum)
            bar_width = 20
            gap = 40
            start_angle = 0
            for i, value in enumerate(_values):
                scaled_value = values[i] * (int(canvas.cget('height'))-y_offset) /max_value
                angle = (values[i] / max_value) * 360 
                x=int(canvas.cget('height'))/2
                y = int(canvas.cget('height'))/2
                radiuse = x/2  
                #angle = 360 * values[i] / total_sum
                #print("values[i] ", values[i])
                #print("start_angle ", start_angle)
                #print("angle ", angle)

                def get_xy(cx, cy, r, angle_deg):
                    rad = math.radians(angle_deg)
                    x99 = cx + r*math.cos(rad)
                    y99 = cy + r*math.sin(rad)
                    return x99 , y99
                mid_angle = start_angle + angle / 2
                x1, y1 = get_xy(x, y, radiuse, mid_angle)
                x2, y2 = get_xy(x, y, radiuse+25, mid_angle)
                x3, y3 = get_xy(x, y, radiuse+50, mid_angle)
                
                if text_style_var.get() == "Oposite" or text_style_var.get() == "Top Of The Ege":
                    if Connectbyline.get() == 1:
                        canvas.create_line(x1, y1, x2, y2, x3, y3, fill=color[i], width=1, smooth=True)
                    canvas.create_oval(x1-3, y1-3, x1+3, y1+3, fill=color[i])
                    anchor = tk.W if x3 > x else tk.E
                    canvas.create_text(x3, y3, text=str(value[1]), anchor=anchor, fill=tools_styel['Text_color'])

                if text_style_var.get() == "Oposite" or text_style_var.get() == "Bottom":
                    if gap == 40:
                        gap0 = 20
                    else:
                        gap0 = 40
                    canvas.create_rectangle(i*20, int(canvas.cget('height'))-gap-5, i*20+20, int(canvas.cget('height'))-gap-22, fill=color[i])
                    
                    canvas.create_text(i*20, int(canvas.cget('height'))-gap0, text=str(value[1]), anchor="center", fill=tools_styel['Text_color'])
                    if gap == 40:
                        gap = 20
                    else:
                        gap = 40
                    
                if text_style_var.get() == "In Middle":
                    anchor = tk.W if x1 > x else tk.E
                    canvas.create_text(x1, y1, text=str(value[1]), anchor=anchor, fill=tools_styel['Text_color'])
                
                
                if start_angle <= 360:
                    canvas.create_arc(x-radiuse, y-radiuse, x+radiuse, y+radiuse, start=start_angle, extent=angle-0.1, fill=color[i])
                
                start_angle += angle
                
                
                
                
        elif style == "Line Chart":
            bar_width = 20
            gap = 30
            total_width = len(values)
            x_offset = 30
            offset = (int(canvas.cget('width')) - total_width)
            scroll_by = x_offset+(offset/(len(values)-1))
            for i, value in enumerate(_values):
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
                scaled_value2 = _values[j][v_index0] * (int(canvas.cget('height'))-40) /max_value
                x2 = x_offset + gap + (j + 1) * j
                y2 = int(canvas.cget('height')) - scaled_value2 - 20
                txt_angle = 90
                if int(canvas.cget('height'))-40 == scaled_value or (int(canvas.cget('height'))+((y1/10)+len(str(value[1]))))-40 >= scaled_value:
                    txt_angle = 0
                
                canvas.create_text((x0 + x1) / 2, y1 - ((y1/10)+len(str(value[1]))), text=str(value[0]), anchor="center", angle=txt_angle, fill=tools_styel['Text_color'])
                canvas.create_text((x0 + x1) / 2, y0 + 10, text=str(value[0]), anchor="center", fill=tools_styel['Text_color'])
                canvas.create_line(x1, y1, x2, y2, fill=color[i], width=2) # color "blue"
        canvas.configure(scrollregion=canvas.bbox("all"))

    
    which_var.trace("w", lambda *arg, c=chart_canvas, s=style_var, w=which_var, e=Connectby_Line_change_var, r=Show_Line_change_var, t=text_style_var: on_style_selected(chart_canvas, s, w, e, r, t))
    text_style_var.trace("w", lambda *arg, c=chart_canvas, s=style_var, w=which_var, e=Connectby_Line_change_var, r=Show_Line_change_var, t=text_style_var: on_style_selected(chart_canvas, s, w, e, r, t))
    Connectby_Line_change_var.trace("w", lambda *arg, c=chart_canvas, s=style_var, w=which_var, e=Connectby_Line_change_var, r=Show_Line_change_var, t=text_style_var: on_style_selected(chart_canvas, s, w, e, r, t))
    Show_list_var.trace("w", lambda *arg, c=chart_canvas, s=style_var, w=which_var, e=Connectby_Line_change_var, r=Show_Line_change_var, t=text_style_var: on_style_selected(chart_canvas, s, w, e, r, t))
    Show_Line_change_var.trace("w", lambda *arg, c=chart_canvas, s=style_var, w=which_var, e=Connectby_Line_change_var, r=Show_Line_change_var, t=text_style_var: on_style_selected(chart_canvas, s, w, e, r, t))
    style_var.trace("w", lambda *arg, c=chart_canvas, s=style_var, w=which_var, e=Connectby_Line_change_var, r=Show_Line_change_var, t=text_style_var: on_style_selected(chart_canvas, s, w, e, r, t))
    
    
    on_style_selected(chart_canvas, style_var, which_var, Connectby_Line_change_var, Show_Line_change_var, text_style_var)





        
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
    #print("rr_dict :" + str(rr_dict))
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
    #print("r_dict :" + str(r_dict))
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
    #print("r_list :" + str(r_list))
    return r_dict, r_list, title
