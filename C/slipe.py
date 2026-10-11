import sqlite3
import datetime
import os
import sys
import os
import sys
current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(current_dir, '..')
sys.path.append(MAIN_dir)
#from M.Display import DisplayFrame

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')

from C.API.Get import *
from C.API.API import *
from C.API.Set import *

def find_user(Linke, v):
    it = None
    if v and v.isdigit():
        
        it = fetch_as_dict_list(Linke, "SELECT * FROM users WHERE User_id=?", (v,))
    elif  v and not v == 'None':
        it = fetch_as_dict_list(Linke, "SELECT * FROM users WHERE User_name=?", (v,))
    if it:
        return it[0]
    
def find_shop(Linke, id):
    if id and id.isdigit():
        results = fetch_as_dict_list(Linke, "SELECT * FROM Shops WHERE Shop_Id=?", (id,))
    elif  id and not id == 'None':
        results = fetch_as_dict_list(Linke, "SELECT * FROM Shops WHERE Shop_brand_name=?", (id,))
    if results:
        print("found shop ", results)
        return results[0]
    return None

def add_text_(width, value):
    ret = ""
    i = 0
    for l in value:
        ret += l
        i+=1
    return [ret]
    
def add_ltext_(width, value, do=""):
    ret = ""
    i = 0
    for l in value:
        ret += l
        i+=1
        if i == int(width):
            if not do or do == "":
               break
            else:
                ret+=do 
    return [ret]
    
def get_sparet_2(Linke, doc, width, pvv, user, shop):
    ret = ""
    for i in range(int(width)):
        ret += "_"
    return [ret + "\n"]

def get_Information(Linke, doc, width, pvv, user, shop):
    if doc.get("_preview_receipt_sections") is not None:
        return [""]
    v = shop['Shop_Adress_Information']
    ret = ""
    if v and "+" in v:
        infos = v.split("+")
        for l in infos:
            info = l.split("=")
            if "Location" == info[0]:
                ret += "* "+ add_ltext_(width, info[1], "\n")[0] + "\n"
        wod = 0        
        for l in infos:
            info = l.split("=")
            if wod + len(info[0]) >= round(float(width))+1:
                ret += "\n"
            if "Phone Number" == info[0]:
                ret += "[] "+add_ltext_(width, info[1])[0]
        ret += "\n" 
    return [ret + "\n"]

def get_About(Linke, doc, width, pvv, user, shop):
    v = shop['Shop_about']
    ret = ""
    if v and "+" in v:
        Shop_about = v.split("+")
        for l in Shop_about:
            ret += add_ltext_(width, l)[0] + "\n"
    elif v:
        ret += add_ltext_(width, v)[0] + "\n"
    return [ret]

def get_Phone_No(Linke, doc, width, pvv, user, shop):
    v = "" # shop['Shop_phone_num'] TODO : get phone number
    ret = ""
    if v and "+" in v:
        location = v.split("+")
        for l in location:
            ret +=  add_ltext_(width, l)[0] + "\n"
    elif v:
        ret +=  add_ltext_(width, v)[0]
        return [ret]

def get_Receipt_no(Linke, doc, width, pvv, user, shop):
    return ["Receipt No : " + str(doc['doc_barcode']) + "\n"]

def get_extnsion_Receipt_no(Linke, doc, width, pvv, user, shop):
    if not str(doc['extension_barcode']) == 'extension_barcode':
        return ["extnsion Receipt No :  " + str(doc['extension_barcode']) + "\n"]
           
def get_date(Linke, doc, width, pvv, user, shop):
    return ["Date :  " + str(doc['doc_created_date']) + "\n"]
           
def get_updated_date(Linke, doc, width, pvv, user, shop):
    if not str(doc['doc_created_date']) == str(doc['doc_updated_date']):
        return ["updated Date :  " + str(doc['doc_updated_date']) + "\n"]
           
def get_Due_date(Linke, doc, width, pvv, user, shop):
    if doc.get("_preview_receipt_sections") is not None:
        return ["Due Date :  " + str(doc['doc_expire_date']) + "\n"]
    if not str(doc['doc_created_date']) == str(doc['doc_expire_date']):
        return ["Due Date :  " + str(doc['doc_expire_date']) + "\n"]

def get_user(Linke, doc, width, pvv, user, shop):
    slip =""
    # get user and custemusr infor
    it = find_user(Linke, doc['user_id'])
    if it:
        #print("it c: " + str(it))   
        slip += "User : "+ str(it['User_name']) +"\n"
    return [slip]

def get_seller(Linke, doc, width, pvv, user, shop):
    slip = ""
    # get Seller info    if len(doc) > 16 and doc['Seller_id'] and doc['Seller_id'] != "":
    it = find_user(Linke, doc['Seller_id'])
    if it:
        #print("it c: " + str(it))   
        slip += "Seller : "+ str(it['User_name']) +"\n"
    return [slip]
            
def get_customer(Linke, doc, width, pvv, user, shop):
    slip = ""
    # get custemur info
    if doc['customer_id'] != "":
        it = find_user(Linke, doc['customer_id'])
        if it:
            #print("it c: " + str(it))   
            slip += "Customer : "+ str(it['User_name']) +"\n"\
                    "Phone No : "+ str(it['User_phone_num']) +"\n"
    return [slip]

shop, color, size, PRICE, QTY, Disc, TAX, payments, taxstr = \
    ["", "", "", 0, 0, 0, 0, "", ""]
def get_items(Linke, doc, width, pvv, user, shop):
    # get items
    #print("load_slip items : " + str(doc['item']))
    slip = ""
    shop, color, size, PRICE, QTY, Disc, TAX, payments = \
    ["", "", "", 0, 0, 0, 0, ""]
    v = []
    items_lists = str(doc['item'])
    list_items_copy = json.loads(items_lists)
    T_price = 0
    T_Disc = 0
    count = 1
    thereisdic = 0
    last_discount = 0
    for iv in list_items_copy:
        print("load_slip items iv: " + str(iv))
        # id, code, bar, name, shop, color, size, qty, price, disc, T_price = iv
        QTY += round(float(iv[7]))
        total_price = float(iv[7])*float(iv[8])
        PRICE += float(total_price)
        T_Disc += float(iv[9])
        last_discount = float(iv[9])
        TAX += float(0)
        price = str(iv[8])
        T_price += float(iv[8])+float(iv[9])
        if float(iv[9]) != 0:
            price = str(float(iv[8])+float(iv[9])+(-float(iv[9])))
            if not float(iv[9]) < 0:
                price = str(float(iv[8])+float(iv[9]))+"-"+str(float(iv[9]))
                thereisdic = 1
        # No : Code   : Name      : qty : price - Disc : totale :
        v.append([str(count), str(iv[1]), str(iv[3]), str(round(float(iv[7]))), price, str(total_price)])
        count += 1
    # No : Code   : Name      : qty : price  : totale :
    itemforslip = ""
    #print("v : " + str(v))
    if thereisdic:
        vsl = [2, 4, 4, 3, 8, 4] # tall the maximam space for columens
    else:
        vsl = [2, 4, 4, 3, 4, 4] # tall the maximam space for columens
    tw=21
    width = int(width)
    while not (tw+5 > width-3 and tw+5 < width+3):
        if tw+5 < width:
            vsl = [2 , vsl[1]+1, vsl[2]+2, vsl[3], vsl[4]+1, vsl[5]+1]
            tw += 7
        elif tw+5 > width:
            vsl = [2, vsl[1]-1, vsl[2]-1, vsl[3], vsl[4]-1, vsl[5]-1]
            tw -= 4

    preview_sections = doc.get("_preview_receipt_sections")
    v.append([
        str('-'*vsl[0]), str("-"*vsl[1]), str("-"*vsl[2]),
        str("-"*vsl[3]), str("-"*vsl[4]), str('-'*vsl[5]),
    ])
    if preview_sections is not None:
        v.append(["", "", "TOTAL ", str(QTY), str(PRICE), str(PRICE)])
    elif T_Disc != 0 and last_discount >= 0:
        v.append([
            "", "", "TOTAL ", str(QTY),
            str(PRICE + T_Disc) + "-" + str(T_Disc), str(PRICE),
        ])
    else:
        v.append(["", "", "TOTAL ", str(QTY), str(PRICE), str(PRICE)])
    for countv, vs in enumerate(v):
        vl = vsl
        vsy = ['.', '/', ' ', 'x', '=', ' ']
        vvi = 0
        for vi in vl:
            for w in range(vi):
                if w < len(vs[vvi]):
                    #print("vs[] : " + str(vs[vvi])+ " vvi :" + str(vvi) + " w :" + str(w))
                    itemforslip += vs[vvi][w]
                else:
                    itemforslip += ' '
            if not len(v) == countv+1 and not len(v) == countv+2:
                itemforslip += vsy[vvi]
            elif len(v) == countv+2:
                 itemforslip += "-"
            else:
                itemforslip += " " # this will skip any simbols for the last list
            vvi += 1
        itemforslip += "\n"
    
    itemcolumnsforslip = ""
    #print("v : " + str(v))
    vi = 0
    if thereisdic:
        vs = ["NO", "CODE", "NAME", "QTY", "PRICE-DISC", "TOTAL"] #21 letters + 5 spaces + 5 Blockes = 31
    else:
        vs = ["NO", "CODE", "NAME", "QTY", "PRICE", "TOTAL"] #21 letters + 5 spaces + 5 Blockes = 31
    von = 0
    won = 0 
    for wid in range(int(width)):
        if von >= len(vs):
            itemcolumnsforslip += " "
            continue
            
        if won < vsl[von]: # chacke it is not more that given space
            if won < len(vs[von]):
                itemcolumnsforslip += vs[von][won]
                won += 1
            elif won < vsl[von]:
                itemcolumnsforslip += " "
                won += 1
            elif von < len(vs):
                von += 1
                won = 0
            else:
                itemcolumnsforslip += " "
        else:
            itemcolumnsforslip += "|"
            von += 1
            won = 0
            
    slip += itemcolumnsforslip +"\n"
    slip += get_sparet_2(Linke, doc, width, pvv, user, shop)[0]
    slip += itemforslip + "\n"
    if preview_sections is not None:
        return [slip, [QTY, PRICE, Disc, TAX, T_price]]

    #infos_needed = ["TOTAL QTY", "TOTAL Price", "TOTAL Tax", "TOTAL Discount", "Recived", "Balance"]
    infos_needed = ["TOTAL Price", "TOTAL Tax", "TOTAL Discount", "Recived", "Balance", "LEFT"]
    #, "CHANGE"
    # paymenats 
    given_info = []
    totalitemforslip = ""
    pvv = [QTY, PRICE, TAX, Disc, T_price]
    if len(pvv) == 5:
        if doc['pid']:
            #pvv = [str(pvv[0]), str(pvv[1]), str(pvv[2]), str(pvv[3]), str(float(doc['pid'])), "0"]
            pvv = [str(pvv[1]), str(pvv[2]), str(pvv[3]), str(float(doc['pid'])), "0", "0"]
            # , str(str(float(doc['pid'])-(PRICE-Disc)))
        else:
            #pvv = [str(pvv[0]), str(pvv[1]), str(pvv[2]), str(pvv[3]), str(float(pvv[4])), str(float(pvv[4]))]
            pvv = [str(pvv[1]), str(pvv[2]), str(pvv[3]), str(float(pvv[4])), str(float(pvv[4])), '0']

    done_inserting = 0
    infos_need_on = -1
    payment_on = -1
    hafe_width = int(width)//2
    list_payment_copy = json.loads(doc['payments'])
    
    while(infos_need_on < len(pvv)) or payment_on < len(list_payment_copy):
        fwon = 0
        fw = 0
        swon = 0
        
        # if the value is 0 or Null pass it no need to print
        #if infos_need_on < len(pvv) and float(pvv[infos_need_on]) == 0:
            #infos_need_on+=1
            #continue
        
        for wid in range(int(width)):
            if done_inserting == 0:
                intesd = infos_need_on+1
                while intesd < len(pvv) and float(pvv[intesd]) == float('0'):
                    intesd += 1
                
                if intesd < len(pvv) or payment_on < len(list_payment_copy):
                    totalitemforslip += "_" 
                continue
            
            if wid < hafe_width:
                if payment_on < len(list_payment_copy):
                    price = list_payment_copy[payment_on][1]
                    if " " in list_payment_copy[payment_on][5]:
                        fusername = list_payment_copy[payment_on][5].split(" ")[0]
                    else:
                        fusername = list_payment_copy[payment_on][5]
                    F = fusername + " " + str(list_payment_copy[payment_on][1]) + ", " +  str(list_payment_copy[payment_on][2])
                    S = list_payment_copy[payment_on][3]+ ", " # pay_updated_date.split()[0] + ", " 
                    if fw < len(F):
                        totalitemforslip += F[fw]
                        fw +=1
                    else:
                        totalitemforslip += " "
                else:
                    totalitemforslip += " "
            elif infos_need_on < len(pvv):
                if wid == hafe_width + 1 + (hafe_width/2):
                    totalitemforslip += "|"
                elif(wid < hafe_width + 1 + (hafe_width//2) and fwon < len(infos_needed[infos_need_on])):
                    totalitemforslip += infos_needed[infos_need_on][fwon]
                    fwon +=1
                elif(wid > hafe_width + 1 + (hafe_width//2) and swon < len(pvv[infos_need_on])):
                    totalitemforslip += pvv[infos_need_on][swon]
                    swon +=1
                else:
                    totalitemforslip += " "
            
        if done_inserting == 0:
            done_inserting = 1
            infos_need_on += 1
            while (payment_on >= len(list_payment_copy)) and (infos_need_on < len(pvv) and (pvv[infos_need_on] == '0' or pvv[infos_need_on] == '0.0')):
                infos_need_on += 1
            payment_on += 1
            if infos_need_on < len(pvv) or payment_on < len(list_payment_copy):
                totalitemforslip += "\n" 
        else:
            totalitemforslip += "\n" 
            done_inserting = 0
            
    slip += totalitemforslip + "\n"
    return [slip, [QTY, PRICE, Disc, TAX, T_price]]
    
def get_payments(Linke, doc, width, pvv, user, shop):
    slip = ""
    return [slip]

def get_total(Linke, doc, width, pvv, user, shop):
    slip = ""
    return [slip]

import string

def get_Rules(Linke, doc, width, pvv, user, shop):
    v = shop['Shop_rules']
    ret = ""
    if v and "+" in v:
        ruls = v.split("+")
        def letter_count(sen):
            return len([char for char in sen if char.isalpha()])
        sorted_sentences = sorted(ruls, key=letter_count)
        i = 0
        for l in ruls:
            i+=1
            ret += str(i)+". "+add_text_(width, l)[0] + "\n"
    elif v:
        ret += v + "\n"
    return [ret]

def parse_slip_rules(value):
    return [rule.strip() for rule in str(value or "").split("+") if rule.strip()]

def format_slip_rules(rules):
    selected = [str(rule).strip() for rule in rules if str(rule).strip()]
    if len(selected) > 1:
        return "".join(f"{index}. {rule}\n" for index, rule in enumerate(selected, 1))
    return selected[0] + "\n" if selected else ""

def get_Social(Linke, doc, width, pvv, user, shop):
    links = parse_social_links(shop.get("Shop_SocLinks"))
    return [format_social_links(links)]

def parse_social_links(value):
    return [
        link.strip()
        for link in str(value or "").split("+")
        if link.strip()
    ]

def format_social_links(links):
    value = "\n".join(links)
    return value + ("\n" if value else "")

def get_shop_information_values(shop, label):
    values = []
    for field in str(shop.get("Shop_Adress_Information") or "").split("+"):
        key, separator, value = field.partition("=")
        if separator and key.strip() == label:
            values.extend(
                part.strip()
                for part in value.split("=")
                if part.strip()
            )
    return values

def get_Location(Linke, doc, width, pvv, user, shop):
    locations = get_shop_information_values(shop, "Location")
    return ["".join(f"* {location}\n" for location in locations)]

def get_Shop_Phone(Linke, doc, width, pvv, user, shop):
    phones = get_shop_information_values(shop, "Phone Number")
    return ["".join(f"Phone Number: {phone}\n" for phone in phones)]

def get_Payments(Linke, doc, width, pvv, user, shop):
    payments = json.loads(str(doc.get("payments") or "[]"))
    return ["".join(
        f"{payment[0]} {payment[1]}: {payment[2]}\n"
        for payment in payments if len(payment) > 2
    )]

def get_Total_Payment(Linke, doc, width, pvv, user, shop):
    total = float(doc.get("price") or 0)
    tax = float(doc.get("tax") or 0)
    discount = float(doc.get("discount") or 0)
    received = float(doc.get("pid") or 0)
    amount_due = total + tax - discount
    balance = max(amount_due - received, 0)
    return [
        f"Total: {total:.2f}\n"
        f"Tax: {tax:.2f}\n"
        f"Discount: {discount:.2f}\n"
        f"Received: {received:.2f}\n"
        f"Balance: {balance:.2f}\n"
    ]

def get_Logo(Linke, doc, width, pvv, user, shop):
    if width == "":
        width = 20
    logo = shop['Shop_name'] # 
    # TODO: MAKE SOURE IT IS ALLOWED AND CHACKE BEAND NAME OR SHOP NAME TO DISPLAY
    ret = ("-"*(round(float(width))-1))+"\n"
    size = str(round(float(width))-4)
    ret += f"| {logo:^{size}} |\n"
    ret += ("-"*(round(float(width))-1))+"\n"
    return [ret]

def get_sparet(Linke, doc, width, pvv, user, shop):
    ret = ""
    for i in range(int(width)):
        ret += "*"
    return [ret + "\n"]

def get_sparet_0(Linke, doc, width, pvv, user, shop):
    ret = ""
    for i in range(int(width)):
        ret += "#"
    return [ret + "\n"]

def get_sparet_1(Linke, doc, width, pvv, user, shop):
    ret = ""
    for i in range(int(width)):
        ret += "-"
    return [ret + "\n"]

def get_sparet_3(Linke, doc, width, pvv, user, shop):
    ret = ""
    for i in range(int(width)):
        ret += "="
    return [ret + "\n"]

def get_sparet_4(Linke, doc, width, pvv, user, shop):
    ret = ""
    for i in range(int(width)):
        ret += "~"
    return [ret + "\n"]

slip_order_type=[
    get_sparet, get_sparet_0, get_sparet_1, get_sparet_2, get_sparet_3,
    get_sparet_4, get_Logo, get_Information, get_About, get_Phone_No,
    get_Receipt_no, get_extnsion_Receipt_no, get_date, get_updated_date,
    get_Due_date, get_user, get_seller, get_customer, get_items, get_Rules,
    get_Social, get_Location, get_Shop_Phone, get_Payments, get_Total_Payment,
]

slip_order_labels = [
    "*", "#", "-", "_", "=", "~", "Shop Name", "Shop Information",
    "Shop About", "Shop Phone", "Receipt Number", "Extension Receipt Number",
    "Sale Date", "Updated Date", "Expiry Date", "User Name", "Seller",
    "Customer Information", "Items", "Rules", "Social", "Location",
    "Phone Number", "Payments", "Total Payment",
]

def _insert_preview_order(orders, section_index, anchors):
    for position, order in enumerate(orders):
        try:
            if int(order[0]) == section_index:
                return
        except (IndexError, TypeError, ValueError):
            continue
    anchor_positions = []
    for position, order in enumerate(orders):
        try:
            if int(order[0]) in anchors:
                anchor_positions.append(position)
        except (IndexError, TypeError, ValueError):
            continue
    insert_at = min(anchor_positions) if anchor_positions else len(orders)
    orders.insert(insert_at, [str(section_index)])

def _complete_preview_order(orders):
    orders = list(orders)
    for section_index in (20, 21, 22):
        _insert_preview_order(
            orders, section_index,
            set(range(10, 20)) | {23, 24},
        )
    for section_index in (12, 14, 15, 17):
        _insert_preview_order(orders, section_index, {18, 19, 23, 24})
    _insert_preview_order(orders, 18, {19, 23, 24})
    _insert_preview_order(orders, 23, {24, 19})
    _insert_preview_order(orders, 24, {19})
    _insert_preview_order(orders, 19, set())
    return orders

import json
import ast
import textwrap


def _format_payment_summary_columns(payment_text, total_text, width):
    width = max(1, int(width))
    if not payment_text:
        return total_text
    if not total_text:
        return payment_text

    left_width = max(1, (width - 3) // 2)
    right_width = max(1, width - left_width - 3)
    left_lines = [
        wrapped
        for line in payment_text.splitlines()
        for wrapped in (textwrap.wrap(line, left_width) or [""])
    ]
    right_lines = [
        wrapped
        for line in total_text.splitlines()
        for wrapped in (textwrap.wrap(line, right_width) or [""])
    ]
    row_count = max(len(left_lines), len(right_lines))
    return "".join(
        f"{left_lines[index] if index < len(left_lines) else '':<{left_width}}"
        f" | "
        f"{right_lines[index] if index < len(right_lines) else ''}\n"
        for index in range(row_count)
    )

def load_slip(
    Linke, doc, d_id, shop_override=None, receipt_sections=None,
    capture_sections=None,
):
    print("doc : "+str(doc))
    user = find_user(Linke, doc['user_id'])
    print("User : ", user)
    at_shop = shop_override or find_shop(Linke, doc['At_Shop_Id'])
    print("at_shop", at_shop)

    slip = ""
    footer = ""
    preview_mode = receipt_sections is not None or capture_sections is not None
    if preview_mode:
        doc = dict(doc)
        doc["_preview_receipt_sections"] = (
            receipt_sections if receipt_sections is not None else {}
        )
        if at_shop and not at_shop.get("Shop_Slip_Settings"):
            at_shop = dict(at_shop)
            at_shop["Shop_Slip_Settings"] = json.dumps([
                [42, 0],
                [
                    ["6"], ["7"], ["8"], ["20"], ["21"], ["22"], ["10"],
                    ["12"], ["14"], ["15"], ["17"], ["18"], ["23"], ["24"],
                    ["19"],
                ],
            ])
    if at_shop and at_shop['Shop_Slip_Settings']:
        sittings = json.loads(at_shop['Shop_Slip_Settings'])
        print("sittings : "+str(sittings))
        width = sittings[0][0]
        hight = sittings[0][1]
        orders = sittings[1]
        if preview_mode:
            orders = _complete_preview_order(orders)
        # Make shouer that user shop is same as viewing admin
        print("width : "+str(width))
        print("order : "+str(orders))
        print("shop : "+str(at_shop))
        pvv = []
        section_occurrences = {}
        captured = []
        rendered_sections = []
        for order in orders:
            if order != "":
                order_index = int(order[0])
                occurrence = section_occurrences.get(order_index, 0)
                section_occurrences[order_index] = occurrence + 1
                section_key = f"{order_index}:{occurrence}"
                ret = slip_order_type[order_index](Linke, doc, width, pvv, user, at_shop)
                section_text = ""
                if ret:
                    if len(ret) == 1:
                        section_text = ret[0]
                    elif len(ret) == 2:
                        section_text = ret[0]
                        pvv = ret[1]
                if preview_mode and receipt_sections is not None:
                    section_text = receipt_sections.get(section_key, section_text)
                rendered_sections.append((order_index, section_text))
                if capture_sections is not None:
                    label = (
                        slip_order_labels[order_index]
                        if 0 <= order_index < len(slip_order_labels)
                        else f"Receipt Section {order_index}"
                    )
                    captured.append({
                        "key": section_key,
                        "index": order_index,
                        "label": label,
                        "text": section_text,
                    })
        payment_position = next(
            (
                position for position, (index, _text) in enumerate(rendered_sections)
                if index == 23
            ),
            None,
        )
        total_position = next(
            (
                position for position, (index, _text) in enumerate(rendered_sections)
                if index == 24
            ),
            None,
        )
        paired_positions = set()
        if payment_position is not None and total_position is not None:
            payment_text = rendered_sections[payment_position][1]
            total_text = rendered_sections[total_position][1]
            rendered_sections[payment_position] = (
                23,
                _format_payment_summary_columns(payment_text, total_text, width),
            )
            rendered_sections[total_position] = (24, "")
            paired_positions.add(total_position)
        slip += "".join(
            text
            for position, (_index, text) in enumerate(rendered_sections)
            if position not in paired_positions
        )
        footer = "   THANK YOU FOR SHOPING WITH US     \n" \
                 "          " + str(doc['doc_barcode']) + "       \n"
        if preview_mode and receipt_sections is not None:
            footer = receipt_sections.get("_footer", footer)
        if capture_sections is not None:
            captured.append({
                "key": "_footer",
                "index": None,
                "label": "Thank You and Receipt Barcode",
                "text": footer,
            })
            capture_sections[:] = captured

    else:
        #get informations
        #print("doc in lload slip = " + str(doc))
        slip = "             MAMS MALL                   \n"\
               "    INFRONT OF PNP CLOTHING AND MR.PRICE \n"\
               "*****************************************\n" \
               "JOIN SOCIAL MIDEIA FOR NEW ARRIVALS \n" \
               "WITH SPCIAL DISCOUN                 \n" \
               "INSTAGRAM   : @ADOTOUTFIT\n" \
               "WEBSITE     : http://adot.unaux.com\n" \
               "WHATS UP    : MESSAGE AS ON\n" \
               "     +276 12231 353 \n" \
               "*****************************************\n" 
        #get doc information
        slip += "Receipt No : " + str(doc['doc_barcode']) + "\n"\
                "extnsion Receipt No :  " + str(doc['extension_barcode']) + "\n"\
                "Date :  " + str(doc['doc_created_date']) + "\n"\
                "updated Date :  " + str(doc['doc_updated_date']) + "\n"\
                "Due Date :  " + str(doc['doc_expire_date']) + "\n"\
                "------------------------------------------\n" 
        # get user and custemusr infor
        it = find_user(Linke, doc['user_id'])
        if it:
            print("it c: " + str(it))   
            slip += "User : "+ str(it['User_name']) +"\n"
        
        # get Seller info    if len(doc) > 16 and doc['Seller_id'] and doc['Seller_id'] != "":
        it = find_user(Linke, doc['Seller_id'])
        if it:
            #print("it c: " + str(it))   
            slip += "Seller : "+ str(it['User_name']) +"\n"
                
                
        # get custemur info
        if doc['customer_id'] != "":
            it = find_user(Linke, doc['customer_id'])
            if it:
                #print("it c: " + str(it))   
                slip += "Customer : "+ str(it['User_name']) +"\n"\
                        "Phone No : "+ str(it['User_phone_num']) +"\n"
        
        slip += "------------------------------------------\n"

        # get items
        #print("load_slip items : " + str(doc['item']))
        shop, color, size, PRICE, QTY, Disc, TAX, payments = \
        ["", "", "", 0, 0, 0, 0, ""]
        v = []
        items_ = str(doc['item']) + ","
        items_lists = items_.split("|),")
        if ":)," in items_:
            #print("spliting by :")
            items_lists = items_.split(":),")
            for values in items_lists:
                code, name, qty, price, total_price = ['', '', '', "",0]
                item = values.split(":,:")
                if len(item) == 11:
                    #print("there is id :")
                    #for each items
                    id = item[0].replace("(:", "")
                    code = item[1]
                    bar = item[2]
                    name = item[3]
                    # if item shop and sold shop not same
                    shop = item[4]
                    color = item[5]
                    size = item[6]
                    qty = item[7]
                    price = item[8]
                    total_price = float(qty)*float(price)
                    QTY += float(qty)
                    PRICE += float(total_price)
                    disc = item[9]
                    Disc += float(disc)
                    tax = item[10].replace(":)", "")
                    TAX += float(tax)
                    v.append([str(code), str(name), str(qty), str(price), str(total_price)])
                    #print("list | " + str([code, name, qty, price, total_price]))
                elif len(item) == 10:
                    #print("no id :")
                    #for each items
                    id = item[0].replace("(:", "")
                    code = item[1].replace("(:", "")
                    name = item[2]
                    # if item shop and sold shop not same
                    shop = item[3]
                    color = item[4]
                    size = item[5]
                    qty = item[6]
                    price = item[7]
                    total_price = float(qty)*float(price)
                    QTY += float(qty)
                    PRICE += float(total_price)
                    disc = item[8]
                    Disc += float(disc)
                    tax = item[9].replace(":)", "")
                    TAX += float(tax)
                    v.append([str(code), str(name), str(qty), str(price), str(total_price)])
                    #print("list | " + str([code, name, qty, price, total_price]))
        # Code   : Name      : qty : price  : totale :
        # TODO make equal space
        itemforslip = ""
        #print("v : " + str(v))
        for vs in v:
            vl = [7, 10, 3, 8, 8]
            vsy = ['/', '(', 'x', '=', ')']
            vvi = 0
            for vi in vl:
                for w in range(vi):
                    if w < len(vs[vvi]):
                        #print("vs[] : " + str(vs[vvi])+ " vvi :" + str(vvi) + " w :" + str(w))
                        itemforslip += vs[vvi][w]
                    else:
                        itemforslip += ' '
                itemforslip += vsy[vvi]
                vvi += 1
            itemforslip += "\n_________________________________________\n"
            
        slip += "Code    Name       qty  price    totale \n" \
                "_________________________________________\n" \
                + itemforslip 
        
        taxstr = ""
        if TAX == 0:
            taxstr = "5%"
        else:
            taxstr = str(TAX)
        
        slip_payments = ""
        #print("payment : " + str(doc['payments']))
        '''if ")" in doc['payments'] or ")," in doc['payments']:
            items_lists = (doc['payments'] + ",").split("),")
            index = 0
            for p in range(len(items_lists)-1):
                item = items_lists[p].split(",")
                #print("item ;" + str(item))
                #for each items+
                pay_id = item[0].replace("(", "")
                pay_type = item[1]
                pay_pid = item[2]
                pay_pid_date = item[3].replace(",", "")
                pay_updated_date = item[4].replace(",", "")
                pay_user = item[5].replace(",", "")
                price = item[1]
                slip_payments += str(pay_id) + ". " + str(pay_type) + ", " +  str(pay_pid) + ", " + pay_pid_date.split()[0] + ", " + pay_user + "\n"
                index += 1   
        elif "," in doc['payments']:
            items_lists = doc['payments'].split(",")
            index = 0
            for p in range(len(items_lists)-1):
                item = items_lists[p].split(" = ")
                #print("item :" + str(item))
                #for each items
                name = item[0].replace("(:", "")
                price = item[1]
                slip_payments += str(index) + ". " + str(name) + ", " +  str(price) + ", " + doc['doc_expire_date'].split()[0] + ", " + doc['extension_barcode'] + "\n"
                index += 1  
        else:
            item = doc['payments'].split(" = ")
            #print("item :" + str(item))
            if len(item) >= 2:
                name = item[0].replace("(:", "")
                price = item[1]
                slip_payments += "0. " + str(name) + ", " +  str(price) + ", " + doc['doc_expire_date'].split()[0] + ", " + doc['extension_barcode'] + "\n"
        '''
        slip += str(slip_payments) + "\n" + \
                "=========================================\n"
        
        pvv = [str(QTY), str(PRICE), str(taxstr), str(Disc), str(0), str(0)]
        if doc['pid']:
            pvv = [str(QTY), str(PRICE), str(taxstr), str(Disc), str(float(doc['pid'])), str(str(float(doc['pid'])-(PRICE-Disc)-TAX))]
        pvvi = 0
        totalitemforslip = ""
        pv = [3, 7, 3, 8, 6, 8]
        vsy = [' ', '-', '-', ' ', '=', '']
        for pvi in pv:
            for w in range(pvi):
                if w < len(pvv[pvvi]):
                    #print("pvv : " + str(pvv[pvvi])+ " pvvi :" + str(pvvi) + " w :" + str(w))
                    totalitemforslip += pvv[pvvi][w]
                else:
                    totalitemforslip += ' '
            totalitemforslip += vsy[pvvi]
            pvvi += 1
        totalitemforslip += "\n"
        
        slip += "QTY  Price  Tax  Discount  Paid  CHANGE\n" \
                + str(totalitemforslip) + "\n"\
            "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n" \
            "1. NO REFUNDS AT ALL EXCHANGE IN 7 DAYS \n" \
            "2. FOR HYGIENIC REASONS, NO REFUNDS OR\n" \
            "   EXCHANGES ON UNDERWEAR AND SOCKS\n" \
            "3. PLEASE PRESENT THIS SLIP TO CALIDATE \n" \
            "   YOUR GUARNTEE\n" \
            "       THANK YOU FOR SHOPING WITH US     \n" \
            "          " + str(doc['doc_barcode']) + "       \n"
    if preview_mode and receipt_sections is not None:
        footer = receipt_sections.get("_footer", footer)
        footer = footer.replace(
            "PREVIEW", str(doc.get("doc_barcode") or "PREVIEW"),
        )
    return slip + footer
