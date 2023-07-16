# give do_ 0 to reduce and 1 to add qty
def reduc_qty(item_info, do_, item_shop_name, item_color, item_size, item_qty_):
    vs_info = "\""
    t = item_info.replace("\"", "") + ","
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
                s_value = s_info[s].split(", ")
                if s_info[s] == s_value[0]:
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
                        if do_ == 0:
                            new_qty = float(s_v.replace("|", ""))-float(item_qty_)
                        if do_ == 1:
                            new_qty = float(s_v.replace("|", ""))+float(item_qty_)
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
