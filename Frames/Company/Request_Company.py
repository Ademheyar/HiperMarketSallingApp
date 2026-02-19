import tkinter as tk
from tkinter import ttk
import sqlite3
import json
# Connect to the database or create it if it does not exist

import os
import os, sys
current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(os.path.join(current_dir, '..'), '..')
sys.path.append(MAIN_dir)

# from D.docediterform import DocEditForm
from D.printer import PrinterForm
from C.slipe import load_slip

from C.API.Get import *


class Request_Company_Frame(tk.Frame):
    def __init__(self, parent, Canceal_callback, User_data, Shop_data):
        tk.Frame.__init__(self, parent)
        pass
