import sqlite3
import datetime
import os
import sys
import os
import sys
import os


def fetch_as_dict_list(cursor, query, values):
    cursor.execute(query, values)
    items = cursor.fetchall()
    #print("items len", len(items))
    columns = [col[0] for col in cursor.description]
    #print("columns")
    #print(str(columns))
    #print("items len", len(items))
    results = []
    for row in items:
        #print("row")
        #print(str(row))
        #print("items len", len(items))
        if len(columns) != len(row):
            raise ValueError("Mismatch between number of columns and rows "+ str(len(columns)) + ", "+ str(len(row)))
            
        results.append(dict(zip(columns, row)))
    return results
