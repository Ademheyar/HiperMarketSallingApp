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
