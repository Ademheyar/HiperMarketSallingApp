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

def find_user(v):
    it = None
    if v and v.isdigit():
        it = fetch_as_dict_list("SELECT * FROM users WHERE User_id=?", (v,))
    elif  v:
        it = fetch_as_dict_list("SELECT * FROM users WHERE User_name=?", (v,))
    if it:
        return it[0]
    
def find_shop(id):
    results = fetch_as_dict_list("SELECT * FROM Shops WHERE Shop_id=?", (id,))[0]
    print("found shop ", results)
    return results

def add_text_(width, value):
    ret = ""
    i = 0
    for l in value:
        ret += l
        i+=1
    return [ret]
    
def add_ltext_(width, value):
    ret = ""
    i = 0
    for l in value:
        ret += l
        i+=1
        if i == int(width):
           break
    return [ret]
    
def get_sparet_2(doc, width, pvv, user, shop):
    ret = ""
    for i in range(int(width)):
        ret += "_"
    return [ret + "\n"]

def get_location(doc, width, pvv, user, shop):
    v = shop['Shop_location']
    ret = ""
    if v and "+" in v:
        location = v.split("+")
        for l in location:
            ret += add_ltext_(width, l)[0] + "\n"
    elif v:
        ret += add_ltext_(width, v)[0]
    return [ret + "\n"]

def get_Linkes(doc, width, pvv, user, shop):
    v = shop['Shop_about']
    ret = ""
    if v and "+" in v:
        Shop_about = v.split("+")
        for l in Shop_about:
            ret += add_ltext_(width, l)[0] + "\n"
    elif v:
        ret += add_ltext_(width, v)[0]
    return [ret]

def get_Phone_No(doc, width, pvv, user, shop):
    v = "" # shop['Shop_phone_num'] TODO : get phone number
    ret = ""
    if v and "+" in v:
        location = v.split("+")
        for l in location:
            ret +=  add_ltext_(width, l)[0] + "\n"
    elif v:
        ret +=  add_ltext_(width, v)[0]
        return [ret]

def get_Receipt_no(doc, width, pvv, user, shop):
    return ["Receipt No : " + str(doc['doc_barcode']) + "\n"]

def get_extnsion_Receipt_no(doc, width, pvv, user, shop):
    if not str(doc['extension_barcode']) == 'extension_barcode':
        return ["extnsion Receipt No :  " + str(doc['extension_barcode']) + "\n"]
           
def get_date(doc, width, pvv, user, shop):
    return ["Date :  " + str(doc['doc_created_date']) + "\n"]
           
def get_updated_date(doc, width, pvv, user, shop):
    if not str(doc['doc_created_date']) == str(doc['doc_updated_date']):
        return ["updated Date :  " + str(doc['doc_updated_date']) + "\n"]
           
def get_Due_date(doc, width, pvv, user, shop):
    if not str(doc['doc_created_date']) == str(doc['doc_expire_date']):
        return ["Due Date :  " + str(doc['doc_expire_date']) + "\n"]

def get_user(doc, width, pvv, user, shop):
    slip =""
    # get user and custemusr infor
    it = find_user(doc['user_id'])
    if it:
        #print("it c: " + str(it))   
        slip += "User : "+ str(it['User_name']) +"\n"
    return [slip]

def get_seller(doc, width, pvv, user, shop):
    slip = ""
    # get Seller info    if len(doc) > 16 and doc['Seller_id'] and doc['Seller_id'] != "":
    it = find_user(doc['Seller_id'])
    if it:
        #print("it c: " + str(it))   
        slip += "Seller : "+ str(it['User_name']) +"\n"
    return [slip]
            
def get_customer(doc, width, pvv, user, shop):
    slip = ""
    # get custemur info
    if doc['customer_id'] != "":
        it = find_user(doc['customer_id'])
        if it:
            #print("it c: " + str(it))   
            slip += "Customer : "+ str(it['User_name']) +"\n"\
                    "Phone No : "+ str(it['User_phone_num']) +"\n"
    return [slip]

shop, color, size, PRICE, QTY, Disc, TAX, payments, taxstr = \
    ["", "", "", 0, 0, 0, 0, "", ""]
def get_items(doc, width, pvv, user, shop):
    # get items
    #print("load_slip items : " + str(doc['item']))
    slip = ""
    shop, color, size, PRICE, QTY, Disc, TAX, payments = \
    ["", "", "", 0, 0, 0, 0, ""]
    v = []
    items_lists = str(doc['item'])
    list_items_copy = json.loads(items_lists)
    T_price = 0
    for iv in list_items_copy:
        print("load_slip items iv: " + str(iv))
        # id, code, bar, name, shop, color, size, qty, price, disc, T_price = iv
        QTY += float(iv[7])
        total_price = float(iv[7])*float(iv[8])
        T_price += total_price
        PRICE += float(total_price)
        Disc += float(iv[9])
        TAX += float(0)
        v.append([str(iv[1]), str(iv[3]), str(iv[7]), str(iv[8]), str(total_price)])
    # Code   : Name      : qty : price  : totale :
    # TODO make equal space
    itemforslip = ""
    #print("v : " + str(v))
    vsl = [4, 4, 3, 4, 4]
    tw=21
    width = int(width)
    while not (tw+5 > width-3 and tw+5 < width+3):
        if tw+5 < width:
            vsl = [vsl[0]+2, vsl[1]+3, vsl[2]+0, vsl[3]+1, vsl[4]+1]
            tw += 7
        elif tw+5 > width:
            vsl = [vsl[0]-1, vsl[1]-1, vsl[2], vsl[3]-1, vsl[4]-1]
            tw -= 4
    for vs in v:
        vl = vsl
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
        itemforslip += "\n"
    
    itemcolumnsforslip = ""
    #print("v : " + str(v))
    vi = 0
    vs = ["Code", "Name", "qty", "price", "Totale"] #21 letters + 5 spaces + 5 Blockes = 31
    von = 0
    won = 0 
    for wid in range(int(width)):
        if von >= len(vs):
            itemcolumnsforslip += " "
            continue
            
        if won < vsl[von]:
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
    slip += get_sparet_2(doc, width, pvv, user, shop)[0]
    slip += itemforslip + "\n"
    infos_needed = ["TOTAL QTY", "TOTAL Price", "TOTAL Tax", "TOTAL Discount", "Recived", "Balance"]
    #, "CHANGE"
    given_info = []
    totalitemforslip = ""
    pvv = [QTY, PRICE, TAX, Disc, T_price]
    if len(pvv) == 5:
        if doc['pid']:
            pvv = [str(pvv[0]), str(pvv[1]), str(pvv[2]), str(pvv[3]), str(float(doc['pid'])), "0"]
            # , str(str(float(doc['pid'])-(PRICE-Disc)))
        else:
            pvv = [str(pvv[0]), str(pvv[1]), str(pvv[2]), str(pvv[3]), str(float(pvv[4])), str(float(pvv[4]))]

    done_inserting = 0
    infos_need_on = -1
    payment_on = -1
    hafe_width = int(width)//2
    list_payment_copy = json.loads(doc['payments'])
    
    while(infos_need_on < len(pvv)):
        fwon = 0
        fw = 0
        swon = 0
        for wid in range(int(width)):
            if done_inserting == 0:
                intesd = infos_need_on+1
                while intesd < len(pvv) and (pvv[intesd] == '0' or pvv[intesd] == '0.0'):
                    intesd += 1
                
                if intesd < len(pvv):
                    totalitemforslip += "_" 
                else:
                    break
            elif wid < hafe_width:
                if payment_on < len(list_payment_copy):
                    price = list_payment_copy[payment_on][1]
                    F = str(list_payment_copy[payment_on][1]) + ", " +  str(list_payment_copy[payment_on][0])+ " " + list_payment_copy[payment_on][5]
                    S = list_payment_copy[payment_on][3]+ ", " # pay_updated_date.split()[0] + ", " 
                    if fw < len(F):
                        totalitemforslip += F[fw]
                        fw +=1
                    else:
                        totalitemforslip += " "
                else:
                    totalitemforslip += " "
            else:
                if wid == hafe_width + (hafe_width/2):
                    totalitemforslip += "|"
                elif(wid < hafe_width + (hafe_width//2) and fwon < len(infos_needed[infos_need_on])):
                    totalitemforslip += infos_needed[infos_need_on][fwon]
                    fwon +=1
                elif(wid > hafe_width + (hafe_width//2) and swon < len(pvv[infos_need_on])):
                    totalitemforslip += pvv[infos_need_on][swon]
                    swon +=1
                else:
                    totalitemforslip += " "
            
        if done_inserting == 0:
            done_inserting = 1
            infos_need_on += 1
            while infos_need_on < len(pvv) and (pvv[infos_need_on] == '0' or pvv[infos_need_on] == '0.0'):
                infos_need_on += 1
            payment_on += 1
            if infos_need_on < len(pvv):
                totalitemforslip += "\n" 
        else:
            totalitemforslip += "\n" 
            done_inserting = 0
            
    slip += totalitemforslip + "\n"
    return [slip, [QTY, PRICE, Disc, TAX, T_price]]
    
def get_payments(doc, width, pvv, user, shop):
    slip = ""
    return [slip]

def get_total(doc, width, pvv, user, shop):
    slip = ""
    return [slip]

import string

def get_Rules(doc, width, pvv, user, shop):
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
        ret += v
    return [ret]

def get_sparet(doc, width, pvv, user, shop):
    ret = ""
    for i in range(int(width)):
        ret += "*"
    return [ret + "\n"]

def get_sparet_0(doc, width, pvv, user, shop):
    ret = ""
    for i in range(int(width)):
        ret += "#"
    return [ret + "\n"]

def get_sparet_1(doc, width, pvv, user, shop):
    ret = ""
    for i in range(int(width)):
        ret += "-"
    return [ret + "\n"]



def get_sparet_3(doc, width, pvv, user, shop):
    ret = ""
    for i in range(int(width)):
        ret += "="
    return [ret + "\n"]

def get_sparet_4(doc, width, pvv, user, shop):
    ret = ""
    for i in range(int(width)):
        ret += "~"
    return [ret + "\n"]

slip_order_type=[get_sparet, get_sparet_0, get_sparet_1, get_sparet_2, get_sparet_3, get_sparet_4, get_location, get_Linkes, get_Phone_No, get_Receipt_no, get_extnsion_Receipt_no, get_date, get_updated_date, get_Due_date, get_user, get_seller, get_customer, get_items, get_Rules]

import json
import ast

def load_slip(doc, d_id):
    print("doc : "+str(doc))
    user = find_user(doc['user_id'])
    print("User : ", user)
    at_shop = find_shop(doc['At_Shop_Id'])
    print("User : ", at_shop)

    slip = ""
    if at_shop and at_shop['Shop_Slip_Settings']:
        sittings = json.loads(at_shop['Shop_Slip_Settings'])
        print("sittings : "+str(sittings))
        width = sittings[0][0]
        hight = sittings[0][1]
        orders = sittings[1]
        # Make shouer that user shop is same as viewing admin
        print("width : "+str(width))
        print("order : "+str(orders))
        print("shop : "+str(at_shop))
        pvv = []
        for order in orders:
            if order != "":
                ret = slip_order_type[int(order[0])](doc, width, pvv, user, at_shop)
                if ret:
                    if len(ret) == 1:
                        slip += ret[0]
                    elif len(ret) == 2:
                        slip += ret[0]
                        pvv = ret[1]
        slip += "   THANK YOU FOR SHOPING WITH US     \n" \
                "          " + str(doc['doc_barcode']) + "       \n"

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
        it = find_user(doc['user_id'])
        if it:
            print("it c: " + str(it))   
            slip += "User : "+ str(it['User_name']) +"\n"
        
        # get Seller info    if len(doc) > 16 and doc['Seller_id'] and doc['Seller_id'] != "":
        it = find_user(doc['Seller_id'])
        if it:
            #print("it c: " + str(it))   
            slip += "Seller : "+ str(it['User_name']) +"\n"
                
                
        # get custemur info
        if doc['customer_id'] != "":
            it = find_user(doc['customer_id'])
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
    return slip
