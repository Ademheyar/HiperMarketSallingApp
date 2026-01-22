import sqlite3
import datetime
import os
import sys
import os
import sys

# for prudoct
def Add_new_on_nested(on_list, given_path, new_value):
    #print("Add_new_on_nested new_value : " + str(new_value))
    def loop_on_nasted_list(ls, pi):
        sub_up = []
        for li, l in enumerate(ls):
            #print("li : " + str(li))
            #print("l : " + str(l))
            #print("given_path l : " + str(len(given_path)))
            #print("given_path : " + str(given_path))
            if pi < len(given_path) and l[0] == given_path[pi]:
                if len(l[1][0]) > 3:
                    #print("Found Mauch main info")
                    #print("pi : " + str(pi))
                    if pi+2 < len(given_path):
                        found = 0
                        for infoi, info in enumerate(l[1]):
                            #print("info : " + str(info))
                            if info[0] == given_path[pi+1] and info[1] == given_path[pi+2]:
                               # print("Found Mauch info going to chang it to new")
                                l[1][infoi] = new_value
                                found = 1
                                break
                        if found == 0:
                            l[1].append(new_value)
                    else:
                        l[1].append(new_value)
                    return 1
                else:
                    #print("Found Mauch next list")
                    ret = loop_on_nasted_list(l[1], pi+1)
                    if not ret:
                        def listt(i):
                            isnewlist = 0
                            ll = None
                            if len(given_path) > 0:
                                ll = [given_path[i]]
                                #print("ll : " + str(ll))
                                isnewlist = 1
                                i+=1
                                if i < len(given_path):
                                    isnewlist, i, ll1 = listt(i)
                                    ll.append([ll1])
                                else:
                                    #add value
                                    ll.append([new_value])
                            return isnewlist, i, ll
                            
                        isnewlist, pi, new_list = listt(pi+1) 
                        #print("new_list : " + str(new_list))           
                        if isnewlist:
                            l[1].append(new_list)
                    return 1
        return 0
    newls = loop_on_nasted_list(on_list, 0)
    return on_list

def add_new_list(_list, paths, value, do_what):
    clist, left_path, fpath = get_last_same_path_list(paths, _list)
    if not fpath:
        left_path = paths
    new_list = []
    def listt(i):
        isnewlist = 0
        l0 = left_path
        ll = None
        if len(l0) > 0:
            ll = [l0[i]]
            #print("ll : " + str(ll))
            isnewlist = 1
            i+=1
            if i < len(l0):
                isnewlist, i, ll1 = listt(i)
                ll.append([ll1])
            else:
                #add value
                ll.append([value])
        return isnewlist, i, ll
        
    isnewlist, i, new_list = listt(0) 
    #print("new_list : " + str(new_list))           
    if isnewlist:
        if not fpath:
            #print("not fpath : " + str(new_list))
            clist.append(new_list)
        else:
            #print("paths, _list, new_list : " + str([paths, _list, new_list]))
            clist = Add_new_on_nested(_list, paths, value)
    return isnewlist, clist


def dele_on_nested(on_list, given_path, new_value):
    #print("new_value : " + str(new_value))
    def loop_on_nasted_list(ls, pi):
        sub_up = []
        for li, l in enumerate(ls):
            #print("li : " + str(li))
            #print("l : " + str(l))
            #print("given_path l : " + str(len(given_path)))
            #print("given_path : " + str(given_path))
            if l[0] == given_path[pi]:
                if l[1] and len(l[1][0]) > 3:
                    #print("Found Mauch main info")
                    #print("pi : " + str(pi))
                    if pi+2 < len(given_path):
                        found = 0
                        for infoi, info in enumerate(l[1]):
                            #print("info : " + str(info))
                            if info[0] == given_path[pi+1] and info[1] == given_path[pi+2]:
                                #print("Found Mauch info going to chang it to new")
                                l[1].remove(l[1][infoi])
                                found = 1
                                break
                        if found == 0:
                            l = []
                            return 1
                    else:
                        l = []
                    return 1
                
                elif pi+1 < len(given_path):
                    #print("Found Mauch next list")
                    ret = loop_on_nasted_list(l[1], pi+1)
                    if ret:
                        return 1
                else:
                    ls.remove(ls[li])
        return 0
    newls = loop_on_nasted_list(on_list, 0)
    return on_list

    
def dele_list(_list, paths, value):
    leng = len(paths)
    clist = _list
    if leng != 0:
        if leng >= 2:
            clist = dele_on_nested(_list, paths, value)
        else:
            for i, l in enumerate(_list):
                if l[0] == paths[0]:
                    clist.remove(_list[i])
    return 1, clist

# this will convert text old list saving to new listnode
def read_code(vs_info, shop_s, code_s, color_s, size_s):
    a_u_list = []
    shops = []
    codes = []
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
        code_nodes = []
        
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

                s_n = [s_value[0].replace("|", "").strip()]
                s_n_v = []
                for si in range(len(s_value)-1):
                    if (not shop_s == "" and shop_s == shop_name) and \
                    (not color_s == "" and color_s == color_txt) and \
                    (size_s == "" or size_s == s_value[si].replace("|", "").strip()):
                        if si == 0:
                            sizes.append(s_value[si].replace("|", "").strip())
                        elif si == 1:
                            self.selected_barcode.set(s_value[si].strip())
                    if not si == 0:
                        s_n_v.append(s_value[si].replace("|", "").strip())
                s_n.append([s_n_v])
                color_node.append(s_n)
                
            color.append(color_node)
            code_nodes.append(color)
        code = [code_s, code_nodes]
        shop_node.append(code)
        shop.append(shop_node)
        a_u_list.append(shop)

    return shops, codes, colors, sizes, a_u_list


def load_list(text):
    def sub_list(t, i):
        #print("\n reding next t = " +str(t)+"on line "+str(i))
        rv = ""
        pp = ""
        rl = []
        v=[]
        while i < len(t):
            if t[i] == '\'' or t[i] == '\"':
                i+=1
                if rv == "":
                    rv = " "
                continue
            if t[i] == "[":
                i+=1
                if rv == " ":
                    rv = ""
                i, v = sub_list(t, i)
                rl.append(v)
                #print("\n out [ v = " +str(rl)+"on "+str(v))
                #print("\n rv = " +str(rv)+"on "+str(i))
                continue
                
            if t[i] == "]":
                if t[i+1] == "]" or t[i+1] == ",":
                    if rv != "":
                        rl.append(rv)
                        rv == " "
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
                if rv == " ":
                    rv = ""
                rv += t[i]
                i+=1
        #print("pp : " + str(pp))
        return i, rl
    ret = sub_list(text+",", 0)[1]
    #print("ret : " + str(ret[0]))
    if len(ret) != 0 or ret:
        ret = ret[0]
    else:
        ret = []
    return ret

def convert_list_to_text(_list):
    return str(_list)

def search_list_name(name, liston):
    if liston and len(liston):
        for l in liston:
            if l[0] == name:
                return l[1]
    return None

def get_last_same_path_list(paths, _list):
    if not _list or _list == []:
        return [], paths, 0
    corrontl = _list
    left_path = ""
    get_left_path = 0
    found_path = 0
    for path in paths:
        if left_path:
            left_path += "|" + path
        else:
            ret = search_list_name(path, corrontl)
            if ret:
                corrontl = ret
                found_path+=1
            else:
                get_left_path = 1
                left_path += path
    return corrontl, paths, found_path

def change_last_same_path_list(paths, _list, new_list):
    corrontl = _list
    left_path = ""
    get_left_path = 0
    found_path = 0
    for path in paths.split("|"):
        if left_path:
            left_path += "|" + path
        else:
            ret = search_list_name(path, corrontl)
            if ret:
                corrontl = ret
                found_path+=1
            else:
                get_left_path = 1
                left_path += path
    corrontl = new_list
    return _list, left_path, found_path

def get_semilar_paths(given_path, on_list):
    found_p = []
    def loop_on_nasted_list(ls, pi):
        sub_up = []
        for li, l in enumerate(ls):
            ppi = 0
            #print("l : " + str(l))
            #print("pf : " + str(pf))
            #print("pl : " + str(pl))
            #if pi < len(path):
                #print(str(len(given_path))+"given_path["+str(pi)+"] : " + str(given_path[pi]))
            if pi < len(given_path) and l[0] == given_path[pi]:
                found_p.append(pl)
                #print("l[0] == given_path[pi] : " + str(given_path[pi]))
                
            if len(l) <= 2:
                sub_sub_up = [l[0]]
                #print("sub_sub_up : " + str(sub_sub_up))
                ret = loop_on_nasted_list(l[1], pi+1)
                sub_sub_up.append(ret)
                if pi >= len(given_path) and ppi:
                    sub_sub_up.append(new_l)
                    #print("new sub_up : " + str(sub_sub_up))
                else:
                    sub_up.append(sub_sub_up)
                    #print("copy sub_up : " + str(sub_sub_up))
            else:
                if pi >= len(given_path):
                    sub_up.append(new_l)
                    #print("new2 sub_up : " + str(sub_up))
                else:
                    sub_up.append(l)
                    #print("copy2 sub_up : " + str(sub_up))
        return sub_up
    loop_on_nasted_list(on_list, 0)
    return found_p


    
def add_at_last_same_path_list(paths, _list, new_l, do_what):
    up = []
    found_p = []
    path = paths
    
    def copy_list(ls, pf, pi, pl):
        sub_up = []
        for li, l in enumerate(ls):
            ppi = 0
            #print("l : " + str(l))
            #print("pf : " + str(pf))
            #print("pl : " + str(pl))
            #if pi < len(path):
                #print(str(len(path))+"path["+str(pi)+"] : " + str(path[pi]))
            if pf and pi < len(path) and l[0] == path[pi]:
                ppi = 1
                pl = pl+[li]
                found_p.append(pl)
                #print("l[0] == path[pi] : " + str(path[pi]))
                
            if len(l) <= 2:
                sub_sub_up = [l[0]]
                #print("sub_sub_up : " + str(sub_sub_up))
                ret = copy_list(l[1], ppi, pi+1, pl)
                sub_sub_up.append(ret)
                if pi >= len(path) and ppi:
                    sub_sub_up.append(new_l)
                    #print("new sub_up : " + str(sub_sub_up))
                else:
                    sub_up.append(sub_sub_up)
                    #print("copy sub_up : " + str(sub_sub_up))
            else:
                if pi >= len(path) and ppi:
                    sub_up.append(new_l)
                    #print("new2 sub_up : " + str(sub_up))
                else:
                    sub_up.append(l)
                    #print("copy2 sub_up : " + str(sub_up))
        return sub_up
    
    
    def add_s(mlist, path, new_sub):
        current = mlist
        onc = -1
        #print("path : " + str(path))
        for c, index in enumerate(path):
            #print("in list  : " + str(current))
            if index < len(current):
                current = current[index][1]
                if len(current[0]) > 2:
                    onc = c
                    break  
            else:
                #print("filed : " + str(c) +" v "+ str(index))
                return mlist
        #print("current : " + str(current))
        if len(current[0]) > 2:
            if onc >= 0 and onc+1 < len(path):
                for ind, item in enumerate(current):
                    if current[ind] == path[onc+1] and current[ind] == path[onc+2]:
                        current[ind] = new_sub[1][0]
                        break
            elif do_what == 0: # change
                current[0] = new_sub[1][0]
            else: # add new one
                current.append(new_sub[1][0])    
            #print("current1 : " + str(current))
        else:
            current.append(new_sub)
            #print("current2 : " + str(current))
        return mlist
    
    sub = copy_list(_list, 1, 0, [])
    
    fpi = 0
    fpl = 0
    #print("found_p : " + str(found_p))
    for j, fp in enumerate(found_p):
        #print("\n\n\nfound_p["+str(j)+"] : " + str(fp))
        if len(fp) > fpl:
            #print("found long")
            fpi = j
            fpl = len(fp)
            
    #print("sub : " + str(sub))
    #up.append()
    sub = add_s(sub, found_p[fpi], new_l)
    #print("up : " + str(sub))
    return sub


def change_at_last_same_path_list(paths, _list, new_l):
    up = []
    found_p = []
    path = paths.split("|")
    def copy_list(ls, pf, pi, pl):
        for li, l in enumerate(ls):
            ppi = 0
            #print("l : " + str(l))
            #print("pf : " + str(pf))
            #print("pl : " + str(pl))
            #if pi < len(path):
                #print(str(len(path))+"path["+str(pi)+"] : " + str(path[pi]))
            if pf and pi < len(path) and l[0] == path[pi]:
                ppi = 1
                pl = pl+[li]
                found_p.append(pl)
                #print("l[0] == path[pi] : " + str(path[pi]))
                
            if len(l) == 2 :
                copy_list(l[1], ppi, pi+1, pl)
    
    def add_s(mlist, path, new_sub):
        current = mlist
        #print("path : " + str(path))
        for c, index in enumerate(path):
            #print("in list  : " + str(current))
            if index < len(current):
                if len(path)-1 == c+1:
                    current = current
                else:
                    current = current[index][1]
            else:
                #print("filed : " + str(c) +" v "+ str(index))
                return mlist
        #print("current : " + str(current))
        if len(current[0]) > 2:
            current[0] = []
            #print("current1 : " + str(current))
        else:
            current.remove(current[0])
            #print("current2 : " + str(current))
        return mlist
    
    copy_list(_list, 1, 0, [])
    
    fpi = 0
    fpl = 0
    #print("found_p : " + str(found_p))
    for j, fp in enumerate(found_p):
        #print("\n\n\nfound_p["+str(j)+"] : " + str(fp))
        if len(fp) > fpl:
            #print("found long")
            fpi = j
            fpl = len(fp)
            
    #print("sub : " + str(_list))
    #up.append()
    _list = add_s(_list, found_p[fpi], new_l)
    #print("up : " + str(_list))
    return _list

    
def change_list(_list, paths, value):
    clist, left_path, fpath = get_last_same_path_list(paths, _list)
    if not fpath:
        left_path = paths
    clist = change_at_last_same_path_list(paths, _list, [])
    return 1, clist
