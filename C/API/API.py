import tkinter as tk
from tkinter import ttk
import sqlite3
import shutil
import datetime
import os
import atexit
import sys
import random
import sqlite3, os
import base64
import json

import requests

current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(os.path.join(current_dir, '..'), '..')
sys.path.append(MAIN_dir)
data_dir = os.path.join(MAIN_dir, 'data')
db_path = os.path.join(data_dir, 'my_database.db')


import re
from urllib.parse import urlparse

_API_SESSION = requests.Session()
_API_SESSION.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/html, */*'
})

def _solve_aes_challenge(session, url, html):
    try:
        m_a = re.search(r'a=toNumbers\("([0-9a-fA-F]+)"\)', html)
        m_b = re.search(r'b=toNumbers\("([0-9a-fA-F]+)"\)', html)
        m_c = re.search(r'c=toNumbers\("([0-9a-fA-F]+)"\)', html)
        if m_a and m_b and m_c:
            from Crypto.Cipher import AES
            key = bytes.fromhex(m_a.group(1))
            iv = bytes.fromhex(m_b.group(1))
            ct = bytes.fromhex(m_c.group(1))
            cipher = AES.new(key, AES.MODE_CBC, iv)
            cookie_val = cipher.decrypt(ct).hex()
            parsed = urlparse(url)
            session.cookies.set('__test', cookie_val, domain=parsed.netloc, path='/')
            return True
    except Exception as e:
        print(f"AES challenge solve error: {e}")
    return False

# API Connection 

def normalize_url(url):
    if not url:
        return ""
    url = str(url).strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
    return url

def get_app_data_mode():
    try:
        conn = sqlite3.connect(db_path)
        from M.Preferences import load_api_preferences
        _url, mode = load_api_preferences(conn)
        conn.close()
        return mode
    except Exception:
        return "Cloud API"

def get_app_api_url():
    try:
        conn = sqlite3.connect(db_path)
        from M.Preferences import load_api_preferences
        url, _mode = load_api_preferences(conn)
        conn.close()
        return url
    except Exception:
        return "https://hipermarket0.xo.je/API/API.php"

def is_local_mode():
    return get_app_data_mode() == "Local Database"

def Chacke_Connection(Link):
    if not Link or is_local_mode():
        return False
    url = normalize_url(Link)
    entry = {'Do': "Testing Connection", 'shop': 0, 'user' : 0, 'ISNEW_USER' : 0 , 'ISNEW_SHOP' : 0 }
    response_data = Sand_API(url, entry)
    if response_data and isinstance(response_data, dict):
        status = response_data.get('status')
        if status == 'success' or response_data.get('ok') is True or response_data.get('message') == 'Connection OK':
            return True
        elif response_data.get('Erorr') in ['NO USER FOUND', 'NO SHOP FOUND', 'Try Agane', 'FILED REGISTERING SHOP']:
            return True
    return False

import time
_LINK_CACHE = {}

def islinked(link):
    if not link or is_local_mode():
        return False
    url = normalize_url(link)
    now = time.time()
    cached = _LINK_CACHE.get(url)
    if cached and (now - cached['time']) < 30:
        return cached['status']

    status = Chacke_Connection(link)
    _LINK_CACHE[url] = {'status': status, 'time': now}
    return status

def Sand_API(url, entry):
    if not url or is_local_mode():
        return None
    url = normalize_url(url)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    try:
        response = _API_SESSION.post(url, json=entry, headers=headers, timeout=10)
        if response is not None and response.status_code == 200:
            text = response.text.strip()
            # If server returned InfinityFree / Epizy free hosting anti-bot JS challenge
            if 'slowAES' in text or 'aes.js' in text or 'toNumbers' in text:
                if _solve_aes_challenge(_API_SESSION, url, text):
                    response = _API_SESSION.post(url, json=entry, headers=headers, timeout=10)
                    text = response.text.strip()

            if '{' in text and '}' in text:
                json_str = text[text.find('{'):text.rfind('}')+1]
                try:
                    return json.loads(json_str)
                except Exception:
                    pass
            try:
                return response.json()
            except Exception:
                pass
    except Exception as e:
        print(f"Sand_API error for {url}: {e}")
    return None
    
