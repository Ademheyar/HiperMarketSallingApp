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
conn = sqlite3.connect(db_path)
cursor = conn.cursor()


def load_slip(doc, d_id):
    #get informations
<<<<<<< HEAD
=======
    #print("doc in lload slip = " + str(doc))
>>>>>>> db9ae79 (adding seller)
    slip = "             MAMS MALL                   \n"\
           "    INFRONT OF PNP CLOTHING AND MR.PRICE \n"\
           "*****************************************\n" \
           "JOIN SOCIAL MIDEIA FOR NEW ARRIVALS \n" \
           "WITH SPCIAL DISCOUN                 \n" \
           "INSTAGRAM   : @ADOTOUTFIT\n" \
           "WEBSITE     : http://adot.unaux.com\n" \
           "WHATS UP    : MESSAGE AS ON\n" \
<<<<<<< HEAD
           "     +276 12231 353 OR +276 52699 508   \n" \
           "*****************************************\n" 
    #get doc information
    slip += "Receipt No : " + str(doc[0]) + "\n"\
            "extnsion Receipt No :  " + str(doc[1]) + "\n"\
            "Date :  " + str(doc[11]) + "\n"\
            "updated Date :  " + str(doc[13]) + "\n"\
            "Due Date :  " + str(doc[12]) + "\n"\
            "-----------------------------------------\n" 
    # get user and custemusr infor
    slip += "User : " + str(doc[2]) + "\n"
    
            
    # get custemur info
    if doc[3] != "":
        cursor.execute("SELECT * FROM users WHERE id=?", (doc[3],))
        it = cursor.fetchone()
        print("it c: " + str(it))   
        slip += "Customer : "+ str(it[1]) +"\n"\
                "Phone No : "+ str(it[4]) +"\n"
    slip += "-----------------------------------------\n"

    # get items
    print("load_slip items : " + str(doc[5]))
    shop, color, size, PRICE, QTY, Disc, TAX, payments = \
    ["", "", "", 0, 0, 0, 0, ""]
    v = []
    items_ = str(doc[5]) + ","
    items_lists = items_.split("|),")
    if ":)," in items_:
        print("spliting by :")
=======
           "     +276 12231 353 \n" \
           "*****************************************\n" 
    #get doc information
    slip += "Receipt No : " + str(doc[1]) + "\n"\
            "extnsion Receipt No :  " + str(doc[2]) + "\n"\
            "Date :  " + str(doc[12]) + "\n"\
            "updated Date :  " + str(doc[14]) + "\n"\
            "Due Date :  " + str(doc[13]) + "\n"\
            "------------------------------------------\n" 
    # get user and custemusr infor
    slip += "User : " + str(doc[3]) + "\n"
    
            
    # get custemur info
    if doc[4] != "":
        it = cursor.execute("SELECT * FROM users WHERE User_id=?", (doc[4],)).fetchone()
        if it:
            #print("it c: " + str(it))   
            slip += "Customer : "+ str(it[3]) +"\n"\
                    "Phone No : "+ str(it[6]) +"\n"
    slip += "------------------------------------------\n"

    # get items
    #print("load_slip items : " + str(doc[6]))
    shop, color, size, PRICE, QTY, Disc, TAX, payments = \
    ["", "", "", 0, 0, 0, 0, ""]
    v = []
    items_ = str(doc[6]) + ","
    items_lists = items_.split("|),")
    if ":)," in items_:
        #print("spliting by :")
>>>>>>> db9ae79 (adding seller)
        items_lists = items_.split(":),")
        for values in items_lists:
            code, name, qty, price, total_price = ['', '', '', "",0]
            item = values.split(":,:")
            if len(item) == 11:
<<<<<<< HEAD
                print("there is id :")
=======
                #print("there is id :")
>>>>>>> db9ae79 (adding seller)
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
<<<<<<< HEAD
                print("list | " + str([code, name, qty, price, total_price]))
            elif len(item) == 10:
                print("no id :")
=======
                #print("list | " + str([code, name, qty, price, total_price]))
            elif len(item) == 10:
                #print("no id :")
>>>>>>> db9ae79 (adding seller)
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
<<<<<<< HEAD
                print("list | " + str([code, name, qty, price, total_price]))
    # Code   : Name      : qty : price  : totale :
    # TODO make equal space
    itemforslip = ""
    print("v : " + str(v))
    for vs in v:
        vl = [7, 10, 3, 8, 8]
=======
                #print("list | " + str([code, name, qty, price, total_price]))
    # Code   : Name      : qty : price  : totale :
    # TODO make equal space
    itemforslip = ""
    #print("v : " + str(v))
    for vs in v:
        vl = [7, 10, 3, 8, 8]
        vsy = ['/', '(', 'x', '=', ')']
>>>>>>> db9ae79 (adding seller)
        vvi = 0
        for vi in vl:
            for w in range(vi):
                if w < len(vs[vvi]):
<<<<<<< HEAD
                    print("vs[] : " + str(vs[vvi])+ " vvi :" + str(vvi) + " w :" + str(w))
                    itemforslip += vs[vvi][w]
                else:
                    itemforslip += ' '
            vvi += 1
            itemforslip += "|"
        itemforslip += "\n"
    slip += "Code   |Name      |qty| price  |totale  |\n" \
            + itemforslip + \
            "=========================================\n"
    
    pv = [3, 4, 3, 8, 8, 8]
    taxstr = ""
    if TAX == 0:
        taxstr = "10%"
    else:
        taxstr = str(TAX)
    pvv = [str(QTY), str(Disc), str(taxstr), str(PRICE), str(PRICE), str(str(0))]
    pvvi = 0
    totalitemforslip = ""
    for pvi in pv:
        for w in range(pvi):
            if w < len(pvv[pvvi]):
                print("pvv : " + str(pvv[pvvi])+ " pvvi :" + str(pvvi) + " w :" + str(w))
                totalitemforslip += pvv[pvvi][w]
            else:
                totalitemforslip += ' '
        pvvi += 1
        totalitemforslip += "|"
    totalitemforslip += "\n"
    slip += "QTY|Disc|Tax| Price  |  Paid  |CHANGE   |\n" \
            + str(totalitemforslip) + "\n"
    slip_payments = ""
    print("payment : " + str(doc[10]))
    if ")" in doc[10] or ")," in doc[10]:
        items_lists = (doc[10] + ",").split("),")
        index = 0
        for p in range(len(items_lists)-1):
            item = items_lists[p].split(",")
            print("item ;" + str(item))
=======
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
    #print("payment : " + str(doc[11]))
    if ")" in doc[11] or ")," in doc[11]:
        items_lists = (doc[11] + ",").split("),")
        index = 0
        for p in range(len(items_lists)-1):
            item = items_lists[p].split(",")
            #print("item ;" + str(item))
>>>>>>> db9ae79 (adding seller)
            #for each items+
            pay_id = item[0].replace("(", "")
            pay_type = item[1]
            pay_pid = item[2]
            pay_pid_date = item[3].replace(",", "")
            pay_updated_date = item[4].replace(",", "")
            pay_user = item[5].replace(",", "")
            price = item[1]
<<<<<<< HEAD
            slip_payments += str(pay_id) + ". " + str(pay_type) + ", " +  str(pay_pid) + ", " + pay_updated_date + ", " + pay_user + "\n"
            index += 1   
    elif "," in doc[10]:
        items_lists = doc[10].split(",")
        index = 0
        for p in range(len(items_lists)-1):
            item = items_lists[p].split(" = ")
            print("item :" + str(item))
            #for each items
            name = item[0].replace("(:", "")
            price = item[1]
            slip_payments += str(index) + ". " + str(name) + ", " +  str(price) + ", " + doc[13] + ", " + doc[2] + "\n"
            index += 1  
    else:
        item = doc[10].split(" = ")
        print("item :" + str(item))
        name = item[0].replace("(:", "")
        price = item[1]
        slip_payments += "0. " + str(name) + ", " +  str(price) + ", " + doc[13] + ", " + doc[2] + "\n"

    slip += str(slip_payments) + "\n" \
=======
            slip_payments += str(pay_id) + ". " + str(pay_type) + ", " +  str(pay_pid) + ", " + pay_pid_date.split()[0] + ", " + pay_user + "\n"
            index += 1   
    elif "," in doc[11]:
        items_lists = doc[11].split(",")
        index = 0
        for p in range(len(items_lists)-1):
            item = items_lists[p].split(" = ")
            #print("item :" + str(item))
            #for each items
            name = item[0].replace("(:", "")
            price = item[1]
            slip_payments += str(index) + ". " + str(name) + ", " +  str(price) + ", " + doc[13].split()[0] + ", " + doc[2] + "\n"
            index += 1  
    else:
        item = doc[11].split(" = ")
        #print("item :" + str(item))
        if len(item) >= 2:
            name = item[0].replace("(:", "")
            price = item[1]
            slip_payments += "0. " + str(name) + ", " +  str(price) + ", " + doc[13].split()[0] + ", " + doc[2] + "\n"

    slip += str(slip_payments) + "\n" + \
            "=========================================\n"
    
    pvv = [str(QTY), str(PRICE), str(taxstr), str(Disc), str(0), str(0)]
    if doc[15]:
        pvv = [str(QTY), str(PRICE), str(taxstr), str(Disc), str(float(doc[15])), str(str(float(doc[15])-(PRICE-Disc)-TAX))]
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
>>>>>>> db9ae79 (adding seller)
        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n" \
        "1. NO REFUNDS AT ALL EXCHANGE IN 7 DAYS \n" \
        "2. FOR HYGIENIC REASONS, NO REFUNDS OR\n" \
        "   EXCHANGES ON UNDERWEAR AND SOCKS\n" \
        "3. PLEASE PRESENT THIS SLIP TO CALIDATE \n" \
        "   YOUR GUARNTEE\n" \
        "       THANK YOU FOR SHOPING WITH US     \n" \
<<<<<<< HEAD
        "          " + str(doc[0]) + "       \n"
=======
        "          " + str(doc[1]) + "       \n"
>>>>>>> db9ae79 (adding seller)
    return slip
