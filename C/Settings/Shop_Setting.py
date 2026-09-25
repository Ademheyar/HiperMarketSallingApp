import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk, filedialog
import os, shutil
import sqlite3
import shutil
import datetime
import atexit
import sys
import json
import ast


current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(os.path.join(current_dir, '..'), '..')
sys.path.append(MAIN_dir)

data_dir = os.path.abspath(os.path.join(MAIN_dir, 'data'))
db_path = os.path.join(data_dir, 'my_database.db')
from D.Getdefsize import ButtonEntryApp
from C.List import *
from D.printer import *
from D.GetVALUE import GetvalueForm
# Connect to the database or create it if it does not exist

from C.List import *
from D.Getdate import GetDateForm
from D.Chart.Chart import *

from C.Product.selecttype import *

from C.Settings.Shop_Expenses import *
from C.Settings.Shop_Workers import *

from C.API.Get import *
from C.API.API import *
from C.API.Set import *

Shop_deff_type = [["MANS",[
                    ["ACCESSORIES",[
                        ["BAG",[
                            ["BACKPACK BAG", []],
                            ["DUFFLE BAG", []],
                            ["LAPTOP BAG", []],
                            ["WALLET BAG", []],
                            ["BELT BAG", []],
                            ["HAND BAG", []],
                            ["TOTE", []],
                            ["CLUTCH BAG", []],
                            ["CROSSBODY", []]
                        ]],
                        ["JEWELRY",[
                            ["WATCH", []],
                            ["BRACELET", []],
                            ["RING", []],
                            ["CUFFLINKS", []],
                            ["EARING", []],
                            ["NECKLACE", []],
                            ["ANKLET", []]
                        ]],
                        ["HEADWEAR", [
                            ["CAP", []],
                            ["HAT", []],
                            ["BEANIE", []],
                            ["DURAG", []],
                            ["HIJAB", []],
                            ["SCARF", []],
                            ["HEADBAND", []]
                        ]],
                        ["EYEWEAR", [
                            ["SUNGLASSES", []],
                            ["GLASSES", []],
                            ["EYELASH", []],
                            ["EYELANCE", []]
                        ]],
                        ["BELT", []],
                        ["HAIR ACCESSORIES", []],
                        ["OTHERS", [
                            ["SOCKS", []],
                            ["GLOVES", []],
                            ["SHOELACE", []],
                            ["TIE", []],
                            ["BOWTIE", []],
                            ["SHAWL", []],
                            ["TIGHTS", []]
                        ]],
                    ]],
                    ["SHOES", [
                        ["CASUAL", [
                            ["SNEAKERS", []],
                            ["LOAFERS", []],
                            ["FLATS", []],
                            ["SANDALS", []]
                        ]],
                        ["FORMAL", [
                            ["OXFORD", []],
                            ["DERBY", []],
                            ["SUIT SHOES", []],
                            ["HEELS", []],
                            ["PUMPS", []],
                            ["WEDGES", []]
                        ]],
                        ["SPORT SHOES", [
                            ["RUNNING SHOES", []],
                            ["TRAINING SHOES", []]
                        ]],
                        ["BOOTS", [
                            ["CHELSEA", []],
                            ["COMBAT", []],
                            ["WORK BOOTS", []],
                            ["ANKLE BOOTS", []],
                            ["KNEE HIGH BOOTS", []],
                            ["FORMAL BOOTS", []]
                        ]]
                    ]],
                    ["TOP", [
                        ["T-SHIRT", []],
                        ["SHIRT", []],
                        ["BLOUSES", []],
                        ["POLO SHIRT", []],
                        ["TANK", []],
                        ["SWEATER", []],
                        ["HOODIES", []],
                        ["JACKET", []],
                        ["BLAZER", []],
                        ["CROP TOP", []]
                    ]],
                    ["BOTTOM", [
                        ["JEAN", []],
                        ["PANT", []],
                        ["SHORT", []],
                        ["SKIRT", []],
                        ["LEGGING", []],
                        ["CULOTTE", []],
                        ["CHINOS", []],
                        ["TROUSERS", []],
                        ["SUIT PANT", []],
                        ["JOGGERS", []],
                        ["PALAZZO", []]
                    ]],
                    ["OUTERWEAR", [
                        ["COAT", []],
                        ["TRENCH COAT", []],
                        ["PARKA", []],
                        ["WINDBREAKER", []],
                        ["LEZER JACKET", []],
                        ["RIN COAT JACKET", []],
                        ["BOMBER JACKET", []],
                        ["CARDIGAN", []],
                        ["DENIM JACKET", []]
                    ]],
                    ["ACTIVEWEAR", [
                        ["ATHLETICSHORTS", []],
                        ["JOGGINGPANT", []],
                        ["SPORTJACKET", []],
                        ["YOGAPANT", []],
                        ["PREFORMANCETOP", []]
                    ]],
                    ["TRADITIONAL", [
                        ["KURTA", []],
                        ["SHERWANI", []],
                        ["THOBE", []],
                        ["KURTI", []],
                        ["SAREE", []],
                        ["HIJAB DRESS", []],
                        ["ABAYA", []],
                        ["KAFTAN", []]
                    ]],
                    ["DRESS", [
                        ["CASUAL DRESS", []],
                        ["MAXI DRESS", []],
                        ["EVENING DRESS", []],
                        ["SUMMER DRESS", []],
                        ["ABAYA DRESS", []]
                    ]]
                ]], 
                ["WOMANS", [["ACCESSORIES",[
                        ["BAG",[
                            ["BACKPACK BAG", []],
                            ["DUFFLE BAG", []],
                            ["LAPTOP BAG", []],
                            ["WALLET BAG", []],
                            ["BELT BAG", []],
                            ["HAND BAG", []],
                            ["TOTE", []],
                            ["CLUTCH BAG", []],
                            ["CROSSBODY", []]
                        ]],
                        ["JEWELRY",[
                            ["WATCH", []],
                            ["BRACELET", []],
                            ["RING", []],
                            ["CUFFLINKS", []],
                            ["EARING", []],
                            ["NECKLACE", []],
                            ["ANKLET", []]
                        ]],
                        ["HEADWEAR", [
                            ["CAP", []],
                            ["HAT", []],
                            ["BEANIE", []],
                            ["DURAG", []],
                            ["HIJAB", []],
                            ["SCARF", []],
                            ["HEADBAND", []]
                        ]],
                        ["EYEWEAR", [
                            ["SUNGLASSES", []],
                            ["GLASSES", []],
                            ["EYELASH", []],
                            ["EYELANCE", []]
                        ]],
                        ["BELT", []],
                        ["HAIR ACCESSORIES", []],
                        ["OTHERS", [
                            ["SOCKS", []],
                            ["GLOVES", []],
                            ["SHOELACE", []],
                            ["TIE", []],
                            ["BOWTIE", []],
                            ["SHAWL", []],
                            ["TIGHTS", []]
                        ]],
                    ]],
                    ["SHOES", [
                        ["CASUAL", [
                            ["SNEAKERS", []],
                            ["LOAFERS", []],
                            ["FLATS", []],
                            ["SANDALS", []]
                        ]],
                        ["FORMAL", [
                            ["OXFORD", []],
                            ["DERBY", []],
                            ["SUIT SHOES", []],
                            ["HEELS", []],
                            ["PUMPS", []],
                            ["WEDGES", []]
                        ]],
                        ["SPORT SHOES", [
                            ["RUNNING SHOES", []],
                            ["TRAINING SHOES", []]
                        ]],
                        ["BOOTS", [
                            ["CHELSEA", []],
                            ["COMBAT", []],
                            ["WORK BOOTS", []],
                            ["ANKLE BOOTS", []],
                            ["KNEE HIGH BOOTS", []],
                            ["FORMAL BOOTS", []]
                        ]]
                    ]],
                    ["TOP", [
                        ["T-SHIRT", []],
                        ["SHIRT", []],
                        ["BLOUSES", []],
                        ["POLO SHIRT", []],
                        ["TANK", []],
                        ["SWEATER", []],
                        ["HOODIES", []],
                        ["JACKET", []],
                        ["BLAZER", []],
                        ["CROP TOP", []]
                    ]],
                    ["BOTTOM", [
                        ["JEAN", []],
                        ["PANT", []],
                        ["SHORT", []],
                        ["SKIRT", []],
                        ["LEGGING", []],
                        ["CULOTTE", []],
                        ["CHINOS", []],
                        ["TROUSERS", []],
                        ["SUIT PANT", []],
                        ["JOGGERS", []],
                        ["PALAZZO", []]
                    ]],
                    ["OUTERWEAR", [
                        ["COAT", []],
                        ["TRENCH COAT", []],
                        ["PARKA", []],
                        ["WINDBREAKER", []],
                        ["LEZER JACKET", []],
                        ["RIN COAT JACKET", []],
                        ["BOMBER JACKET", []],
                        ["CARDIGAN", []],
                        ["DENIM JACKET", []]
                    ]],
                    ["ACTIVEWEAR", [
                        ["ATHLETICSHORTS", []],
                        ["JOGGINGPANT", []],
                        ["SPORTJACKET", []],
                        ["YOGAPANT", []],
                        ["PREFORMANCETOP", []]
                    ]],
                    ["TRADITIONAL", [
                        ["KURTA", []],
                        ["SHERWANI", []],
                        ["THOBE", []],
                        ["KURTI", []],
                        ["SAREE", []],
                        ["HIJAB DRESS", []],
                        ["ABAYA", []],
                        ["KAFTAN", []]
                    ]],
                    ["DRESS", [
                        ["CASUAL DRESS", []],
                        ["MAXI DRESS", []],
                        ["EVENING DRESS", []],
                        ["SUMMER DRESS", []],
                        ["ABAYA DRESS", []]
                    ]]
                ]],
                ["KIDS", [["GIRLS", [["ACCESSORIES",[
                        ["BAG",[
                            ["BACKPACK BAG", []],
                            ["DUFFLE BAG", []],
                            ["LAPTOP BAG", []],
                            ["WALLET BAG", []],
                            ["BELT BAG", []],
                            ["HAND BAG", []],
                            ["TOTE", []],
                            ["CLUTCH BAG", []],
                            ["CROSSBODY", []]
                        ]],
                        ["JEWELRY",[
                            ["WATCH", []],
                            ["BRACELET", []],
                            ["RING", []],
                            ["CUFFLINKS", []],
                            ["EARING", []],
                            ["NECKLACE", []],
                            ["ANKLET", []]
                        ]],
                        ["HEADWEAR", [
                            ["CAP", []],
                            ["HAT", []],
                            ["BEANIE", []],
                            ["DURAG", []],
                            ["HIJAB", []],
                            ["SCARF", []],
                            ["HEADBAND", []]
                        ]],
                        ["EYEWEAR", [
                            ["SUNGLASSES", []],
                            ["GLASSES", []],
                            ["EYELASH", []],
                            ["EYELANCE", []]
                        ]],
                        ["BELT", []],
                        ["HAIR ACCESSORIES", []],
                        ["OTHERS", [
                            ["SOCKS", []],
                            ["GLOVES", []],
                            ["SHOELACE", []],
                            ["TIE", []],
                            ["BOWTIE", []],
                            ["SHAWL", []],
                            ["TIGHTS", []]
                        ]],
                    ]],
                    ["SHOES", [
                        ["CASUAL", [
                            ["SNEAKERS", []],
                            ["LOAFERS", []],
                            ["FLATS", []],
                            ["SANDALS", []]
                        ]],
                        ["FORMAL", [
                            ["OXFORD", []],
                            ["DERBY", []],
                            ["SUIT SHOES", []],
                            ["HEELS", []],
                            ["PUMPS", []],
                            ["WEDGES", []]
                        ]],
                        ["SPORT SHOES", [
                            ["RUNNING SHOES", []],
                            ["TRAINING SHOES", []]
                        ]],
                        ["BOOTS", [
                            ["CHELSEA", []],
                            ["COMBAT", []],
                            ["WORK BOOTS", []],
                            ["ANKLE BOOTS", []],
                            ["KNEE HIGH BOOTS", []],
                            ["FORMAL BOOTS", []]
                        ]]
                    ]],
                    ["TOP", [
                        ["T-SHIRT", []],
                        ["SHIRT", []],
                        ["BLOUSES", []],
                        ["POLO SHIRT", []],
                        ["TANK", []],
                        ["SWEATER", []],
                        ["HOODIES", []],
                        ["JACKET", []],
                        ["BLAZER", []],
                        ["CROP TOP", []]
                    ]],
                    ["BOTTOM", [
                        ["JEAN", []],
                        ["PANT", []],
                        ["SHORT", []],
                        ["SKIRT", []],
                        ["LEGGING", []],
                        ["CULOTTE", []],
                        ["CHINOS", []],
                        ["TROUSERS", []],
                        ["SUIT PANT", []],
                        ["JOGGERS", []],
                        ["PALAZZO", []]
                    ]],
                    ["OUTERWEAR", [
                        ["COAT", []],
                        ["TRENCH COAT", []],
                        ["PARKA", []],
                        ["WINDBREAKER", []],
                        ["LEZER JACKET", []],
                        ["RIN COAT JACKET", []],
                        ["BOMBER JACKET", []],
                        ["CARDIGAN", []],
                        ["DENIM JACKET", []]
                    ]],
                    ["ACTIVEWEAR", [
                        ["ATHLETICSHORTS", []],
                        ["JOGGINGPANT", []],
                        ["SPORTJACKET", []],
                        ["YOGAPANT", []],
                        ["PREFORMANCETOP", []]
                    ]],
                    ["TRADITIONAL", [
                        ["KURTA", []],
                        ["SHERWANI", []],
                        ["THOBE", []],
                        ["KURTI", []],
                        ["SAREE", []],
                        ["HIJAB DRESS", []],
                        ["ABAYA", []],
                        ["KAFTAN", []]
                    ]],
                    ["DRESS", [
                        ["CASUAL DRESS", []],
                        ["MAXI DRESS", []],
                        ["EVENING DRESS", []],
                        ["SUMMER DRESS", []],
                        ["ABAYA DRESS", []]
                    ]]
                ]],
                ["BOYS", [["ACCESSORIES",[
                        ["BAG",[
                            ["BACKPACK BAG", []],
                            ["DUFFLE BAG", []],
                            ["LAPTOP BAG", []],
                            ["WALLET BAG", []],
                            ["BELT BAG", []],
                            ["HAND BAG", []],
                            ["TOTE", []],
                            ["CLUTCH BAG", []],
                            ["CROSSBODY", []]
                        ]],
                        ["JEWELRY",[
                            ["WATCH", []],
                            ["BRACELET", []],
                            ["RING", []],
                            ["CUFFLINKS", []],
                            ["EARING", []],
                            ["NECKLACE", []],
                            ["ANKLET", []]
                        ]],
                        ["HEADWEAR", [
                            ["CAP", []],
                            ["HAT", []],
                            ["BEANIE", []],
                            ["DURAG", []],
                            ["HIJAB", []],
                            ["SCARF", []],
                            ["HEADBAND", []]
                        ]],
                        ["EYEWEAR", [
                            ["SUNGLASSES", []],
                            ["GLASSES", []],
                            ["EYELASH", []],
                            ["EYELANCE", []]
                        ]],
                        ["BELT", []],
                        ["HAIR ACCESSORIES", []],
                        ["OTHERS", [
                            ["SOCKS", []],
                            ["GLOVES", []],
                            ["SHOELACE", []],
                            ["TIE", []],
                            ["BOWTIE", []],
                            ["SHAWL", []],
                            ["TIGHTS", []]
                        ]],
                    ]],
                    ["SHOES", [
                        ["CASUAL", [
                            ["SNEAKERS", []],
                            ["LOAFERS", []],
                            ["FLATS", []],
                            ["SANDALS", []]
                        ]],
                        ["FORMAL", [
                            ["OXFORD", []],
                            ["DERBY", []],
                            ["SUIT SHOES", []],
                            ["HEELS", []],
                            ["PUMPS", []],
                            ["WEDGES", []]
                        ]],
                        ["SPORT SHOES", [
                            ["RUNNING SHOES", []],
                            ["TRAINING SHOES", []]
                        ]],
                        ["BOOTS", [
                            ["CHELSEA", []],
                            ["COMBAT", []],
                            ["WORK BOOTS", []],
                            ["ANKLE BOOTS", []],
                            ["KNEE HIGH BOOTS", []],
                            ["FORMAL BOOTS", []]
                        ]]
                    ]],
                    ["TOP", [
                        ["T-SHIRT", []],
                        ["SHIRT", []],
                        ["BLOUSES", []],
                        ["POLO SHIRT", []],
                        ["TANK", []],
                        ["SWEATER", []],
                        ["HOODIES", []],
                        ["JACKET", []],
                        ["BLAZER", []],
                        ["CROP TOP", []]
                    ]],
                    ["BOTTOM", [
                        ["JEAN", []],
                        ["PANT", []],
                        ["SHORT", []],
                        ["SKIRT", []],
                        ["LEGGING", []],
                        ["CULOTTE", []],
                        ["CHINOS", []],
                        ["TROUSERS", []],
                        ["SUIT PANT", []],
                        ["JOGGERS", []],
                        ["PALAZZO", []]
                    ]],
                    ["OUTERWEAR", [
                        ["COAT", []],
                        ["TRENCH COAT", []],
                        ["PARKA", []],
                        ["WINDBREAKER", []],
                        ["LEZER JACKET", []],
                        ["RIN COAT JACKET", []],
                        ["BOMBER JACKET", []],
                        ["CARDIGAN", []],
                        ["DENIM JACKET", []]
                    ]],
                    ["ACTIVEWEAR", [
                        ["ATHLETICSHORTS", []],
                        ["JOGGINGPANT", []],
                        ["SPORTJACKET", []],
                        ["YOGAPANT", []],
                        ["PREFORMANCETOP", []]
                    ]],
                    ["TRADITIONAL", [
                        ["KURTA", []],
                        ["SHERWANI", []],
                        ["THOBE", []],
                        ["KURTI", []],
                        ["SAREE", []],
                        ["HIJAB DRESS", []],
                        ["ABAYA", []],
                        ["KAFTAN", []]
                    ]],
                    ["DRESS", [
                        ["CASUAL DRESS", []],
                        ["MAXI DRESS", []],
                        ["EVENING DRESS", []],
                        ["SUMMER DRESS", []],
                        ["ABAYA DRESS", []]
                    ]]
                ]],
                ["FORKIDS", [["ACCESSORIES",[
                        ["BAG",[
                            ["BACKPACK BAG", []],
                            ["DUFFLE BAG", []],
                            ["LAPTOP BAG", []],
                            ["WALLET BAG", []],
                            ["BELT BAG", []],
                            ["HAND BAG", []],
                            ["TOTE", []],
                            ["CLUTCH BAG", []],
                            ["CROSSBODY", []]
                        ]],
                        ["JEWELRY",[
                            ["WATCH", []],
                            ["BRACELET", []],
                            ["RING", []],
                            ["CUFFLINKS", []],
                            ["EARING", []],
                            ["NECKLACE", []],
                            ["ANKLET", []]
                        ]],
                        ["HEADWEAR", [
                            ["CAP", []],
                            ["HAT", []],
                            ["BEANIE", []],
                            ["DURAG", []],
                            ["HIJAB", []],
                            ["SCARF", []],
                            ["HEADBAND", []]
                        ]],
                        ["EYEWEAR", [
                            ["SUNGLASSES", []],
                            ["GLASSES", []],
                            ["EYELASH", []],
                            ["EYELANCE", []]
                        ]],
                        ["BELT", []],
                        ["HAIR ACCESSORIES", []],
                        ["OTHERS", [
                            ["SOCKS", []],
                            ["GLOVES", []],
                            ["SHOELACE", []],
                            ["TIE", []],
                            ["BOWTIE", []],
                            ["SHAWL", []],
                            ["TIGHTS", []]
                        ]],
                    ]],
                    ["SHOES", [
                        ["CASUAL", [
                            ["SNEAKERS", []],
                            ["LOAFERS", []],
                            ["FLATS", []],
                            ["SANDALS", []]
                        ]],
                        ["FORMAL", [
                            ["OXFORD", []],
                            ["DERBY", []],
                            ["SUIT SHOES", []],
                            ["HEELS", []],
                            ["PUMPS", []],
                            ["WEDGES", []]
                        ]],
                        ["SPORT SHOES", [
                            ["RUNNING SHOES", []],
                            ["TRAINING SHOES", []]
                        ]],
                        ["BOOTS", [
                            ["CHELSEA", []],
                            ["COMBAT", []],
                            ["WORK BOOTS", []],
                            ["ANKLE BOOTS", []],
                            ["KNEE HIGH BOOTS", []],
                            ["FORMAL BOOTS", []]
                        ]]
                    ]],
                    ["TOP", [
                        ["T-SHIRT", []],
                        ["SHIRT", []],
                        ["BLOUSES", []],
                        ["POLO SHIRT", []],
                        ["TANK", []],
                        ["SWEATER", []],
                        ["HOODIES", []],
                        ["JACKET", []],
                        ["BLAZER", []],
                        ["CROP TOP", []]
                    ]],
                    ["BOTTOM", [
                        ["JEAN", []],
                        ["PANT", []],
                        ["SHORT", []],
                        ["SKIRT", []],
                        ["LEGGING", []],
                        ["CULOTTE", []],
                        ["CHINOS", []],
                        ["TROUSERS", []],
                        ["SUIT PANT", []],
                        ["JOGGERS", []],
                        ["PALAZZO", []]
                    ]],
                    ["OUTERWEAR", [
                        ["COAT", []],
                        ["TRENCH COAT", []],
                        ["PARKA", []],
                        ["WINDBREAKER", []],
                        ["LEZER JACKET", []],
                        ["RIN COAT JACKET", []],
                        ["BOMBER JACKET", []],
                        ["CARDIGAN", []],
                        ["DENIM JACKET", []]
                    ]],
                    ["ACTIVEWEAR", [
                        ["ATHLETICSHORTS", []],
                        ["JOGGINGPANT", []],
                        ["SPORTJACKET", []],
                        ["YOGAPANT", []],
                        ["PREFORMANCETOP", []]
                    ]],
                    ["TRADITIONAL", [
                        ["KURTA", []],
                        ["SHERWANI", []],
                        ["THOBE", []],
                        ["KURTI", []],
                        ["SAREE", []],
                        ["HIJAB DRESS", []],
                        ["ABAYA", []],
                        ["KAFTAN", []]
                    ]],
                    ["DRESS", [
                        ["CASUAL DRESS", []],
                        ["MAXI DRESS", []],
                        ["EVENING DRESS", []],
                        ["SUMMER DRESS", []],
                        ["ABAYA DRESS", []]
                    ]]
                ]]
                ]],
                ["FOREVERYONE", [["ACCESSORIES",[
                        ["BAG",[
                            ["BACKPACK BAG", []],
                            ["DUFFLE BAG", []],
                            ["LAPTOP BAG", []],
                            ["WALLET BAG", []],
                            ["BELT BAG", []],
                            ["HAND BAG", []],
                            ["TOTE", []],
                            ["CLUTCH BAG", []],
                            ["CROSSBODY", []]
                        ]],
                        ["JEWELRY",[
                            ["WATCH", []],
                            ["BRACELET", []],
                            ["RING", []],
                            ["CUFFLINKS", []],
                            ["EARING", []],
                            ["NECKLACE", []],
                            ["ANKLET", []]
                        ]],
                        ["HEADWEAR", [
                            ["CAP", []],
                            ["HAT", []],
                            ["BEANIE", []],
                            ["DURAG", []],
                            ["HIJAB", []],
                            ["SCARF", []],
                            ["HEADBAND", []]
                        ]],
                        ["EYEWEAR", [
                            ["SUNGLASSES", []],
                            ["GLASSES", []],
                            ["EYELASH", []],
                            ["EYELANCE", []]
                        ]],
                        ["BELT", []],
                        ["HAIR ACCESSORIES", []],
                        ["OTHERS", [
                            ["SOCKS", []],
                            ["GLOVES", []],
                            ["SHOELACE", []],
                            ["TIE", []],
                            ["BOWTIE", []],
                            ["SHAWL", []],
                            ["TIGHTS", []]
                        ]],
                    ]],
                    ["SHOES", [
                        ["CASUAL", [
                            ["SNEAKERS", []],
                            ["LOAFERS", []],
                            ["FLATS", []],
                            ["SANDALS", []]
                        ]],
                        ["FORMAL", [
                            ["OXFORD", []],
                            ["DERBY", []],
                            ["SUIT SHOES", []],
                            ["HEELS", []],
                            ["PUMPS", []],
                            ["WEDGES", []]
                        ]],
                        ["SPORT SHOES", [
                            ["RUNNING SHOES", []],
                            ["TRAINING SHOES", []]
                        ]],
                        ["BOOTS", [
                            ["CHELSEA", []],
                            ["COMBAT", []],
                            ["WORK BOOTS", []],
                            ["ANKLE BOOTS", []],
                            ["KNEE HIGH BOOTS", []],
                            ["FORMAL BOOTS", []]
                        ]]
                    ]],
                    ["TOP", [
                        ["T-SHIRT", []],
                        ["SHIRT", []],
                        ["BLOUSES", []],
                        ["POLO SHIRT", []],
                        ["TANK", []],
                        ["SWEATER", []],
                        ["HOODIES", []],
                        ["JACKET", []],
                        ["BLAZER", []],
                        ["CROP TOP", []]
                    ]],
                    ["BOTTOM", [
                        ["JEAN", []],
                        ["PANT", []],
                        ["SHORT", []],
                        ["SKIRT", []],
                        ["LEGGING", []],
                        ["CULOTTE", []],
                        ["CHINOS", []],
                        ["TROUSERS", []],
                        ["SUIT PANT", []],
                        ["JOGGERS", []],
                        ["PALAZZO", []]
                    ]],
                    ["OUTERWEAR", [
                        ["COAT", []],
                        ["TRENCH COAT", []],
                        ["PARKA", []],
                        ["WINDBREAKER", []],
                        ["LEZER JACKET", []],
                        ["RIN COAT JACKET", []],
                        ["BOMBER JACKET", []],
                        ["CARDIGAN", []],
                        ["DENIM JACKET", []]
                    ]],
                    ["ACTIVEWEAR", [
                        ["ATHLETICSHORTS", []],
                        ["JOGGINGPANT", []],
                        ["SPORTJACKET", []],
                        ["YOGAPANT", []],
                        ["PREFORMANCETOP", []]
                    ]],
                    ["TRADITIONAL", [
                        ["KURTA", []],
                        ["SHERWANI", []],
                        ["THOBE", []],
                        ["KURTI", []],
                        ["SAREE", []],
                        ["HIJAB DRESS", []],
                        ["ABAYA", []],
                        ["KAFTAN", []]
                    ]],
                    ["DRESS", [
                        ["CASUAL DRESS", []],
                        ["MAXI DRESS", []],
                        ["EVENING DRESS", []],
                        ["SUMMER DRESS", []],
                        ["ABAYA DRESS", []]
                    ]]
                ]]]

slip_order_type=["*", "#", "-", "_", "=", "~", "LOGO", "Information", "About", "Phone_No", "Receipt_no", "Extnsion_Receipt_no", "Date", "Updated_date", "Due_date", "User", "Seller", "Customer", "Item", "Rules"]


Shop_Types = [
    "Grocery & Food Store", "Clothing & Accessories Store", "Electtronics & Tech Store", "Health &Beauty Store",
    "Home & Living Store", "Food Service Store", "Servives",
    "Supermarket", "Convenience Store", "Bakery", "Butchery",
    "Boutique", "Shoes", "Electronics", "Mobile Phones",
    "Pharmacy", "Cosmetics", "Furniture", "Hardware",
    "Restaurant", "Fast Food", "Coffee Shop", "Liquor Store",
    "Stationery", "Auto Parts", "Pet Shop", "Online Store", "Other"
]

# Function to search for documents in the doc_table SQLite database table
def search_documents(doc_id=None, doc_type=None, doc_barcode=None, extension_barcode=None, 
                    item=None, user_id=None, customer_id=None, sold_item_info=None, discount=None, 
                    tax=None, doc_created_date=None, doc_expire_date=None, doc_updated_date=None):
    given = []
    # Build the SQL query based on the provided attributes
    query = 'SELECT * FROM doc_table WHERE 1=1'
    if doc_id is not None and doc_id is not '':
        query += f" AND id='{doc_id}'"
    if doc_type is not None and doc_type != '':
        query += f" AND type='{doc_type}'"
    if doc_barcode is not None and doc_barcode is not '':
        query += f" AND doc_barcode='{doc_barcode}'"
    if extension_barcode is not None and extension_barcode is not '':
        query += f" AND extension_barcode='{extension_barcode}'"
    if item is not None and item is not '':
        query += f" AND item LIKE ?"
        if given == None:
            given.append(f'%{item}%')
        else:
            given.append(f'%{item}%')
    if user_id is not None and user_id is not '':
        query += f" AND user_id='{user_id}'"
    if customer_id is not None and customer_id is not '':
        query += f" AND customer_id='{customer_id}'"
    if sold_item_info is not None and sold_item_info is not '':
        query += f" AND sold_item_info='{sold_item_info}'"
    if discount is not None and discount is not '':
        query += f" AND discount='{discount}'"
    if tax is not None and tax is not '':
        query += f" AND tax='{tax}'"
    if doc_created_date is not None and doc_created_date is not '':
        query += f" AND doc_created_date LIKE ?"
        if given == None:
            given.append(f'%{doc_created_date}%')
        else:
            given.append(f'%{doc_created_date}%')
    if doc_expire_date is not None and doc_expire_date is not '':
        query += f" AND doc_expire_date='{doc_expire_date}'"
    if doc_updated_date is not None and doc_updated_date is not '':
        query += f" AND doc_updated_date='{doc_updated_date}'"
    
    #print(query+"\n")
    # Execute the SQL query and return the results as a list of tuples
    Update_table_database(query, (*given,))
    results = cur.fetchall()
    return results
# Example node hierarchy

class Shop_SettingForm(ttk.Notebook):
    def __init__(self, master, user, shop):
        ttk.Notebook.__init__(self, master)
        self.master = master
        self.nested_list = []
        self.user_info = None
        self.user = user
        self.Shop = shop
        self.Shops = [shop]
        self.slip_order_list = []

        self.homemaster = self
        while(True):
            if hasattr(self.homemaster, 'onDisplayFrame'):
                break
            else:
                self.homemaster = self.homemaster.master
                
        self.bg_dark = "#0d47a1"      # Deep blue
        self.bg_light = "#1565c0"     # Darker blue
        self.accent_blue = "#1976d2"  # Medium blue
        self.text_light = "#ffffff"   # White text
        self.bg_darker = "#0a3d91"    # Even darker blue
        self.button_style = {"font": ("Arial", 11, "bold"), "bg": self.accent_blue, "fg": self.text_light, "activebackground": self.bg_light, "activeforeground": self.text_light, "relief": tk.FLAT, "bd": 0}


        
        self.ShopInfo = tk.Frame(self , bg=self.bg_dark)
        self.ShopInfo.pack()
        self.add(self.ShopInfo, text="Shop Info")
        
        self.ShopInfoFrame_contaner_frame = tk.Frame(self.ShopInfo , bg=self.bg_dark)
        self.ShopInfoFrame_contaner_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.ShopInfoList_Frame_contaner_frame = tk.Frame(self.ShopInfoFrame_contaner_frame, bg=self.bg_dark)
        self.ShopInfoList_Frame_contaner_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.ShopInfoList_Frame = tk.Frame(self.ShopInfoList_Frame_contaner_frame, bg=self.bg_dark)
        self.ShopInfoList_Frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.ShopInfoitem_List_canvas = tk.Canvas(self.ShopInfoList_Frame, bg=self.bg_dark, highlightthickness=0)
        self.ShopInfoitem_List_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.ShopInfoitem_List_yscrollbar = tk.Scrollbar(self.ShopInfoList_Frame, orient='vertical', 
                                                 command=self.ShopInfoitem_List_canvas.yview, bg=self.bg_light, activebackground=self.accent_blue)
        self.ShopInfoitem_List_yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.ShopInfoitem_List_xscrollbar = tk.Scrollbar(self.ShopInfoList_Frame_contaner_frame, orient='horizontal', 
                                                 command=self.ShopInfoitem_List_canvas.xview, bg=self.bg_light, activebackground=self.accent_blue)
        self.ShopInfoitem_List_xscrollbar.pack(side=tk.TOP, fill=tk.X)
        
        self.ShopInfoitem_List_canvas.configure(xscrollcommand=self.ShopInfoitem_List_xscrollbar.set, 
                                       yscrollcommand=self.ShopInfoitem_List_yscrollbar.set)

        # Create the frame for the Shop Info
        self.Shop_listinfo_frame = tk.Frame(self.ShopInfoitem_List_canvas, bg=self.bg_dark, bd=2, relief="raised")
        self.Shop_listinfo_frame.columnconfigure((0), weight=1)
        self.Shop_listinfo_frame.columnconfigure((1), weight=1)
        self.Shop_listinfo_frame.columnconfigure((2), weight=1)
        self.Shop_listinfo_frame.columnconfigure((3), weight=1)
        self.Shop_listinfo_frame.columnconfigure((4), weight=1)
        self.Shop_listinfo_frame.columnconfigure((5), weight=1)
        self.Shop_listinfo_frame.columnconfigure((6), weight=1)
        self.Shop_listinfo_frame.columnconfigure((7), weight=1)
        self.Shop_listinfo_frame.columnconfigure((8), weight=1)
        self.Shop_listinfo_frame.columnconfigure((9), weight=1)
        self.Shop_listinfo_frame.columnconfigure((10), weight=1)
        self.Shop_listinfo_frame.columnconfigure((11), weight=1)
        self.Shop_listinfo_frame.columnconfigure((12), weight=1)
        self.Shop_listinfo_frame.columnconfigure((13), weight=1)
        self.Shop_listinfo_frame.columnconfigure((14), weight=1)
        #self.Shop_listinfo_frame.rowconfigure((0), weight=1)
        

        
        self.window_id = self.ShopInfoitem_List_canvas.create_window((0, 0), window=self.Shop_listinfo_frame, anchor="nw")
        
        def resize(event):
            
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
        
            self.ShopInfoitem_List_canvas.configure(scrollregion=self.ShopInfoitem_List_canvas.bbox("all"))
            self.ShopInfoitem_List_canvas.itemconfig(self.window_id, width=screen_width-(screen_width/10))
        self.Shop_listinfo_frame.bind('<Configure>', resize)



        self.Shop_rate = 0
        self.Shop_profile_frame = tk.Frame(self.Shop_listinfo_frame, bg=self.bg_dark)
        self.Shop_profile_frame.grid(row=0, column=2, rowspan=4, columnspan=2, sticky='ew')

        self.Shop_avatar_label = tk.Label(self.Shop_profile_frame, bg=self.bg_dark)
        self.Shop_avatar_label.pack(pady=10)
        self.Shop_avatar_label.bind("<Button-1>", lambda _: self.change_shop_image())
        
        self.Shop_rate_frame = tk.Frame(self.Shop_listinfo_frame, bg=self.bg_dark)
        self.Shop_rate_frame.grid(row=4, column=3, columnspan=2, sticky='ew')

        self.Shop_rate20_label = tk.Label(self.Shop_rate_frame, bg=self.bg_dark)
        self.Shop_rate20_label.pack(side="left", pady=10)
        self.Shop_rate20_label.bind("<Button-1>", lambda _: self.change_rate_image(20))
        self.Shop_rate40_label = tk.Label(self.Shop_rate_frame, bg=self.bg_dark)
        self.Shop_rate40_label.pack(side="left", pady=10)
        self.Shop_rate40_label.bind("<Button-1>", lambda _: self.change_rate_image(40))
        self.Shop_rate60_label = tk.Label(self.Shop_rate_frame, bg=self.bg_dark)
        self.Shop_rate60_label.pack(side="left", pady=10)
        self.Shop_rate60_label.bind("<Button-1>", lambda _: self.change_rate_image(60))
        self.Shop_rate80_label = tk.Label(self.Shop_rate_frame, bg=self.bg_dark)
        self.Shop_rate80_label.pack(side="left", pady=10)
        self.Shop_rate80_label.bind("<Button-1>", lambda _: self.change_rate_image(80))
        self.Shop_rate100_label = tk.Label(self.Shop_rate_frame, bg=self.bg_dark)
        self.Shop_rate100_label.pack(side="left", pady=10)
        self.Shop_rate100_label.bind("<Button-1>", lambda _: self.change_rate_image(100))
        
        
        self.Shop_info_label = tk.Label(self.Shop_listinfo_frame, text='Shop Informations:', bg=self.bg_dark, fg=self.text_light)
        self.Shop_info_label.grid(row=0, column=5, columnspan=6, sticky='ew')
        
        self.Shop_startedDate_label = tk.Label(self.Shop_listinfo_frame, text='Since ', bg=self.bg_dark, fg=self.text_light)
        self.Shop_startedDate_label.grid(row=1, column=6, columnspan=3, sticky='ew')
        
        self.Shop_isenabled_var = tk.IntVar()
        self.Shop_isenabled_var.set(1)
        self.Shop_isenabled_date_Checkbutton = tk.Checkbutton(self.Shop_listinfo_frame, text='Shop Is Enabled :', bg=self.bg_dark, variable=self.Shop_isenabled_var) # , fg=self.text_light
        self.Shop_isenabled_date_Checkbutton.grid(row=4, column=6, columnspan=3)





        
        self.Brand_rate = 0
        self.Brand_profile_frame = tk.Frame(self.Shop_listinfo_frame, bg=self.bg_dark)
        self.Brand_profile_frame.grid(row=0, column=10, rowspan=4, columnspan=2, sticky='ew')

        self.Brand_avatar_label = tk.Label(self.Brand_profile_frame, bg=self.bg_dark)
        self.Brand_avatar_label.pack(pady=10)
        self.Brand_avatar_label.bind("<Button-1>", lambda _: self.change_Brand_image())
        
        self.Brand_rate_frame = tk.Frame(self.Shop_listinfo_frame, bg=self.bg_dark)
        self.Brand_rate_frame.grid(row=4, column=11, columnspan=2, sticky='ew')

        self.Brand_rate20_label = tk.Label(self.Brand_rate_frame, bg=self.bg_dark)
        self.Brand_rate20_label.pack(side="left", pady=10)
        self.Brand_rate20_label.bind("<Button-1>", lambda _: self.change_Brand_rate_image(20))
        self.Brand_rate40_label = tk.Label(self.Brand_rate_frame, bg=self.bg_dark)
        self.Brand_rate40_label.pack(side="left", pady=10)
        self.Brand_rate40_label.bind("<Button-1>", lambda _: self.change_Brand_rate_image(40))
        self.Brand_rate60_label = tk.Label(self.Brand_rate_frame, bg=self.bg_dark)
        self.Brand_rate60_label.pack(side="left", pady=10)
        self.Brand_rate60_label.bind("<Button-1>", lambda _: self.change_Brand_rate_image(60))
        self.Brand_rate80_label = tk.Label(self.Brand_rate_frame, bg=self.bg_dark)
        self.Brand_rate80_label.pack(side="left", pady=10)
        self.Brand_rate80_label.bind("<Button-1>", lambda _: self.change_Brand_rate_image(80))
        self.Brand_rate100_label = tk.Label(self.Brand_rate_frame, bg=self.bg_dark)
        self.Brand_rate100_label.pack(side="left", pady=10)
        self.Brand_rate100_label.bind("<Button-1>", lambda _: self.change_Brand_rate_image(100))
        
            
        self.Shop_name_label = tk.Label(self.Shop_listinfo_frame, text='Shop Name:', bg=self.bg_dark, fg=self.text_light)
        self.Shop_name_label.grid(row=6, column=0, columnspan=5, sticky=tk.W)
        self.Shop_name_entry = tk.Entry(self.Shop_listinfo_frame)
        self.Shop_name_entry.grid(row=7, column=1, columnspan=5, sticky="nsew")

        self.Shop_brand_name_label = tk.Label(self.Shop_listinfo_frame, text='Shop Brand Name:', bg=self.bg_dark, fg=self.text_light)
        self.Shop_brand_name_label.grid(row=6, column=7, columnspan=5, sticky=tk.W)
        self.Shop_brand_name_entry = tk.Entry(self.Shop_listinfo_frame)
        self.Shop_brand_name_entry.grid(row=7, column=8, columnspan=5, sticky="nsew")

        
        self.Shop_types_var = tk.StringVar()  # displayed in the combobox

        # Combobox for User ID (shows user_name but stores user_id)
        self.Shop_type_label = tk.Label(self.Shop_listinfo_frame, text='Shop Type:', bg=self.bg_dark, fg=self.text_light)
        self.Shop_type_label.grid(row=8, column=0, columnspan=5, sticky=tk.W)
        
        self.Shop_type_entry = ttk.Combobox(self.Shop_listinfo_frame, textvariable=self.Shop_types_var, values=Shop_Types, state='readonly')
        self.Shop_type_entry.grid(row=9, column=1, columnspan=5, sticky="nsew")

        # Create the label and entry for the user ID search
        user_info = fetch_as_dict_list(self.homemaster.Link, 'SELECT * FROM USERS', ())  
        # prepare names lists with a blank first entry for null selection
        self.user_names = [''] + [u['User_name'] for u in user_info] if user_info else ['']
        self.customer_names = [''] + [u['User_name'] for u in user_info] if user_info else ['']
        self.seller_names = [''] + [u['User_name'] for u in user_info] if user_info else ['']
        self.At_shop_names = [''] + [u['User_name'] for u in user_info] if user_info else ['']

        # maps including blank -> ''
        self.user_map = {'': ''}
        self.user_map_id = {'': ''}
        if user_info:
            for u in user_info:
                if u['User_id'] is None:
                    uid = u['Id']
                else:
                    uid = u['User_id']
                self.user_map[u['User_name']] = str(uid)
                self.user_map_id[str(uid)] = u['User_name']

        self.user_id_var = tk.StringVar()    # will store the actual user_id (used by perform_search via .get())
        self.user_name_var = tk.StringVar()  # displayed in the combobox

        # Combobox for User ID (shows user_name but stores user_id)
        self.user_id_label = tk.Label(self.Shop_listinfo_frame, text="Shop Owner:", bg=self.bg_dark, fg=self.text_light)
        self.user_id_label.grid(row=8, column=7, columnspan=5, sticky=tk.W)
        
        self.user_combobox = ttk.Combobox(self.Shop_listinfo_frame, textvariable=self.user_name_var, values=self.user_names)
        self.user_combobox.grid(row=9, column=8, columnspan=5, sticky="nsew")


        def _on_user_selected(event=None):
            name = self.user_name_var.get()
            self.user_id_var.set(self.user_map.get(name, ''))
            
        def on_keyrelease(event=None):
            #print("on_keyrelease ")
            typed = self.user_combobox.get().lower()
            if typed == '':
                self.user_combobox['values'] = self.user_names
            else:
                filtered = [item for item in self.user_names if typed in item.lower()]
                self.user_combobox['values'] = filtered
                if filtered:
                    self.user_combobox.event_generate('<Down>')
            self.user_combobox.focus()
            self.user_combobox.icursor(tk.END)
            
        self.user_name_var.trace('w', lambda name, index, mode: on_keyrelease())
        self.user_combobox.bind('<<ComboboxSelected>>', _on_user_selected)
        
        self.Shop_link_label = tk.Label(self.Shop_listinfo_frame, text='Shop API Link :', bg=self.bg_dark, fg=self.text_light)
        self.Shop_link_label.grid(row=10, column=0, columnspan=5, sticky=tk.W)
        self.Shop_link_entry = tk.Entry(self.Shop_listinfo_frame)
        self.Shop_link_entry.grid(row=11, column=1, columnspan=5, sticky="nsew")
        
        self.Shop_email_label = tk.Label(self.Shop_listinfo_frame, text='Shop Email :', bg=self.bg_dark, fg=self.text_light)
        self.Shop_email_label.grid(row=10, column=7, columnspan=5, sticky=tk.W)
        self.Shop_email_entry = tk.Entry(self.Shop_listinfo_frame)
        self.Shop_email_entry.grid(row=11, column=8, columnspan=5, sticky="nsew")


        self.Shop_about_label = tk.Label(self.Shop_listinfo_frame, text='Shop About :', bg=self.bg_dark, fg=self.text_light)
        self.Shop_about_label.grid(row=12, column=0, columnspan=5, sticky=tk.W)
        self.Shop_about_entry = tk.Entry(self.Shop_listinfo_frame)
        self.Shop_about_entry.grid(row=13, column=1, columnspan=5, sticky="nsew")
        
        self.Shop_country_label = tk.Label(self.Shop_listinfo_frame, text='Shop Country:', bg=self.bg_dark, fg=self.text_light)
        self.Shop_country_label.grid(row=14, column=7, columnspan=5, sticky=tk.W)
        self.Shop_country_entry = tk.Entry(self.Shop_listinfo_frame)
        self.Shop_country_entry.grid(row=15, column=8, columnspan=5, sticky="nsew")
        
        self.Shop_password_label = tk.Label(self.Shop_listinfo_frame, text='Shop Password:', bg=self.bg_dark, fg=self.text_light)
        self.Shop_password_label.grid(row=14, column=0, columnspan=5, sticky=tk.W)
        self.Shop_password_entry = tk.Entry(self.Shop_listinfo_frame,  show="*", bg="#ffffff", fg="#0d47a1", font=("Roboto", 11), relief=tk.FLAT, bd=2)
        self.Shop_password_entry.grid(row=15, column=1, columnspan=5, sticky="nsew")
        
        self.Shop_Contact_label = tk.Label(self.Shop_listinfo_frame, text='Shop Contact:', bg=self.bg_dark, fg=self.text_light)
        self.Shop_Contact_label.grid(row=12, column=7, columnspan=5, sticky=tk.W)
        self.Shop_Contact_entry = tk.Entry(self.Shop_listinfo_frame)
        self.Shop_Contact_entry.grid(row=13, column=8, columnspan=5, sticky="nsew")
        

        
        
        # ----------------------     Phone Number
        self.Shop_phone_nums = "" 
        self.Shop_phone_num_label = tk.Label(self.Shop_listinfo_frame, text='Shop Phone Numbers:', bg=self.bg_dark, fg=self.text_light)
        self.Shop_phone_num_label.grid(row=16, column=0, columnspan=5, sticky=tk.W)
        self.Shop_phone_nums_list = tk.Listbox(self.Shop_listinfo_frame)
        self.Shop_phone_nums_list.grid(row=17, column=1, columnspan=5, sticky="nsew")

        def load_Shop_phone_num():
            self.Shop_phone_nums_list.delete(0, tk.END)
            infos = self.Shop_phone_nums.split("=")
            for l in infos:
                    self.Shop_phone_nums_list.insert(tk.END, str(l))
        self.load_Shop_phone_num = load_Shop_phone_num

        self.Shop_phone_num_entry = tk.Entry(self.Shop_listinfo_frame)
        self.Shop_phone_num_entry.grid(row=18, column=0, columnspan=3, sticky="nsew")
        
        def Shop_phone_num_add():
            v = self.Shop_phone_num_entry.get()
            if self.Shop_phone_nums == "":
                self.Shop_phone_nums = v
            else:
                self.Shop_phone_nums += "=" + v
            load_Shop_phone_num()
            
        def Shop_phone_num_Remove():
            current_selection_indexes = self.Shop_phone_nums_list.curselection()
            if not current_selection_indexes:
                return
            infos = self.Shop_phone_nums.split("=")
            newnums = ""
            for i, l in enumerate(infos):
                if not i == current_selection_indexes[0]:
                    if newnums == "":
                        newnums = l
                    else:
                        newnums += "=" + l
            if not newnums == "":
               self.Shop_phone_nums= newnums
            load_Shop_phone_num()
               
        self.add_shop_pno_button = tk.Button(self.Shop_listinfo_frame, text='Add', command=Shop_phone_num_add, **self.button_style)
        self.add_shop_pno_button.grid(row=18, column=4, sticky=tk.E)
        self.remove_shop_pno_button = tk.Button(self.Shop_listinfo_frame, text='Remove', command=Shop_phone_num_Remove, **self.button_style)
        self.remove_shop_pno_button.grid(row=18, column=5, sticky=tk.E)
        # ------------------------------

        
        # ----------------------   Link 
        self.Shop_slinks = ""
        self.Shop_slink_label = tk.Label(self.Shop_listinfo_frame, text='Shop Social Links :', bg=self.bg_dark, fg=self.text_light)
        self.Shop_slink_label.grid(row=16, column=7, columnspan=5, sticky=tk.W)
        self.Shop_slink_list = tk.Listbox(self.Shop_listinfo_frame)
        self.Shop_slink_list.grid(row=17, column=8, columnspan=5, sticky="nsew")

        self.Shop_slink_entry = tk.Entry(self.Shop_listinfo_frame)
        self.Shop_slink_entry.grid(row=18, column=7, columnspan=3, sticky="nsew")
        
        def load_Shop_slink():
            self.Shop_slink_list.delete(0, tk.END)
            infos = self.Shop_slinks.split("+")
            for l in infos:
                    self.Shop_slink_list.insert(tk.END, str(l))
        self.load_Shop_slink = load_Shop_slink
       
        def Shop_slink_changed():
            v = self.Shop_slink_entry.get()
            if self.Shop_slinks == "":
                self.Shop_slinks = v
            else:
                self.Shop_slinks += "+" + v
            load_Shop_slink()
            
        def Shop_slink_Remove():
            current_selection_indexes = self.Shop_slink_list.curselection()
            if not current_selection_indexes:
                return
            infos = self.Shop_slinks.split("+")
            newnums = ""
            for i, l in enumerate(infos):
                if not i == current_selection_indexes[0]:
                    if newnums == "":
                        newnums = l
                    else:
                        newnums += "+" + l
            if not newnums == "":
               self.Shop_slinks= newnums
            load_Shop_slink()

        
        self.add_Shop_slink_button = tk.Button(self.Shop_listinfo_frame, text='Add', command=Shop_slink_changed, **self.button_style)
        self.add_Shop_slink_button.grid(row=18, column=10, sticky=tk.E)
        self.remove_Shop_slink_button = tk.Button(self.Shop_listinfo_frame, text='Remove', command=Shop_slink_Remove, **self.button_style)
        self.remove_Shop_slink_button.grid(row=18, column=11, sticky=tk.E)
        # ------------------------------


        # ----------------------   Location 
        self.Shop_locations = ""
        self.Shop_location_label = tk.Label(self.Shop_listinfo_frame, text='Shop Location:', bg=self.bg_dark, fg=self.text_light)
        self.Shop_location_label.grid(row=19, column=0, columnspan=5, sticky=tk.W)
        self.Shop_location_list = tk.Listbox(self.Shop_listinfo_frame)
        self.Shop_location_list.grid(row=20, column=1, columnspan=5, sticky="nsew")

        self.Shop_location_entry = tk.Entry(self.Shop_listinfo_frame)
        self.Shop_location_entry.grid(row=21, column=1, columnspan=3, sticky="nsew")
        
        def load_Shop_location():
            self.Shop_location_list.delete(0, tk.END)
            infos = self.Shop_locations.split("=")
            for l in infos:
                self.Shop_location_list.insert(tk.END, str(l))
        self.load_Shop_location = load_Shop_location
        
        
        def Shop_location_changed():
            v = self.Shop_location_entry.get()
            if self.Shop_locations == "":
                self.Shop_locations = v
            else:
                self.Shop_locations += "=" + v
            load_Shop_location()
            
        def Shop_location_Remove():
            current_selection_indexes = self.Shop_location_list.curselection()
            if not current_selection_indexes:
                return
            infos = self.Shop_locations.split("=")
            newnums = ""
            for i, l in enumerate(infos):
                if not i == current_selection_indexes[0]:
                    if newnums == "":
                        newnums = l
                    else:
                        newnums += "=" + l
            if not newnums == "":
               self.Shop_locations= newnums
            load_Shop_location()
        

        
        self.add_Shop_location_button = tk.Button(self.Shop_listinfo_frame, text='Add', command=Shop_location_changed, **self.button_style)
        self.add_Shop_location_button.grid(row=21, column=4, sticky=tk.E)
        self.remove_Shop_location_button = tk.Button(self.Shop_listinfo_frame, text='Remove', command=Shop_location_Remove, **self.button_style)
        self.remove_Shop_location_button.grid(row=21, column=5, sticky=tk.E)
        # ------------------------------


        # ----------------------   Rules 
        self.Shop_rules = ""
        self.Shop_rules_label = tk.Label(self.Shop_listinfo_frame, text='Shop Rules:', bg=self.bg_dark, fg=self.text_light)
        self.Shop_rules_label.grid(row=19, column=7, columnspan=5, sticky=tk.W)
        self.Shop_rules_list = tk.Listbox(self.Shop_listinfo_frame)
        self.Shop_rules_list.grid(row=20, column=8, columnspan=5, sticky="nsew")

        self.Shop_rules_entry = tk.Entry(self.Shop_listinfo_frame)
        self.Shop_rules_entry.grid(row=21, column=7, columnspan=3, sticky="nsew")
        
        def load_Shop_rules():
            self.Shop_rules_list.delete(0, tk.END)
            infos = self.Shop_rules.split("+")
            for l in infos:
                    self.Shop_rules_list.insert(tk.END, str(l))
        self.load_Shop_rules = load_Shop_rules
        
        
        def Shop_rules_changed():
            v = self.Shop_rules_entry.get()
            if self.Shop_rules == "":
                self.Shop_rules = v
            else:
                self.Shop_rules += "+" + v
            load_Shop_rules()
            
        def Shop_rules_Remove():
            current_selection_indexes = self.Shop_rules_list.curselection()
            if not current_selection_indexes:
                return
            infos = self.Shop_rules.split("+")
            newnums = ""
            for i, l in enumerate(infos):
                if not i == current_selection_indexes[0]:
                    if newnums == "":
                        newnums = l
                    else:
                        newnums += "+" + l
            if not newnums == "":
               self.Shop_rules= newnums
            load_Shop_rules()

        
        self.add_Shop_rules_button = tk.Button(self.Shop_listinfo_frame, text='Add', command=Shop_rules_changed, **self.button_style)
        self.add_Shop_rules_button.grid(row=21, column=10, sticky=tk.E)
        self.remove_Shop_rules_button = tk.Button(self.Shop_listinfo_frame, text='Remove', command=Shop_rules_Remove, **self.button_style)
        self.remove_Shop_rules_button.grid(row=21, column=11, sticky=tk.E)
        # ------------------------------


        self.save_button = tk.Button(self.Shop_listinfo_frame, text="SAVE CHANGE", command=self.save_shop_info, **self.button_style)
        self.save_button.grid(row=22, column=5, columnspan=5, sticky="nsew")

        # Create the frame for the Shop Info
        self.Expenses_frame = ExpensesForm(self, user, self.Shops, bg=self.bg_dark)
        self.Expenses_frame.pack()
        self.add(self.Expenses_frame, text="Shop Expenses")
        
        
        # Create the frame for the Shop Info
        self.Workers_frame = WorkersForm(self, user, self.Shops, self.Shop, bg=self.bg_dark)
        self.Workers_frame.pack()
        self.add(self.Workers_frame, text="Workers & SECURITY Levels")
        
        
        '''self.Shop_listinfo_frame.grid_columnconfigure(0, weight=5)
        self.Shop_listinfo_frame.grid_columnconfigure(1, weight=5)
        self.Shop_listinfo_frame.grid_columnconfigure(2, weight=5)
        self.Shop_listinfo_frame.grid_columnconfigure(3, weight=5)
        self.Shop_listinfo_frame.grid_columnconfigure(4, weight=5)
        self.Shop_listinfo_frame.grid_columnconfigure(5, weight=5)
        self.Shop_listinfo_frame.grid_columnconfigure(6, weight=5)
        self.Shop_listinfo_frame.grid_columnconfigure(7, weight=5)
        self.Shop_listinfo_frame.grid_rowconfigure(0, weight=5)
        self.Shop_listinfo_frame.grid_rowconfigure(1, weight=5)
        self.Shop_listinfo_frame.grid_rowconfigure(2, weight=5)
        self.Shop_listinfo_frame.grid_rowconfigure(3, weight=5)
        self.Shop_listinfo_frame.grid_rowconfigure(4, weight=5)
        self.Shop_listinfo_frame.grid_rowconfigure(5, weight=5)
        self.Shop_listinfo_frame.grid_rowconfigure(6, weight=5)
        self.Shop_listinfo_frame.grid_rowconfigure(7, weight=5)
        
        
        self.chart1_total_title = tk.Label(self.Shop_listinfo_frame, text="TOTAL ITEM COUNT :")
        self.chart1_total_title.grid(row=1, column=4, columnspan=3)

        self.style_var1 = tk.StringVar()
        self.style_var1.set("2")
        #self.style_var1.trace("w", on_style_selected)
        self.style_dropdown1 = tk.OptionMenu(self.Shop_listinfo_frame, self.style_var1, "1", "2", "3", "4")
        self.style_dropdown1.grid(row=2, column=4, sticky="nsew")
        
        self.next_button1 = tk.Button(self.Shop_listinfo_frame, text="<", font=("Arial", 12))
        self.next_button1.grid(row=2, column=5, sticky="nsew")
        self.prev_button1 = tk.Button(self.Shop_listinfo_frame, text=">", font=("Arial", 12))
        self.prev_button1.grid(row=2, column=6, sticky="nsew")
        
        self.product_list = tk.Listbox(self.Shop_listinfo_frame, width=30)
        self.product_list.grid(row=3, column=0, columnspan=2, sticky="nsew")
        
        self.details_frame = tk.Frame(self.Shop_listinfo_frame)
        self.details_frame.grid(row=3, column=5, columnspan=3)'''
        
        # Create the frame for the user details
        
        self.inventory = []
        self.selected_type_path = None
        self.selected_type_path_parent = None
        
        self.Type_details_frame = tk.Frame(self, bg=self.bg_dark)
        self.Type_details_frame.pack(fill=tk.BOTH, expand=True)

        self.add(self.Type_details_frame, text="Others...")
        
        self.Frame_contaner_frame = tk.Frame(self.Type_details_frame, bg=self.bg_dark)
        self.Frame_contaner_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


        self.List_Frame_contaner_frame = tk.Frame(self.Frame_contaner_frame, bg=self.bg_dark)
        self.List_Frame_contaner_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Frame Form catagori Control
        self.catagori_controler_frame = tk.Frame(self.List_Frame_contaner_frame, bg=self.bg_dark)
        self.catagori_controler_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=False)
        

        self.type_value_label = tk.Label(self.catagori_controler_frame, text='Value', bg=self.bg_dark, fg=self.text_light)
        self.type_value_label.grid(row=0, column=0, sticky=tk.E)
        self.type_value_entry = tk.Entry(self.catagori_controler_frame)
        self.type_value_entry.grid(row=0, column=1, columnspan=3, sticky=tk.E)
        self.add_new_button = tk.Button(self.catagori_controler_frame, text='Add', command=self.add_new_value, **self.button_style)
        self.add_new_button.grid(row=0, column=4, sticky=tk.E)
        
        self.cear_button = tk.Button(self.catagori_controler_frame, text='Clear Selection', command=self.clear_selected_path, **self.button_style)
        self.cear_button.grid(row=0, column=5, sticky=tk.E)
        self.dele_type_button = tk.Button(self.catagori_controler_frame, text='DELETE Selected', command=self.dele_selected, **self.button_style)
        self.dele_type_button.grid(row=0, column=6, sticky=tk.E)
        self.cear_button = tk.Button(self.catagori_controler_frame, text='Defalute', command=self.Set_Deffalute_type_value, **self.button_style)
        self.cear_button.grid(row=0, column=7, sticky=tk.E)
        
        self.selected_label = tk.Label(self.catagori_controler_frame, text='No selected', bg=self.bg_dark, fg=self.text_light)
        self.selected_label.grid(row=1, column=0, columnspan=1000, sticky=tk.E)


        self.List_Frame = tk.Frame(self.List_Frame_contaner_frame, bg=self.bg_dark)
        self.List_Frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        self.item_List_canvas = tk.Canvas(self.List_Frame, bg=self.bg_dark, highlightthickness=0)
        self.item_List_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)


        
        self.tree = ttk.Treeview(self.item_List_canvas, columns=
                                 ("Shop Name", "Code", "Color", "Size", "Barcode",
                                  "Qtyfirst", "Qty", "cdate", "update"))
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.on_path_select)
        #self.tree.pack(side=tk.LEFT, expand=True)
        self.tree.heading("#0", text="Type", anchor=tk.W)
        
        self.item_List_yscrollbar = tk.Scrollbar(self.List_Frame, orient='vertical', 
                                                 command=self.tree.yview, bg=self.bg_light, activebackground=self.accent_blue)
        self.item_List_yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.item_List_xscrollbar = tk.Scrollbar(self.List_Frame_contaner_frame, orient='horizontal', 
                                                 command=self.tree.xview, bg=self.bg_light, activebackground=self.accent_blue)
        self.item_List_xscrollbar.pack(side=tk.TOP, fill=tk.X)
        
        self.tree.configure(xscrollcommand=self.item_List_xscrollbar.set, 
                                       yscrollcommand=self.item_List_yscrollbar.set)


        self.item_List_canvas.create_window((0, 0), window=self.tree, anchor=tk.NW)
        #self.tree.bind('<Configure>', lambda e: self.item_List_canvas.configure(scrollregion=self.item_List_canvas.bbox("all")))

        self.catagory_Display_frame = tk.Frame(self.List_Frame_contaner_frame, bg=self.bg_dark)
        self.catagory_Display_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        # Slip controlling Frame
        self.slip_frame = tk.Frame(self.catagory_Display_frame, bg=self.bg_dark)
        self.slip_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        
        # Create the frame for the user details
        self.Shops_Names = [shop['Shop_name'] for shop in self.Shops]                            
        self.User_Shopes_Combobox = ttk.Combobox(self.slip_frame, values=self.Shops_Names, width=10)
        self.User_Shopes_Combobox.grid(row=7, column=0, sticky="nsew")
        self.User_Shopes_Combobox.current(0)
        
        self.slip_option_var = tk.StringVar()
        #self.slip_option_var.set("")
        self.slip_option_dropdown = tk.OptionMenu(self.slip_frame, self.slip_option_var, *slip_order_type, command=self.on_new_order_selected)
        self.slip_option_dropdown.grid(row=8, column=0, sticky="nsew")
        self.Dele_button = tk.Button(self.slip_frame, text="Delete", font=("Arial", 12), command=self.dele_slip_order)
        self.Dele_button.grid(row=8, column=1, sticky="nsew")
        

        self.UP_button = tk.Button(self.slip_frame, text="UP", font=("Arial", 12), command= lambda: self.move_slip_order("UP"))
        self.UP_button.grid(row=9, column=0, sticky="nsew")
        self.DOWN_button = tk.Button(self.slip_frame, text="DOWN", font=("Arial", 12), command=lambda: self.move_slip_order("DOWN"))
        self.DOWN_button.grid(row=10, column=0, sticky="nsew")

        # New listbox in the main frame
        self.slip_order_list_items = tk.Listbox(self.slip_frame)
        self.slip_order_list_items.grid(row=9, column=1, rowspan=2, sticky=tk.N)

        self.slip_width_label = tk.Label(self.slip_frame, text='slip_width:', bg=self.bg_dark, fg=self.text_light)
        self.slip_width_label.grid(row=11, column=0, sticky=tk.W)
        self.slip_width_entry = tk.Entry(self.slip_frame)
        self.slip_width_entry.grid(row=11, column=1, sticky=tk.W)
        self.slip_width_var = tk.StringVar()
        self.slip_width_entry["textvariable"] = self.slip_width_var
        self.slip_width_var.trace('w', self.slip_width_changed)


        self.slip_hight_label = tk.Label(self.slip_frame, text='slip_hight:', bg=self.bg_dark, fg=self.text_light)
        self.slip_hight_label.grid(row=12, column=0, sticky=tk.W)
        self.slip_hight_entry = tk.Entry(self.slip_frame)
        self.slip_hight_entry.grid(row=12, column=1, sticky=tk.W)
        self.slip_hight_var = tk.StringVar()
        self.slip_hight_entry["textvariable"] = self.slip_hight_var
        self.slip_hight_var.trace('w', self.slip_hight_changed)

        
        


        # Rghit Controlling fram
        self.controler_frame = tk.Frame(self.Type_details_frame, bg=self.bg_dark)
        self.controler_frame.pack(side=tk.TOP, fill=tk.BOTH)
        
        #self.load_setting()
        
        self.load_slip_order()
        self.load_shop_info()
        self.Load_type_value() 
        

        self.load_shop_image()

        self.load_rate_image()
        self.load_Brand_rate_image()
        self.load_Brand_image()
        
        # Pack the widgets for the product tab2
        #self.update_product_listbox()
        #
        #self.Item_To_Update()

    # typeing catagorry
    def load_type_info(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        if self.Shop_deff_type and self.Shop_deff_type != "":
            try:
                qty_info_list = json.loads(self.Shop_deff_type)
            except Exception as e:
                qty_info_list = Shop_deff_type
            def sub(ls, parent):
                for l in ls:
                    n = self.tree.insert(parent, "end", text=l[0])
                    sub(l[1], n)
            if qty_info_list:
                sub(qty_info_list, "")

    def dele_selected(self):
        item = self.tree.selection()[0]
        parent_item = self.tree.parent(item)
        self.tree.delete(item)
        self.selected_type_path = self.tree.parent(parent_item)
        txt = self.tree.item(self.selected_type_path, "text")
        self.load_path(parent_item, txt)
        self.convert_to_text()

    def on_path_select(self, event):
        item = self.tree.selection()[0]
        parent_item = self.tree.parent(item)
        self.selected_type_path_parent = self.tree.parent(item)
        self.selected_type_path = item
        txt = self.tree.item(item, "text")
        self.load_path(parent_item, txt)
        
    def load_path(self, parent_item, text):
        parent_names = []
        parent_names.append(text)
        while parent_item:
            name = self.tree.item(parent_item, "text")
            parent_names.append(name)
            parent_item = self.tree.parent(parent_item)
        p = len(parent_names)-1
        text = "\\"
        while not p < 0:
            text += parent_names[p] + "\\"
            p-=1
        self.selected_label.config(text=text)

    def clear_selected_path(self):
        self.selected_type_path = None
        self.selected_label.config(text="\\")
        
    
    def add_new_value(self):
        if self.selected_type_path:
            self.selected_type_path = self.tree.insert(self.selected_type_path, "end", text=self.type_value_entry.get())
        else:
            self.selected_type_path = self.tree.insert("", "end", text=self.type_value_entry.get())
        self.load_path(self.selected_type_path, "")
        self.convert_to_text()
        
    # Create the "Change" button
    def build_nested_list(self, item):
        children = self.tree.get_children(item)
        if len(children) > 0:
            nested_list = []
            for child in children:
                child_text = self.tree.item(child, "text")
                nested_list.append([child_text, self.build_nested_list(child)])
            return nested_list
        else:
            return []
        
    def Load_type_value(self):
        shop_ = self.Shop
        if shop_:
            self.Shop_deff_type = shop_['Shop_Items_type']
            self.load_type_info()
            
    def Set_Deffalute_type_value(self):
        answer = tk.messagebox.askquestion("Question", "This Will Change All Edited Catagory To System Deffalut one. Change To System Deffalut ?")
        if answer == 'yes':
            self.Shop_deff_type = json.dumps(Shop_deff_type)
            self.load_type_info()
            self.convert_to_text()
        else:
            self.type_value_entry.delete(0, tk.END)
            self.type_value_entry.insert(0, self.Shop_deff_type)
        
    def convert_to_text(self):
        nested_list = []
        for item in self.tree.get_children():
            child_text = self.tree.item(item, "text")
            nested_list.append([child_text, self.build_nested_list(item)])
        text = json.dumps(nested_list)
        shop_ = self.Shop
        if shop_:
            Update_table_database('UPDATE Shops SET Shop_Items_type=? WHERE Shop_id=?', (text, shop_['Shop_Id']))
            self.homemaster.Shops_info['Selected_Shop']['Shop_Items_type'] = text
            self.Shop_deff_type = text

    def load_Brand_rate_image(self):
        ratingimglist = [self.Brand_rate20_label, self.Brand_rate40_label, self.Brand_rate60_label, self.Brand_rate80_label, self.Brand_rate100_label]
        for i, img_frame in enumerate(ratingimglist):
            if (i+1)*20 == self.Brand_rate or ( ((i+1)*20)-20 < self.Brand_rate and self.Brand_rate > 0):
                img = Image.open(MAIN_dir+"\\data\\Icon\\rating\\star2.png").resize((20, 20))
                img = ImageTk.PhotoImage(img)
                img_frame.config(image=img)
                img_frame.image = img
            elif ((i+1)*20)-10 == self.Brand_rate or ( ((i+1)*20)-30 < self.Brand_rate and self.Brand_rate > 0):
                img = Image.open(MAIN_dir+"\\data\\Icon\\rating\\star1.png").resize((20, 20))
                img = ImageTk.PhotoImage(img)
                img_frame.config(image=img)
                img_frame.image = img
            else:
                img = Image.open(MAIN_dir+"\\data\\Icon\\rating\\star0.png").resize((20, 20))
                img = ImageTk.PhotoImage(img)
                img_frame.config(image=img)
                img_frame.image = img
                
    def change_Brand_rate_image(self, changeto):
        if self.Brand_rate == changeto:
            self.Brand_rate = changeto-20
        elif self.Brand_rate == changeto-10:
            self.Brand_rate = changeto
        else:
            self.Brand_rate = changeto-10
        self.load_Brand_rate_image()

    def load_rate_image(self):
        ratingimglist = [self.Shop_rate20_label, self.Shop_rate40_label, self.Shop_rate60_label, self.Shop_rate80_label, self.Shop_rate100_label]
        for i, img_frame in enumerate(ratingimglist):
            if (i+1)*20 == self.Shop_rate or ( ((i+1)*20)-20 < self.Shop_rate and self.Shop_rate > 0):
                img = Image.open(MAIN_dir+"\\data\\Icon\\rating\\star2.png").resize((20, 20))
                img = ImageTk.PhotoImage(img)
                img_frame.config(image=img)
                img_frame.image = img
            elif ((i+1)*20)-10 == self.Shop_rate or ( ((i+1)*20)-30 < self.Shop_rate and self.Shop_rate > 0):
                img = Image.open(MAIN_dir+"\\data\\Icon\\rating\\star1.png").resize((20, 20))
                img = ImageTk.PhotoImage(img)
                img_frame.config(image=img)
                img_frame.image = img
            else:
                img = Image.open(MAIN_dir+"\\data\\Icon\\rating\\star0.png").resize((20, 20))
                img = ImageTk.PhotoImage(img)
                img_frame.config(image=img)
                img_frame.image = img
                
    def change_rate_image(self, changeto):
        if self.Shop_rate == changeto:
            self.Shop_rate = changeto-20
        elif self.Shop_rate == changeto-10:
            self.Shop_rate = changeto
        else:
            self.Shop_rate = changeto-10
        self.load_rate_image()
        
    def change_shop_rate(self):
        self.Shop_rate = int(self.Shop_rate) + 10
        self.load_rate_image()
        
    def change_shop_image(self):
        file_source = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        dest_folder = MAIN_dir+"\\data\\Company\\"+ str(self.Shop_brand_name_entry.get()) + "\\"+ str(self.Shop_name_entry.get())
        imag_file_name  = "ProfileImage.jpg"
        # make sur folder is there
        os.makedirs(dest_folder, exist_ok=True)
        # join name and folder path
        dest_full_path = os.path.join(dest_folder, imag_file_name)
        # copy it to dest folder
        shutil.copy2(file_source, dest_full_path)
        self.load_shop_image()
        # TODO : MAKE SUIRE IT IS UPLODED TO WEBSITE 
            
    def load_shop_image(self):
        # load image
        #file = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if os.path.exists(MAIN_dir+"\\data\\Company\\"+ str(self.Shop_brand_name_entry.get()) + "\\"+ str(self.Shop_name_entry.get()) + "\\ProfileImage.jpg"):
            Shop_img = Image.open(MAIN_dir+"\\data\\Company\\"+ str(self.Shop_brand_name_entry.get()) + "\\"+ str(self.Shop_name_entry.get()) + "\\ProfileImage.jpg").resize((100, 100))
            Shop_img = ImageTk.PhotoImage(Shop_img)
            self.Shop_avatar_label.config(image=Shop_img)
            self.Shop_avatar_label.image = Shop_img
        else:
            # place holder
            shop_img = Image.open(MAIN_dir+"\\data\\Icon\\no_Profile_image.jpg").resize((100, 100))
            shop_img = ImageTk.PhotoImage(shop_img)
            self.Shop_avatar_label.config(image=shop_img)
            self.Shop_avatar_label.image = shop_img

    def change_Brand_image(self):
        file_source = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        dest_folder = MAIN_dir+"\\data\\Company\\"+ str(self.Shop_brand_name_entry.get())
        imag_file_name  = "ProfileImage.jpg"
        # make sur folder is there
        os.makedirs(dest_folder, exist_ok=True)
        # join name and folder path
        dest_full_path = os.path.join(dest_folder, imag_file_name)
        # copy it to dest folder
        shutil.copy2(file_source, dest_full_path)
        self.load_Brand_image()
        # TODO : MAKE SUIRE IT IS UPLODED TO WEBSITE 
        
    def load_Brand_image(self):
        # load Brand
        if os.path.exists(MAIN_dir+"\\data\\Company\\"+ str(self.Shop_brand_name_entry.get()) + "\\ProfileImage.jpg"):
            Brand_img = Image.open(MAIN_dir+"\\data\\Company\\"+ str(self.Shop_brand_name_entry.get()) + "\\ProfileImage.jpg").resize((100, 100))
            Brand_img = ImageTk.PhotoImage(Brand_img)
            self.Brand_avatar_label.config(image=Brand_img)
            self.Brand_avatar_label.image = Brand_img
        else:
            # place holder
            Brand_img = Image.open(MAIN_dir+"\\data\\Icon\\no_Profile_image.jpg").resize((100, 100))
            Brand_img = ImageTk.PhotoImage(Brand_img)
            self.Brand_avatar_label.config(image=Brand_img)
            self.Brand_avatar_label.image = Brand_img
        
    # shop profile  
    def load_shop_info(self):
        #print("loading shop info", self.Shops)
        shop_ = self.Shops[0]
        if shop_ != None and shop_ != []: 
            self.Shop_name_entry.delete(0, tk.END)
            self.Shop_name_entry.insert(0, str(shop_['Shop_name']))
            self.Shop_brand_name_entry.delete(0, tk.END)
            self.Shop_brand_name_entry.insert(0, str(shop_['Shop_brand_name']))

            self.load_shop_image()
            self.load_Brand_image()

            self.user_name_var.set(self.user_map_id.get(shop_['Shop_oweners_id'], ''))
            self.user_id_var.set(self.user_map.get(shop_['Shop_oweners_id'], ''))
            
            self.Shop_email_entry.delete(0, tk.END)
            self.Shop_email_entry.insert(0, str(shop_['Shop_email']))
            self.Shop_about_entry.delete(0, tk.END)
            self.Shop_about_entry.insert(0, str(shop_['Shop_about']))
            self.Shop_country_entry.delete(0, tk.END)
            self.Shop_country_entry.insert(0, str(shop_['Shop_country']))
            self.Shop_password_entry.delete(0, tk.END)
            self.Shop_password_entry.insert(0, str(shop_['Shop_password']))
            self.Shop_link_entry.delete(0, tk.END)
            self.Shop_link_entry.insert(0, str(shop_['Shop_link']))
            self.Shop_Contact_entry.delete(0, tk.END)
            self.Shop_Contact_entry.insert(0, str(shop_['Shop_contact']))
            self.Shop_startedDate_label.config(text="since "+str(str(shop_['Company_Started_Date']).split(" ")[0].split("-")[0]))
            if shop_['Shop_isenabled'] and shop_['Shop_isenabled'] == "1":
                self.Shop_isenabled_var.set(1)
            else:
                self.Shop_isenabled_var.set(0)
            self.Shop_types_var.set(str(shop_['Shop_type']))

            if shop_['Shop_rate'] and not shop_['Shop_rate'] == "":
                self.Shop_rate = int(shop_['Shop_rate'])

            
            self.Shop_slinks = str(shop_['Shop_SocLinks'])
            self.Shop_rules =str(shop_['Shop_rules'])
            
            #self.Shop_phone_num_entry.delete(0, tk.END)
            v = str(shop_['Shop_Adress_Information'])
            if v and "+" in v:
                infos = v.split("+")
                for l in infos:
                    info = l.split("=")
                    if "Location" == info[0]:
                        self.Shop_locations = info[1]+ "="
                    if "Phone Number" == info[0]:
                        self.Shop_phone_nums = info[1]+ "="
            self.load_Shop_phone_num()
            self.load_Shop_location()
            self.load_Shop_rules()
            self.load_Shop_slink()
    
                 
    def save_shop_info(self):
        # TODO : CHANGE SHOP SELECTED ONLY
        shop_ = self.Shops[0]
        if shop_:
            if shop_['Shop_Id']:
                idq = 'Shop_Id'
                idv = shop_['Shop_Id']
            else:
                idq = 'Id'
                idv = shop_['Id']
            self.user_id_var.set(self.user_map.get(str(self.user_name_var.get()), ''))
            self.Shop_name_entry.get()
            #'Shop_name'
            self.Shop_brand_name_entry.get()
            #'Shop_brand_name'
            self.user_id_var.get()
            #'Shop_oweners_id'
            self.Shop_email_entry.get()
            #'Shop_email'
            self.Shop_about_entry.get()
            #'Shop_about'
            self.Shop_country_entry.get()
            #'Shop_country'
            self.Shop_password_entry.get()
            #'Shop_password'
            self.Shop_link_entry.get()
            #'Shop_link'
            self.Shop_Contact_entry.get()
            #'Shop_contact'
            self.Shop_isenabled_var.get()
            #'Shop_isenabled'
            self.Shop_types_var.get()
            #'Shop_type'
            #self.Shop_rate
            #'Shop_rate'
            #self.Shop_slinks
            #'Shop_SocLinks'
            #self.Shop_rules
            #'Shop_rules'
            #shop_info
            #'Shop_Adress_Information'
            
            shop_info =  "Phone Number="+str(self.Shop_phone_nums)+"+Location="+str(self.Shop_locations)             
            s = Update_Shop(None, None, ['Shop_name', 'Shop_brand_name', 'Shop_oweners_id', 'Shop_email', 'Shop_about', 'Shop_country', 'Shop_password', 'Shop_link', 'Shop_contact', 'Shop_isenabled', 'Shop_type', 'Shop_rate', 'Shop_SocLinks', 'Shop_rules', 'Shop_Adress_Information'], [self.Shop_name_entry.get(), self.Shop_brand_name_entry.get(), self.user_id_var.get(), self.Shop_email_entry.get(), self.Shop_about_entry.get(), self.Shop_country_entry.get(), self.Shop_password_entry.get(), self.Shop_link_entry.get(), self.Shop_Contact_entry.get(), self.Shop_isenabled_var.get(), self.Shop_types_var.get(), self.Shop_rate, self.Shop_slinks, self.Shop_rules, shop_info], [idq], [idv])
            
            #  = fetch_as_dict_list("SELECT * FROM Shops WHERE " + idq + "=?", (str(idv),))
            if s:
                #print("s "+str(s))
                if isinstance(s, list) and len(s) > 0:
                    self.Shops = s
                    self.master.master.master.master.master.Shops[0] = s
                else:
                    self.Shops = [s]
                    self.master.master.master.master.master.Shops[0] = s            
                self.load_shop_info()
    # slip Settings
    def refrash_slip_order(self):
        if self.slip_order_list:
            self.slip_order_list_items.delete(0, tk.END)
            for order in self.slip_order_list[1]:
                if order:
                    #print("order "+str(order))
                    #print("str(slip_order_type[int(order)]) "+str(order[0]))
                    self.slip_order_list_items.insert(tk.END, str(slip_order_type[int(order[0])]))
            #print("displaying self.slip_order_list[1] ", self.slip_order_list[1])
            if not len(self.slip_order_list[0]) >= 2:
                self.slip_order_list[0] = ["40", "20"]

            self.slip_width_var.set(str(self.slip_order_list[0][0]))
            self.slip_hight_var.set(str(self.slip_order_list[0][1]))
            #self.slip_hight_entry.delete(0, tk.END)
            #self.slip_hight_entry.insert(0, str(self.slip_order_list[0][1]))
        else:
            self.slip_order_list = [["40", "20"], []]
                       
    def load_slip_order(self):
        selected_shop_index = self.User_Shopes_Combobox.current()
        if self.Shops[selected_shop_index]['Shop_Slip_Settings']:
            self.slip_order_list = json.loads(self.Shops[selected_shop_index]['Shop_Slip_Settings'])
        self.refrash_slip_order()
        
    def update_slip_order(self):
        selected_shop_index = self.User_Shopes_Combobox.current()
        slip_order_list_str = json.dumps(self.slip_order_list)
        self.Shops[selected_shop_index]['Shop_Slip_Settings'] = slip_order_list_str
        Update_table_database('UPDATE Shops SET Shop_Slip_Settings=? WHERE Shop_id=?', (slip_order_list_str, self.Shops[selected_shop_index]['Shop_Id']))
        #print("updated self.slip_order_list[1] ", self.slip_order_list[1])
        self.refrash_slip_order()

    def on_new_order_selected(self, *arg):
        #print("add self.slip_order_list[1] ", self.slip_order_list[1])
        self.slip_order_list[1].append([slip_order_type.index(str(self.slip_option_var.get()))])
        #print("added self.slip_order_list[1] ", self.slip_order_list[1])
        
        self.update_slip_order()
        
    def dele_slip_order(self):
        current_selection = self.slip_order_list_items.curselection()
        if not current_selection:
            return
        
        if self.slip_order_list:
            on = 0
            #print("self.slip_order_list[1] ", self.slip_order_list[1])
            #print("self.slip_order_list[1] len  ", len(self.slip_order_list[1]))
            for index in reversed(current_selection):
                del self.slip_order_list[1][index]
        self.update_slip_order()
        
    def move_slip_order(self, direc):
        current_selection = self.slip_order_list_items.curselection()
        if not current_selection:
            return
        move = 0
        if direc == "UP": #and current_index > 0:
            move = -1
        elif direc == "DOWN": #and current_index < self.slip_order_list_items.size()-1:
            move = 1
        else:
            return

        for index in current_selection:
            new_index = index + move
            if 0 <= new_index < len(self.slip_order_list[1]):
                self.slip_order_list[1][index], self.slip_order_list[1][new_index] = self.slip_order_list[1][new_index], self.slip_order_list[1][index]
                self.update_slip_order()
                self.slip_order_list_items.selection_set(new_index)

    def slip_width_changed(self, name, index, mode):
        self.slip_order_list[0][0] = self.slip_width_var.get()
        self.update_slip_order()
                        
    def slip_hight_changed(self, name, index, mode):
        self.slip_order_list[0][1] = self.slip_hight_var.get()
        self.update_slip_order()
        






















    
    def chacke_remaber_printer(self):
        #print("chacke_remaber_printer")
        if int(self.Remamber_printer_int.get()):
            b = fetch_as_dict_list("SELECT * FROM setting WHERE User_id = ?", (self.user['User_id'],))
            #print("user " + str(self.user[0]) + " found " +str(b))
            printers = list_available_printers()
            if b and len(b) > 0 and b[0][3] == "" or not b:
                dialog = PrinterSelectionDialog(self, printers)
                self.wait_window(dialog)
                selected_printer = dialog.selected_printer
                if selected_printer:
                    if dialog.issave.get():
                        if b:
                            Update_table_database('UPDATE setting SET printer=?, Get_printer=? WHERE User_id=?', ("", 1, self.user['User_id']))
                            
                        else:
                            Update_table_database('INSERT INTO setting (User_id, Get_printer, printer) VALUES (?, ?, ?, ?)', (self.user['User_id'], 1, selected_printer))
                                                
        else:
            Update_table_database('UPDATE setting SET printer=?, Get_printer=? WHERE User_id=?', ("", int(self.ask_seller_int.get()), self.user['User_id']))
            
            
    def chacke_ask_seller(self):
        #print("going to make seller ask or not...")
        Update_table_database('UPDATE setting SET Get_seller=? WHERE user_id=?', (int(self.ask_seller_int.get()), self.user['User_id']))
        

        
    def show_Setting_Form(self):
        # call the function in the main file to show the first frame
        self.master.master.show_frame("SettingForm")
        
    



    
    def create_sizes_form(self):
        selected_type = self.sizing_var.get()
        if selected_type == "Select Sizing Type":
            return

        self.form_frame.destroy()  # Clear previous form entries

        self.form_frame = tk.Frame(self.second_frame)
        self.form_frame.pack(pady=10)

        self.form_entries = []  # Reset the list of form entries

        sizes_label = tk.Label(self.form_frame, text="Enter Quantities for the Sizes:")
        sizes_label.pack()

        sizes_text = tk.Text(self.form_frame, height=5, width=40)
        sizes_text.pack()

        sizes = []
        if selected_type == "Trouser Sizes":
            sizes = [str(size) + ":0" for size in range(21, 46)]
        elif selected_type == "Clothing Sizes":
            sizes = ["XS:0", "S:0", "M:0", "L:0", "XL:0", "2XL:0", "3XL:0", "4XL:0", "5XL:0"]
        elif selected_type == "Shoe Sizes":
            sizes = [str(size) + ":0" for size in range(1, 13)] + [str(a) + ":0" for a in range(30, 45)]

        for size in sizes:
            sizes_text.insert(tk.END, size + ", ")

        done_button = tk.Button(self.form_frame, text="Done", command=lambda: self.generate_list(selected_type, sizes_text.get("1.0", tk.END)))
        done_button.pack()

    def generate_list(self, sizing_type, sizes):
        sizes_list = sizes.strip().split(",")  # Split the entered sizes by comma
        sizes_list = [size.strip() for size in sizes_list]  # Remove leading/trailing whitespaces

        self.result = []
        for size in sizes_list:
            size_parts = size.split(":")
            if len(size_parts) == 2:
                size_value = size_parts[0].strip()
                quantity = size_parts[1].strip()
                if quantity != "0":
                    self.result.append([size_value, quantity])
                    
        for v in self.result:
            found = 0 
            i = 0
            for p in self.inventory:
                if p["shop_name"] == self.shop_name_entry.get() and p["color"] == self.color_entry.get() and \
                p["size"] == v[0]:
                    if p["barcode"] == self.bracode_entry.get() and p["qtyfirst"] == v[1] and \
                        p["qty"] == v[1]:
                        #print("issame!!!" + str(p)) # TODO: show same earror
                        #    cdate#    update
                        pass
                    else:
                        self.inventory[i]["barcode"] = self.bracode_entry.get()
                        self.inventory[i]["qty"] = v[1]
                    found = 1
                else:
                    found = 0
                i += 1
            # TODO add stock pathern in this new list
            found, self.nested_list = add_new_list(self.nested_list, self.shop_name_entry.get() + "|" + self.code_entry.get() + "|" + self.color_entry.get() + "|" + v[0], [self.bracode_entry.get(), v[1], v[1], "", self.images_entry.get(), "", ""])
            if found:
                self.add_info_(self.shop_name_entry.get(), self.code_entry.get(), self.color_entry.get(), v[0], self.bracode_entry.get(), v[1], v[1], "", "")
        txt = self.get_inventory_nested_list_text()
        self.more_info_label.delete(0, tk.END)
        self.more_info_label.insert(0, txt)

        
        
    def Item_To_Update(self):
        #self.info_tab = None
        # Notebook widget - CENTER_NOTEBOK

        self.Item_To_Update_tab = ttk.Frame(self.Product_notebook)
        self.Item_To_Update_tab.grid()

        # Add tabs to the self.center_notebook
        self.Product_notebook.add(self.Item_To_Update_tab, text='Item_To_Update')

        self.Item_To_Update_tab.grid_columnconfigure(0, weight=5)
        self.Item_To_Update_tab.grid_columnconfigure(1, weight=5)
        self.Item_To_Update_tab.grid_columnconfigure(2, weight=5)
        self.Item_To_Update_tab.grid_columnconfigure(3, weight=5)
        self.Item_To_Update_tab.grid_columnconfigure(4, weight=5)
        self.Item_To_Update_tab.grid_columnconfigure(5, weight=5)
        self.Item_To_Update_tab.grid_columnconfigure(6, weight=5)
        self.Item_To_Update_tab.grid_rowconfigure(0, weight=5)
        self.Item_To_Update_tab.grid_rowconfigure(1, weight=5)
        self.Item_To_Update_tab.grid_rowconfigure(2, weight=5)
        self.Item_To_Update_tab.grid_rowconfigure(3, weight=5)
        self.Item_To_Update_tab.grid_rowconfigure(4, weight=5)
        
        self.Item_To_Update_tab_details_frame = tk.Frame(self.Item_To_Update_tab)
        self.Item_To_Update_tab_details_frame.grid(row=0, column=0, columnspan=6)

        
        # Create the label and entry for the document expire date search
        self.Item_To_Update_tab_date_entry = tk.Label(self.Item_To_Update_tab_details_frame, text="Document Updated Date:")
        self.Item_To_Update_tab_date_entry.grid(row=2, column=5)
        self.Item_To_Update_tab_entry = tk.Entry(self.Item_To_Update_tab_details_frame)
        self.Item_To_Update_tab_entry.grid(row=3, column=5)

        # Create the search button
        self.Item_To_Update_tab_search_button = tk.Button(self.Item_To_Update_tab_details_frame, text="Search", command=self.perform_search)
        self.Item_To_Update_tab_search_button.grid(row=3, column=6)

        # Create the search button
        self.Item_To_Update_tab_print_button = tk.Button(self.Item_To_Update_tab_details_frame, text="Print", command=self.perform_print)
        self.Item_To_Update_tab_print_button.grid(row=4, column=1)

        self.Item_To_Update_tab_upload_button = tk.Button(self.Item_To_Update_tab_details_frame, text="Refresh", bg="red", fg="white", font=("Arial", 12), command=lambda: self.perform_search_Item_size_chack())
        self.Item_To_Update_tab_upload_button.grid(row=4, column=2)


        # Create the listbox to display search results
        self.Item_To_Update_tab_listbox = ttk.Treeview(self.Item_To_Update_tab)        
        self.Item_To_Update_tab_listbox.bind('<<TreeviewSelect>>', self.on_select)
        #self.listbox.bind("<Button-1>", self.on_treeview_double_click)
        #self.listbox.grid_propagate(False)


        # Add vertical scrollbar
        tree_scrollbar_y = ttk.Scrollbar(self.Item_To_Update_tab_listbox, orient='vertical', command=self.Item_To_Update_tab_listbox.yview)
        self.Item_To_Update_tab_listbox.configure(yscrollcommand=tree_scrollbar_y.set)
        tree_scrollbar_y.pack(side='right', fill='y')

        # Add horizontal scrollbar
        tree_scrollbar_x = ttk.Scrollbar(self.Item_To_Update_tab_listbox, orient='horizontal', command=self.Item_To_Update_tab_listbox.xview)
        self.Item_To_Update_tab_listbox.configure(xscrollcommand=tree_scrollbar_x.set)
        tree_scrollbar_x.pack(side='bottom', fill='x')

        # Set the size of the self.listbox widget
        self.Item_To_Update_tab_listbox.grid(row=1, column=0, rowspan=3, columnspan=5, sticky="nsew")
        self.get_columen_()
        
        # New listbox in the main frame
        self.Item_To_Update_tab_list_items = tk.Listbox(self.Item_To_Update_tab, bg="yellow", height=17)
        self.Item_To_Update_tab_list_items.grid(row=1, column=5, rowspan=2, sticky="nsew")
        '''self.doc_total_unpaid = tk.Label(self.home_tab, text="Amount Unpid:", font=("Arial", 11))
        self.doc_total_unpaid.grid(row=3, column=5)
        self.doc_total_paid = tk.Label(self.home_tab, text="Amount pid:", font=("Arial", 12))
        self.doc_total_paid.grid(row=4, column=5)
        self.doc_total_ = tk.Label(self.home_tab, text="Totale :", font=("Arial", 15))
        self.doc_total_.grid(row=5, column=5)'''

        # show the Payment Form window
















        
    def get_columen_(self):
        self.Item_To_Update_tab_listbox['columns'] = ('doc_barcode', 'extension_barcode', 'user_id', 'customer_id', 'Type', 'Itmes', 'Qty', 'Paymen', 'price', 'disc', 'tax', 'doc_created_date', 'doc_expire_date', 'doc_updated_date')
        self.Item_To_Update_tab_listbox.heading("#0", text="ID")
        self.Item_To_Update_tab_listbox.column("#0", stretch=tk.NO, minwidth=25, width=50) 
        self.Item_To_Update_tab_listbox.heading("#1", text="doc_barcode")
        self.Item_To_Update_tab_listbox.column("#1", stretch=tk.NO, minwidth=25, width=100) 
        self.Item_To_Update_tab_listbox.heading("#2", text="extension_barcode")
        self.Item_To_Update_tab_listbox.column("#2", stretch=tk.NO, minwidth=25, width=100) 
        self.Item_To_Update_tab_listbox.heading("#3", text="user_id")
        self.Item_To_Update_tab_listbox.column("#3", stretch=tk.NO, minwidth=25, width=100) 
        self.Item_To_Update_tab_listbox.heading("#4", text="customer_id")
        self.Item_To_Update_tab_listbox.column("#4", stretch=tk.NO, minwidth=25, width=100) 
        self.Item_To_Update_tab_listbox.heading("#5", text="Type")
        self.Item_To_Update_tab_listbox.column("#5", stretch=tk.NO, minwidth=25, width=80) 
        self.Item_To_Update_tab_listbox.heading("#6", text="Itmes")
        self.Item_To_Update_tab_listbox.column("#6", stretch=tk.NO, minwidth=25, width=100) 
        self.Item_To_Update_tab_listbox.heading("#7", text="Qty")
        self.Item_To_Update_tab_listbox.column("#7", stretch=tk.NO, minwidth=25, width=100) 
        self.Item_To_Update_tab_listbox.heading("#8", text="price")
        self.Item_To_Update_tab_listbox.column("#8", stretch=tk.NO, minwidth=25, width=50) 
        self.Item_To_Update_tab_listbox.heading("#9", text="disc")
        self.Item_To_Update_tab_listbox.column("#9", stretch=tk.NO, minwidth=25, width=50) 
        self.Item_To_Update_tab_listbox.heading("#10", text="tax")
        self.Item_To_Update_tab_listbox.column("#10", stretch=tk.NO, minwidth=25, width=50) 
        self.Item_To_Update_tab_listbox.heading("#11", text="Payment")
        self.Item_To_Update_tab_listbox.column("#11", stretch=tk.NO, minwidth=25, width=100) 
        self.Item_To_Update_tab_listbox.heading("#12", text="doc_created_date")
        self.Item_To_Update_tab_listbox.column("#12", stretch=tk.NO, minwidth=25, width=100) 
        self.Item_To_Update_tab_listbox.heading("#13", text="doc_expire_date")
        self.Item_To_Update_tab_listbox.column("#13", stretch=tk.NO, minwidth=25, width=100) 
        self.Item_To_Update_tab_listbox.heading("#14", text="doc_updated_date")
        self.Item_To_Update_tab_listbox.column("#14", stretch=tk.NO, minwidth=25, width=100) 

    def perform_search_Item_size_chack(self):
        item = fetch_as_dict_list(self.homemaster.Link, 'SELECT * FROM product', ())
        
        for it in item:
            #print("item["+str(it[0])+"]  : " + str(it[12]))
            qty_info_list = []
            if "\"{" in str(it[12]):
                qty_info_list = read_code(it[12], "", str(it[2]), "", "")[4]
            else:
                qty_info_list = load_list(it[12])
            
            def sub_list(ls):
                main_name = []
                for l in ls:
                    if len(l) > 2:
                        # chacke size has problame
                        if float(l[2]) < 0:
                            self.Item_To_Update_tab_listbox.insert("", 'end', text="Size", values=(it[1], it[2], it[3], it[4], it[5], it[6], it[7], it[8], it[9], it[10], it[11], it[12], it[13], it[14]))
                        
                    elif len(l) == 2:
                        #main_name.append(l[0])
                        sub_list(l[1])
            sub_list(qty_info_list)
                
    
    def perform_print(self):
        # todo make it print by catagory
        print_slip = "Name   |  code    |       "
        for item in self.Item_To_Update_tab_listbox.get_children():
            item_text = self.Item_To_Update_tab_listbox.item(item, "values")
            print_slip += item_text[0] + "  :  " + item_text[1] + "\n"
        self.user = self.master.user
        PrinterForm.print_slip(self, print_slip, 1) # TODO chack in setting if paper cut allowed

    def perform_search(self):
        self.pyment_used = []
        # Get the search criteria from the entry boxes
        doc_id = self.doc_id_entry.get()
        doc_type = self.type_entry.get_value  #"self.doc_type_entry.get()"
        doc_barcode = self.doc_barcode_entry.get()
        extension_barcode = self.extension_barcode_entry.get()
        item = self.item_entry.get()
        user_id = self.user_id_entry.get()
        customer_id = self.customer_id_entry.get()
        sold_item_info = self.sold_item_info_entry.get()
        discount = self.discount_entry.get()
        tax = self.tax_entry.get()
        doc_created_date = self.doc_created_date_entry.get()
        doc_expire_date = self.doc_expire_date_entry.get()
        doc_updated_date = self.doc_updated_date_entry.get()

        # Perform the search and update the listbox with the results
        df = search_documents(doc_id, doc_type, doc_barcode, extension_barcode, item, user_id, customer_id,
                            sold_item_info, discount, tax, doc_created_date, doc_expire_date, doc_updated_date)
        self.listbox.delete(*self.listbox.get_children())
        #self.get_columen()
        for index in df:
            #print("df : " + str(index))
            item = self.listbox.insert('', 'end', text=index[0], values=(index[1], index[2], index[3], index[4], index[5], index[6], index[7], index[8], index[9], index[10], index[11], index[12], index[13], index[14]))
            #  payment
            self.load_payment(index[11])
        
        self.creat_info()
            
    def load_payment(self, p_text):
        #print("tiems : " + str(p_text))
        if ")" in str(p_text) or ")," in str(p_text):
            items_lists = (p_text + ",").split("),")
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
                found = 0
                for pay in self.pyment_used:
                    if pay[0] == pay_type:
                        found = 1
                        pay[1] += float(pay_pid)
                        break
                if found == 0:
                    #print("new payment :" + str([pay_type, pay_pid]))
                    self.pyment_used.append([pay_type, float(pay_pid)])
                index += 1

        elif "," in str(p_text):
            items_lists = self.items[10].split(",")
            index = 0
            for p in range(len(items_lists)-1):
                item = items_lists[p].split(" = ")
                #print("item :" + str(item))
                #for each items
                name = item[0].replace("(:", "")
                price = item[1]
                #print("list : " + str([name, price]))
                
                index += 1
        else:
            item = str(p_text).split(" = ")
            #print("item :" + str(item))
            if len(item) > 1:
                name = item[0].replace("(:", "")
                price = item[1]
                self.list_payment.insert("", 'end', text="0", values=(name, price, self.created_date, self.created_date, self.created_user))
        
    def display_products(self, products, ind):
            self.product_list.delete(0, tk.END)
            for product in products[ind]:
                self.product_list.insert(tk.END, f"{product[0]}  {product[1]}")
                
    def format_price(self, price):
        suffixes = ['Hundred', 'Thousand', 'Million', 'Billion']
        suffic_index = 0
        nprice = price
        while nprice >= 1000 and suffic_index < len(suffixes):
            nprice /= 1000
            suffic_index += 1
        if suffic_index == 0:
            formatted_price = "{:,.0f} {}".format(nprice *100, suffixes[suffic_index])
        else:
            formatted_price = "{:,.2f} {}".format(nprice, suffixes[suffic_index])
        return formatted_price

    def add_info_(self, shop_name, code, color, size, barcode, qtyfirst, qty, stock, img, cdate, update):
        p = {"shop_name": shop_name, "code": code, "color": color, "size": size, "barcode": barcode, "qtyfirst": qtyfirst, "qty": qty, "cdate": cdate, "update": update}
        self.inventory.append(p)
        self.update_tree()

    def get_unique_shop_names(self):
        return list(set([p["shop_name"] for p in self.inventory]))

    def get_unique_codes_for_shop_name(self, shop_name):
        return list(set([p["code"] for p in self.inventory if p["shop_name"] == shop_name]))

    def get_unique_colors_for_shop_name(self, shop_name, code):
        return list(set([p["color"] for p in self.inventory if p["shop_name"] == shop_name and p["code"] == code]))

    def get_sizes_for_shop_name_and_color(self, shop_name, code, color):
        return list(set([p["size"] for p in self.inventory if p["shop_name"] == shop_name and p["code"] == code and p["color"] == color]))

    def get_barcode_and_qty_for_shop_name_and_color_and_size(self, shop_name, code, color, size):
        for p in self.inventory:
            if p["shop_name"] == shop_name and p["code"] == code and p["color"] == color and p["size"] == size:
                return (p["barcode"], p["qtyfirst"], p["qty"], p["cdate"], p["update"])
        return (None, None)
    
    def chang_to_list(self, vs_info):
        '''a_u_list = []
        t = vs_info.replace("\"", "") + ","
        main_info = t.split("},")
        for m in range(len(main_info)-1):
            main_value = main_info[m].split(",(")
            shop_name = main_value[0].replace("{", "")
            shop = [shop_name]
            shop_node = []
            t = main_value[1].replace(")", "") + ","
            f_info = t.split(">,")
            for c in range(len(f_info)-1):
                f_value = f_info[c].split(",[")
                color_txt = f_value[0].replace("<", "")
                color = [color_txt]
                color_node = []
                t = f_value[1].replace("]", "") + ","
                s_info = t.split("|,")
                for s in range(len(s_info)-1):
                    s_value = s_info[s].split(", ")
                    s_n = []
                    for s_v in s_value:
                        s_n.append(s_v.replace("|", ""))
                    color_node.append(s_n)
                color.append(color_node)
                shop_node.append(color)
            shop.append(shop_node)
            a_u_list.append(shop)
        return a_u_list'''

    def chang_to_text(self, a_u_list):
        '''vs_info = "\""
        si = 0
        for s in a_u_list:
            si += 1
            vs_info += '{'
            vs_info += s[0]
            vs_info += ',('
            ci = 0
            for c in s[1]:
                ci += 1
                vs_info += '<'
                vs_info += c[0]
                vs_info += ',['
                sei = 0
                for se in c[1]:
                    vs_info += '|'
                    sei += 1
                    for j in range(len(se)):
                        vs_info += se[j]
                        if j < len(se)-1:
                            vs_info += ', '
                    if sei < len(c[1])-1:
                        vs_info += ',|'
                    else:
                        vs_info += '|'
                vs_info += ']'
                if ci < len(s[1])-1:
                    vs_info += ',>'
                else:
                    vs_info += '>'
            vs_info += ')'
            if si < len(a_u_list)-1:
                vs_info += ',}'
            else:
                vs_info += '}'
        vs_info += "\""
        return vs_info'''
    
    def add_product_from_nested_list(self, nested_list):
        for s in nested_list:
            if not s:
                break
            shop_name, nested_items = s
            color, nested_items2 = nested_items
            size, nested_items3 = nested_items2
            #print("shop name : " + shop_name)
            #print("shop nested_item : " + str(nested_items))
            barcode, qtyfirst, qty, cdate, update = nested_items3
            self.add_info_(shop_name, color, size, barcode, qtyfirst, qty, cdate, update)
    
    def get_inventory_nested_list(self, text, code):
        '''nested_list = []
        unique_shop_names = self.get_unique_shop_names()
        for shop_name in unique_shop_names:
            shop_node = [shop_name]
            unique_colors = self.get_unique_colors_for_shop_name(shop_name)
            shop_subnode = []
            for color in unique_colors:
                color_nodes = [color]
                sizes = self.get_sizes_for_shop_name_and_color(shop_name, color)
                color_subnodes = []
                for size in sizes:
                    barcode, qtyfirst, qty, cdate, update = self.get_barcode_and_qty_for_shop_name_and_color_and_size(shop_name, color, size)
                    color_subnodes.append([size, barcode, qtyfirst, qty, cdate, update])
                color_nodes.append(color_subnodes)
                shop_subnode.append(color_nodes)
            shop_node.append(shop_subnode)
            nested_list.append(shop_node)
        return nested_list'''
        if "\"{" in str(text):
            self.nested_list = read_code(text, "", str(code), "", "")[4]
        else:
            self.nested_list = load_list(text) 

    def get_inventory_nested_list_text(self): # change tree vew nested list to text
        '''vs_info = '\"'
        unique_shop_names = self.get_unique_shop_names()
        s = 0
        for shop_name in unique_shop_names:
            vs_info += '{'
            vs_info += shop_name + ',('
            unique_colors = self.get_unique_colors_for_shop_name(shop_name)
            c = 0
            for color in unique_colors:
                vs_info += '<'
                vs_info += color + ',['
                sizes = self.get_sizes_for_shop_name_and_color(shop_name, color)
                i = 0
                for size in sizes:
                    vs_info += '|' 
                    vs_info += size + ','
                    v, n, m, g, y = self.get_barcode_and_qty_for_shop_name_and_color_and_size(shop_name, color, size)
                    vs_info += str(v + "," + n + "," + m + "," + g + "," + y)
                    if i < len(sizes)-1:
                        vs_info += '|,'
                    else:
                        vs_info += '|'
                    i += 1
                vs_info += ']'
                if c < len(unique_colors)-1:
                    vs_info += '>,'
                else:
                    vs_info += '>'
                c += 1 
            vs_info += ')'
            if s < len(unique_shop_names)-1:
                vs_info += '},'
            else:
                vs_info += '}'
            s += 1
        vs_info += '\"'
        return vs_info'''
        return str(self.nested_list)
    
    def update_tree(self):
        self.tree.delete(*self.tree.get_children())
        #print("gount tot add tree ")
        for shop in self.nested_list:
            #print("shop")
            shop_name_node = self.tree.insert("", "end", text=shop[0])
            for code in shop[1]:
                #print("code")
                code_node = self.tree.insert(shop_name_node, "end", text=code[0])
                for color in code[1]:
                    color_node = self.tree.insert(code_node, "end", text=color[0])
                    for size in color[1]:
                        size_node = self.tree.insert(color_node, "end", text=size[0])
                        for value in size[1]:
                            #print("value : " + str(value))
                            barcode, qtyfirst, qty, patern, imgs, cdate, update = value
                            if barcode and qtyfirst and qty and cdate and update:
                                self.tree.insert(size_node, "end", text=value[0], values=(barcode, qtyfirst, qty, cdate, update))
                            else:
                                self.tree.insert(size_node, "end", text=value[0])
                            
    def remove_info(self):
        """self.more_info_label = tk.Label(self.tab3_frame, text='More Info:')
        self.more_info_label.grid(row=1, column=0, sticky=tk.E)

        self.list_box2 = ttk.Treeview(self.tab3_frame)
        self.list_box2.grid(row=2, column=0, sticky=tk.E)

        self.shop_name_entry = tk.Entry(self.tab3_frame)
        self.color_label = tk.Label(self.tab3_frame, text='Price Change:')
        self.color_label.grid(row=8, column=0, sticky=tk.E)
        self.color_entry = tk.Entry(self.tab3_frame)
        self.color_entry.grid(row=8, column=1, sticky=tk.E)
        self.size_label = tk.Label(self.tab3_frame, text='Price Change:')
        self.size_label.grid(row=9, column=0, sticky=tk.E)
        self.size_entry = tk.Entry(self.tab3_frame)
        self.size_entry.grid(row=9, column=1, sticky=tk.E)
        self.qty_label = tk.Label(self.tab3_frame, text='Quantity:')
        self.qty_label.grid(row=10, column=0, sticky=tk.E)
        self.qty_entry = tk.Entry(self.tab3_frame)
        self.qty_entry.grid(row=10, column=1, sticky=tk.E)
        self.bracode_label = tk.Label(self.tab3_frame, text='Barcode : ')
        self.bracode_label.grid(row=11, column=0, sticky=tk.E)
        self.bracode_entry = tk.Entry(self.tab3_frame)
        self.bracode_entry.grid(row=11, column=1, sticky=tk.E)
        for a in self.tree.get_children():
            self.tree.delete(a)
            for a in self.list_items.selection():
            self.list_items.delete(a)
        self.update_info()
        self.update_info()
        """
        found = 0 
        i = 0
        for a in self.tree.selection():
            #print(str(self.tree.item(a)))
            for p in self.inventory:
                if p["shop_name"] == self.shop_name_entry.get() and p["color"] == self.color_entry.get() and \
                p["size"] == self.size_entry.get():
                    if p["barcode"] == self.bracode_entry.get() and p["qtyfirst"] == self.qty_entry.get() and \
                        p["qty"] == self.qty_entry.get():
                        #print("issame!!!" + str(p)) # TODO: show same earror
                        #    cdate#    update
                        pass
                    else:
                        self.inventory[i]["barcode"] = self.bracode_entry.get()
                        self.inventory[i]["qty"] = self.qty_entry.get()
                    found = 1
                else:
                    found = 0
                i += 1
            self.tree.delete(a)
        
        found, self.nested_list = dele_list(self.nested_list, self.shop_name_entry.get() + "|" + self.code_entry.get() + "|" + self.color_entry.get() + "|" + self.size_entry.get() , [self.bracode_entry.get(), self.qty_entry.get(), self.qty_entry.get(), "", self.images_entry.get(), "", ""])
        txt = self.get_inventory_nested_list_text()
        #l = self.get_inventory_nested_list()
        #print("list : " + str(l))
        #txt = self.chang_to_text(l)
        #print("list : " + str(txt))
        #le = self.chang_to_list(txt)
        #print("le :" + str(le))
        self.more_info_label.delete(0, tk.END)
        self.more_info_label.insert(0, txt)
        
    def add_info(self):
        """self.more_info_label = tk.Label(self.tab3_frame, text='More Info:')
        self.more_info_label.grid(row=1, column=0, sticky=tk.E)

        self.list_box2 = ttk.Treeview(self.tab3_frame)
        self.list_box2.grid(row=2, column=0, sticky=tk.E)

        self.shop_name_entry = tk.Entry(self.tab3_frame)
        self.color_label = tk.Label(self.tab3_frame, text='Price Change:')
        self.color_label.grid(row=8, column=0, sticky=tk.E)
        self.color_entry = tk.Entry(self.tab3_frame)
        self.color_entry.grid(row=8, column=1, sticky=tk.E)
        self.size_label = tk.Label(self.tab3_frame, text='Price Change:')
        self.size_label.grid(row=9, column=0, sticky=tk.E)
        self.size_entry = tk.Entry(self.tab3_frame)
        self.size_entry.grid(row=9, column=1, sticky=tk.E)
        self.qty_label = tk.Label(self.tab3_frame, text='Quantity:')
        self.qty_label.grid(row=10, column=0, sticky=tk.E)
        self.qty_entry = tk.Entry(self.tab3_frame)
        self.qty_entry.grid(row=10, column=1, sticky=tk.E)
        self.bracode_label = tk.Label(self.tab3_frame, text='Barcode : ')
        self.bracode_label.grid(row=11, column=0, sticky=tk.E)
        self.bracode_entry = tk.Entry(self.tab3_frame)
        self.bracode_entry.grid(row=11, column=1, sticky=tk.E)
        """
        found = 0 
        i = 0
        for p in self.inventory:
            if p["shop_name"] == self.shop_name_entry.get() and p["color"] == self.color_entry.get() and \
               p["size"] == self.size_entry.get():
                if p["barcode"] == self.bracode_entry.get() and p["qtyfirst"] == self.qty_entry.get() and \
                    p["qty"] == self.qty_entry.get():
                    #print("issame!!!" + str(p)) # TODO: show same earror
                    #    cdate#    update
                    pass
                else:
                    self.inventory[i]["barcode"] = self.bracode_entry.get()
                    self.inventory[i]["qty"] = self.qty_entry.get()
                found = 1
            else:
                found = 0
            i += 1

        #{'shop_name': '1', 'color': '2', 'size': '3', 'barcode': '4', 'qtyfirst': '4', 'qty': '4', 'cdate': '', 'update': ''}
                #return (p["barcode"], p["qtyfirst"], p["qty"], p["cdate"], p["update"])
        found, self.nested_list = add_new_list(self.nested_list, self.shop_name_entry.get() + "|" + self.code_entry.get() + "|" + self.color_entry.get() + "|" + self.size_entry.get() , [self.bracode_entry.get(), self.qty_entry.get(), self.qty_entry.get(), "", self.images_entry.get(), "", ""])
        #print("self.nested_list : " + str(self.nested_list))
        if found:
            self.add_info_(self.shop_name_entry.get(), self.code_entry.get(), self.color_entry.get(), self.size_entry.get(), self.bracode_entry.get(), self.qty_entry.get(), self.qty_entry.get(), "", self.images_entry.get(), "", "")
            
            

        txt = self.get_inventory_nested_list_text()
        #l = self.get_inventory_nested_list()
        #print("list : " + str(l))
        #txt = self.chang_to_text(l)
        #print("list : " + str(txt))
        #le = self.chang_to_list(txt)
        #print("le :" + str(le))
        self.more_info_label.delete(0, tk.END)
        self.more_info_label.insert(0, txt)
        

        
    
    # Create the "Delete" button
    
    # Define the function for deleting a product
    def delete_product(self):
        # Get the selected product from the listbox
        for selected_product in self.list_box.selection():
            # Get the ID of the selected product
            product_id = self.list_box.item(selected_product)['text']
            # Delete the product from the database
            Update_table_database('DELETE FROM product WHERE id=?', (int(product_id),))


            # Clear the product details widgets
            self.clear_product_details_widget()

            # Update the product listbox
            self.update_product_listbox()

    def get_item_by_code(self, item_code):
        result = fetch_as_dict_list("SELECT * FROM product WHERE code=?", (item_code,))
        
        return result
    
    def update_item_info(self, id, code, it_info):
        pass




    
    def search_products(self, search_text):
        # Search for the entered text in the code, name, barcode, and type fields of the product table
        results = fetch_as_dict_list("SELECT * FROM product WHERE code LIKE ? OR name LIKE ? OR barcode LIKE ? OR type LIKE ?", 
                    ('%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%'))
        
        return results

    # create a function to update the search results whenever the search box changes
    def update_search_results(self, *args):
        # get the search string from the search box
        search_str = self.search_var.get()
        
        # search for products based on the search string
        products = self.search_products(search_str)
        
        # clear the current items in the list box
        self.list_box.delete(*self.list_box.get_children())

        # Add the products to the product listbox
        for product in products:
            self.list_box.insert('', 'end', values=(product[0], product[1], product[2], product[3], product[4], product[5], product[6],product[7], product[8], product[9], product[10], product[11], product[12], product[13],product[14], product[15], product[16], product[17]))
        
    # Define the function for updating the product listbox
    def update_product_listbox(self):
        # Clear the product listbox
        self.list_box.delete(*self.list_box.get_children())
        # Get the products from the database
        Update_table_database('SELECT * FROM product')
        products = cur.fetchall()
        items = 0
        TQTY = 0
        Tprice = 0
        Tcost = 0
        vv = []
        item = cur.fetchall()
        for product in products:
            self.list_box.insert('', 'end', values=(product[0], product[1], product[2], product[3], product[4], product[5], product[6],product[7], product[8], product[9], product[10], product[11], product[12], product[13],product[14], product[15], product[16], product[17]))
            chacksize = 0
            cost = float(product[7])
            price = float(product[9])
            qty_info_list = []
            if "\"{" in str(product[12]):
                qty_info_list = read_code(product[12], "", str(product[2]), "", "")[4]
            else:
                qty_info_list = load_list(product[12])
            items += 1
            qty = 0
            def sub_list(ls, qty):
                main_name = []
                for l in ls:
                    if len(l) > 2:
                        qty += float(l[2])
                    elif len(l) == 2:
                        #main_name.append(l[0])
                        qty = sub_list(l[1], qty)
                return qty
            qty = sub_list(qty_info_list, qty)
            vv.append([str(product[0]), float(price)])
            # TODO make user choosh in which name, code, id
            if qty > 0:
                #print("Calculating : " + "qty " + str(qty) + "*" + str(price) + " price = " + str(qty*price) + "  AND QTY * " + str(cost) + " Cost = " + str(qty*cost))
                #print("equal Tprice : " + str(Tprice) + " Cost :" + str(Tcost))
                Tprice += qty*price
                Tcost += qty*cost
                TQTY += qty
        if len(vv) > 0:
            self.graph_value, self.graph_value0, tilte = make_list(vv)
        
            #print("pself.graph_value0 :" + str(self.graph_value0))
            draw_cart(int(self.style_var.get()), self.chart_canvas, self.next_button, self.prev_button, self.graph_value0, int(self.which_var.get()), 1, 0)
            draw_cart(int(self.style_var.get()), self.chart2_canvas, None, None, self.graph_value0, int(self.which_var.get()), 1, 0)
            self.display_products(self.graph_value0, int(self.which_var.get()))
            
        self.total_item_label.config(text="TOTAL ITEM COUNT : " + str(items))
        self.total_qty_label.config(text="TOTAL QTY COUNT : " + str(TQTY))
        self.total_cost_label.config(text="TOTAL COST : " + str(Tcost) + "  (" +str(self.format_price(Tcost)) + ")" )
        self.total_sale_label.config(text="TOTAL AFTER SALE : " + str(Tprice) + "  (" +str(self.format_price(Tprice)) + ")")

        # Hide the product details frame
        self.hide_add_product_forme()
        self.change_button.config(state=tk.DISABLED)








    def on_select(self, event):
        if len(event.widget.selection()) > 0:
            self.change_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.NORMAL)
        else:
            self.change_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)

    def on_name_entry(self, event):
        Update_table_database('SELECT * FROM product')
        products = cur.fetchall()
        for product in products:
            #TODO MAKE IT EASY BY ID
            #print("on_name_entry\n"+str(product[1]))
            if product[1] == self.name_entry.get():
                self.add_button.config(text="Update")    
                return
        if self.main_name == self.name_entry.get() and not self.main_name == "":
            self.add_button.config(text="Update")
        else:
            self.add_button.config(text="New")

    def clear_product_details_widget(self):
        # Clear the product details widgets
        self.name_entry.delete(0, tk.END)
        self.code_entry.delete(0, tk.END)
        #self.type_entry.delete(0, tk.END) self.type_entry
        #self.barcode_entry.delete(0, tk.END)
        #self.at_shop_entry.delete(0, tk.END)
        #self.quantity_entry.delete(0, tk.END)

        self.inventory = []
        # Clear the product tree
        self.tree.delete(*self.tree.get_children())
        self.shop_name_entry.delete(0, tk.END)
        self.color_entry.delete(0, tk.END)
        self.size_entry.delete(0, tk.END)
        self.qty_entry.delete(0, tk.END)
        self.bracode_entry.delete(0, tk.END)

        
        self.cost_entry.delete(0, tk.END)
        self.tax_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.include_tax_var.set(0)
        self.price_change_var.set(0)
        self.more_info_label.delete(0, tk.END)
        self.images_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.service_change_var.set(0)
        self.default_quantity_change_var.set(0)
        self.active_var.set(0)

        self.qty_entry.insert(0, "0")
        self.size_entry.insert(0, "Def_size")
        self.color_entry.insert(0, "Def_color")
        self.code_entry.insert(0, "Def_code")
        self.shop_name_entry.insert(0, "SHOP_NAME") # todo add shop name


    # Create the "Add New" button
    # Define the function for showing the product details frame
   
    def hide_add_product_forme(self):
        self.clear_product_details_widget()
        # Hide the add product button
        self.notebook_frame.pack_forget()

    
    # Define the function for deleting a product
    def delete_product(self):
        # Get the selected product from the listbox
        selected_product = self.list_box.selection()

        if selected_product:
            # Get the ID of the selected product
            product_id = self.list_box.item(selected_product)['values'][0]
        
            # Delete the product from the database
            Update_table_database('DELETE FROM product WHERE id=?', (product_id,))

            # Update the product listbox
            self.update_product_listbox()

    # Define the function for adding a new product
    def add_product(self):
        # Get the values from the product details widgets
        # Get the values from the product details widgets
        name = self.name_entry.get()
        code = self.code_entry.get()
        typ = self.type_entry.get_value
        barcode = ""
        #self.barcode_entry.get()
        at_shop = ""
        # self.at_shop_entry.get()
        quantity = 0
        # self.quantity_entry.get()
        cost = float(self.cost_entry.get())
        tax = float(self.tax_entry.get())
        price = float(self.price_entry.get())
        include_tax = int(self.include_tax_var.get())
        price_change = int(self.price_change_var.get())
        more_info = self.more_info_label.get()
        images = self.images_entry.get()
        description = self.description_entry.get()
        service = self.service_change_var.get()
        default_quantity = int(self.default_quantity_change_var.get())
        active = int(self.active_var.get())
            
        #print(str([name, code, typ, barcode, at_shop, quantity, cost, tax, price, include_tax, price_change, more_info, images, description, service, default_quantity, active]))
        
        item = ""
        doc_type = ""
        brcod = 0
        b = fetch_as_dict_list("SELECT * FROM setting WHERE user_name=?", (self.master.master.master.master.user,))
        
        if not len(b)<= 0:
            brcod = b[2] # getting barcode
        brcod += 1
        if self.add_button.cget("text") == "New":        
            # Insert the new product into the database
            doc_type = "Add_Items"
            # Get the ID of the most recently added item
            Update_table_database('INSERT INTO product (name, code, type, barcode, at_shop, quantity, cost, tax, price, include_tax, price_change, more_info, images, description, service, default_quantity, active) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (name, code, typ, barcode, at_shop, quantity, cost, tax, price, include_tax, price_change, more_info, images, description, service, default_quantity, active))
            new_item_id = fetch_as_dict_list("SELECT last_insert_rowid()")[0]
            #print("new_product_id : " + str(new_item_id) + " barcode : " + str(brcod))
            item += f"(:{new_item_id}:,:{name}:,:{code}:,:{typ}:,:{barcode}:,:{at_shop}:,:{quantity}:,:{cost}:,:{tax}:,:{price}:,:{include_tax}:,:{price_change}:,:{more_info}:,:{images}:,:{description}:,:{service}:,:{default_quantity}:,:{active}:)"
            #print("item : " + str(item))
        else:
            product_id = int(self.list_box.item(self.list_box.selection())['values'][0])
            #print("product_id : " + str(product_id) + " barcode : " + str(brcod))
            doc_type = "Update_Items"
            item += f"(:{product_id}:,:{name}:,:{code}:,:{typ}:,:{barcode}:,:{at_shop}:,:{quantity}:,:{cost}:,:{tax}:,:{price}:,:{include_tax}:,:{price_change}:,:{more_info}:,:{images}:,:{description}:,:{service}:,:{default_quantity}:,:{active}:)"
            #print("item : " + str(item))
            # Update the product in the database
            Update_table_database('UPDATE product SET name=?, code=?, type=?, barcode=?, at_shop=?, quantity=?, cost=?, tax=?, price=?, include_tax=?, price_change=?, more_info=?, images=?, description=?, service=?, default_quantity=?, active=? WHERE id=?', (name, code, typ, barcode, at_shop, quantity, cost, tax, price, include_tax, price_change, more_info, images, description, service, default_quantity, active, product_id))
        

        try:
            # Insert the record into the upload_doc table
            Update_table_database('INSERT INTO upload_doc (doc_barcode, extension_barcode, user_id, customer_id, type, item, qty, price, discount, tax, payments, doc_created_date, doc_expire_date, doc_updated_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', ("23-200-" + str(brcod), "extension_barcode", self.master.master.master.master.user, self.master.master.master.master.custemr, doc_type, item, 1, 0, 0, 0, "payments_", "doc_created_date", "doc_expire_date", "doc_updated_date"))

            
            #print("Data inserted successfully into the upload_doc table.")
        except Exception as e:
            #print("Error occurred while inserting data into the upload_doc table:")
            #print(str(e))
            pass


        # Clear the product details widgets
        self.clear_product_details_widget()
        
        # Update the product listbox
        self.update_product_listbox()
