
import os
import atexit
import sys
import tkinter as tk

current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(current_dir, '..')
sys.path.append(MAIN_dir)

from C.List import *

# give do_ 0 to reduce and 1 to add qty
def change_qty(qty_info_list, do_, item_shop_name, item_code, item_color, item_size, item_qty_):
    #print("qty_info_list: "+str(qty_info_list))
    #print("qty_info_list path: "+str(item_shop_name+"|"+item_code+"|"+item_color+"|"+item_size))
    values = get_last_same_path_list(item_shop_name+"|"+item_code+"|"+item_color+"|"+item_size, qty_info_list)[0]
    #print("b values : "+str(values))
    for value in values:
        if len(value) > 2:
            old_qty = value[2]
            new_qty = value[2]
            if do_ == 0:
                new_qty = float(old_qty)-float(item_qty_)
            elif do_ == 1:
                new_qty = float(old_qty)+float(item_qty_)
            value[2] = new_qty
                
    #print("a values : "+str(values))
    cvalues = change_last_same_path_list(item_shop_name+"|"+item_code+"|"+item_color+"|"+item_size, qty_info_list, values)[0]
    print("a cvalues : "+str(cvalues))
    return str(cvalues)
    
def reduc_qty(item_info, do_, item_shop_name, item_color, item_size, item_qty_):
    vs_info = "\""
    t = (item_info.replace("\"", "") + ",").replace(" ", "")
    main_info = t.split("},")
    si = 0
    for m in range(len(main_info)-1):
        si += 1
        main_value = main_info[m].split(",(")
        shop_name = main_value[0].replace("{", "")
        vs_info += '{'
        vs_info += shop_name
        vs_info += ',('
        t = main_value[1].replace(")", "") + ","
        f_info = t.split(">,")
        for c in range(len(f_info)-1):
            f_value = f_info[c].split(",[")
            color_txt = f_value[0].replace("<", "")
            if not c == 0:
                vs_info += ',<'
            else:
                vs_info += '<'
            vs_info += color_txt
            vs_info += ',['
            t = f_value[1].replace("]", "") + ","
            s_info = t.split("|,")
            for s in range(len(s_info)-1):
                vs_info += '|'
                s_value = s_info[s].split(",")
                size_txt = ""
                j = 0
                for s_v in s_value:
                    j += 1
                    print("j :" + str(j) + "sv :" + str(s_v.replace("|", "")))
                    if j == 1:
                        size_txt = s_v.replace("|", "")
                    if j == 4 and shop_name == item_shop_name and item_color == color_txt and item_size == size_txt:
                        new_qty = float(s_v.replace("|", ""))
                        if float(item_qty_) > 0 and (float(s_v.replace("|", ""))-float(item_qty_) > -100 and float(s_v.replace("|", ""))+float(item_qty_) > -100):
                            if do_ == 0:
                                new_qty = float(s_v.replace("|", ""))-float(item_qty_)
                            if do_ == 1:
                                new_qty = float(s_v.replace("|", ""))+float(item_qty_)
                        else:
                            print("in iteminfo there is erorr 0")
                            #while True:
                            #    continue
                        vs_info += str(new_qty)
                    else:
                        vs_info += s_v.replace("|", "")
                    if j <= len(s_value)-1:
                        vs_info += ', '
                if s+1 < len(s_info)-1:
                    vs_info += '|,'
                else:
                    vs_info += '|'
            vs_info += ']'
            if c < len(f_info):
                vs_info += '>'
        vs_info += ')'
        if si < len(main_info):
            vs_info += '},'
        else:
            vs_info += '}'
    vs_info += "\""
    return vs_info
