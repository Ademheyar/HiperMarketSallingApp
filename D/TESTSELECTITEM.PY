a ='a'
itmes = [['a', 9], ['b', 4], ['q', 3], ['a', 3]] 
olditems = list(itmes)

for olditem in olditems:
    # [id, code, name, shop, color, size, qty, price]
    if olditem[0] == a:
        if olditem[1] == 9:
           olditem[1] = "6"
        elif olditem[1] == 3:
           olditem[1] = 0
print("items :" + str(itmes))
print("new olditems :" + str(olditems))
