import json
import os
from queue import Empty, Queue
import threading
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkmessagebox
from PIL import Image, ImageTk

from C.API.Get import fetch_as_dict_list
from M.Preferences import format_currency, resolve_shop_currency

MAIN_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))


class HomeFeedMixin:
    def initialize_home_feed(self, content_area):
        self.Home_frame = tk.Frame(content_area, bg=self.bg_dark)
        self.main_Notebook.add(self.Home_frame, text='Home')
        self.Home_frame.columnconfigure((0, 1), weight=1)
        self.Home_frame.columnconfigure(1, weight=0)
        self.Home_frame.rowconfigure(0, weight=0)
        self.Home_frame.rowconfigure(1, weight=2)
        self.Home_frame.rowconfigure(2, weight=0)

        self.home_feed_products = []
        self.home_feed_all_products = []
        self.home_comments = {}
        self.home_feed_canvas = None
        self.home_feed_scroll = None
        self.home_feed_offset = 0
        self.home_feed_batch_size = 10
        self.home_feed_has_more = True
        self.home_feed_loading = False
        self.home_search_var = tk.StringVar(value='')
        self.home_link_var = tk.StringVar(value=self.Link)
        self.home_grid_columns = 1
        self.guest_cart = []
        self.home_cart_button = None
        self.home_ui_ready = False
        self.home_search_job = None
        self.home_feed_request_id = 0
        self.home_feed_results = Queue()
        self.home_shop_currency_map = {}

    @staticmethod
    def normalize_home_product(product, currency=None):
        if not isinstance(product, dict):
            return {}

        name = str(product.get('name') or product.get('Name') or 'Untitled Product')
        code = str(product.get('code') or product.get('Code') or product.get('barcode') or product.get('id') or '0')
        shop = str(product.get('at_shop') or product.get('shop') or product.get('Shop_name') or product.get('Shop_name') or 'Main Store')
        price = product.get('price', 0)
        try:
            price = float(price)
        except (TypeError, ValueError):
            price = 0.0

        comments = product.get('comments') or []
        if isinstance(comments, str):
            try:
                comments = json.loads(comments)
            except Exception:
                comments = []
        if not isinstance(comments, list):
            comments = []

        currency = currency or product.get('home_currency') or product.get('Shop_currency') or product.get('currency')
        if not currency:
            try:
                currency = resolve_shop_currency(product.get('home_country') or product.get('Shop_country'))
            except ValueError:
                currency = None

        likes_seed = sum(ord(ch) for ch in name + code)
        likes = int((likes_seed % 210) + 18)
        comments_count = len(comments)
        if comments_count == 0:
            comments_count = int((likes_seed % 12) + 3)

        return {
            'id': int(product.get('id') or product.get('Id') or 0),
            'name': name,
            'shop': shop,
            'code': code,
            'description': str(product.get('description') or product.get('description_text') or product.get('detail') or 'New arrival in stock.'),
            'price': price,
            'currency': currency,
            'image': HomeFeedMixin.find_product_image_path(product),
            'likes': likes,
            'comments': comments,
            'comment_count': comments_count,
            'liked': False,
            'saved': False,
            '_source': dict(product),
        }

    @staticmethod
    def get_home_product_variants(product):
        source = product.get('_source') or product
        raw_info = source.get('more_info') or product.get('more_info') or ''
        try:
            info = json.loads(raw_info) if isinstance(raw_info, str) else raw_info
        except (TypeError, ValueError):
            info = []

        variants = []

        def add_records(node, path):
            if not isinstance(node, list):
                return
            if len(node) > 4 and not isinstance(node[0], (list, tuple, dict)):
                if len(path) < 4:
                    return
                try:
                    stock = float(node[4] or 0)
                    price = float(node[2] or product.get('price') or 0)
                except (TypeError, ValueError):
                    return
                if stock <= 0:
                    return
                try:
                    options = json.loads(node[1]) if isinstance(node[1], str) else node[1]
                except (TypeError, ValueError):
                    options = []
                type_label = ' / '.join(str(value) for value in options) if isinstance(options, list) else str(options or '')
                variants.append({
                    'shop': str(path[-4]),
                    'code': str(path[-3]),
                    'color': str(path[-2]),
                    'size': str(path[-1]),
                    'barcode': str(node[0] or source.get('barcode') or path[-3]),
                    'stock': stock,
                    'price': price,
                    'options': options if isinstance(options, list) else [],
                    'type_value': str(node[1] or '') if options else '',
                    'type_label': type_label,
                })
                return
            if len(node) == 2 and isinstance(node[0], str) and isinstance(node[1], list):
                add_records(node[1], path + [node[0]])
                return
            for child in node:
                add_records(child, path)

        add_records(info, [])
        if not variants and not info:
            try:
                stock = float(source.get('quantity') or product.get('quantity') or 0)
            except (TypeError, ValueError):
                stock = 0.0
            if stock > 0:
                variants.append({
                    'shop': str(product.get('shop') or 'Main Store'),
                    'code': str(product.get('code') or product.get('id') or ''),
                    'color': 'Default',
                    'size': 'Default',
                    'barcode': str(product.get('barcode') or product.get('code') or product.get('id') or ''),
                    'stock': stock,
                    'price': float(product.get('price') or 0),
                    'options': [],
                    'type_value': '',
                    'type_label': '',
                })
        return variants

    @staticmethod
    def find_product_image_path(product):
        candidates = []
        product_id = product.get('id') or product.get('Id')
        for key in ['code', 'Code', 'barcode', 'barcode_num', 'id', 'Id']:
            value = product.get(key)
            if value not in (None, '', 0):
                candidates.append(str(value))

        base_dirs = [
            os.path.join(MAIN_dir, 'data', 'Products'),
            os.path.join(MAIN_dir, 'data', 'Company'),
            os.path.join(MAIN_dir, 'data', 'Icon'),
        ]

        for base_dir in base_dirs:
            if not os.path.exists(base_dir):
                continue
            for candidate in candidates:
                for root, _, files in os.walk(base_dir):
                    if 'ProductImage.jpg' in files and candidate in root:
                        return os.path.join(root, 'ProductImage.jpg')
                    if 'ProductImage.png' in files and candidate in root:
                        return os.path.join(root, 'ProductImage.png')
                    if 'ProductImage.jpg' in files and str(product_id) in root:
                        return os.path.join(root, 'ProductImage.jpg')

        for base_dir in base_dirs:
            for root, _, files in os.walk(base_dir):
                if 'ProductImage.jpg' in files:
                    return os.path.join(root, 'ProductImage.jpg')
                if 'ProductImage.png' in files:
                    return os.path.join(root, 'ProductImage.png')

        return os.path.join(MAIN_dir, 'data', 'Icon', 'no_Product_Image.jpg')

    def _get_home_columns_for_width(self):
        width = max(320, self.Home_frame.winfo_width() if self.Home_frame.winfo_width() > 1 else self.winfo_screenwidth())
        if width < 540:
            return 1
        if width < 900:
            return 2
        if width < 1280:
            return 3
        return 4

    def _refresh_home_search(self):
        if self.home_search_job is not None:
            try:
                self.after_cancel(self.home_search_job)
            except tk.TclError:
                pass
        self.home_search_job = self.after(350, self._begin_home_feed_search)

    def _get_home_link_options(self):
        links = []
        try:
            with open(os.path.join(data_dir, 'loged.txt'), 'r', encoding='utf-8') as logged_file:
                for line in logged_file:
                    parts = line.strip().split('|')
                    if len(parts) == 3 and parts[2] and parts[2] not in links:
                        links.append(parts[2])
        except OSError:
            pass

        current_link = str(self.MainApplication.Link or '').strip()
        if current_link and current_link not in links:
            links.insert(0, current_link)
        return links

    def _apply_home_link(self, event=None):
        link = self.home_link_var.get().strip()
        self.MainApplication.Link = link
        self.home_link_var.set(link)
        self.home_shop_currency_map = {}
        self._begin_home_feed_search()

    def load_home_feed(self):
        if self.home_ui_ready:
            self._begin_home_feed_search()
            return

        self.home_feed_offset = 0
        self.home_feed_has_more = True
        self.home_feed_loading = False
        self.home_feed_products = []
        self.home_feed_all_products = []

        self.Home_frame.configure(bg='#f3f4f6')
        top_bar = tk.Frame(self.Home_frame, bg='#f3f4f6')
        top_bar.pack(fill='x', padx=12, pady=(10, 6))
        tk.Label(top_bar, text='Connection Link', bg='#f3f4f6', fg='#111827', font=('Arial', 11, 'bold')).pack(anchor='w', pady=(0, 6))
        link_row = tk.Frame(top_bar, bg='#f3f4f6')
        link_row.pack(fill='x', pady=(0, 10))
        self.home_link_selector = ttk.Combobox(
            link_row,
            textvariable=self.home_link_var,
            values=self._get_home_link_options(),
            font=('Arial', 10),
        )
        self.home_link_selector.pack(side='left', fill='x', expand=True, ipady=4)
        self.home_link_selector.bind('<<ComboboxSelected>>', self._apply_home_link)
        self.home_link_selector.bind('<Return>', self._apply_home_link)
        tk.Button(
            link_row, text='Apply', command=self._apply_home_link,
            bg='#1976d2', fg='white', activebackground='#1565c0',
            activeforeground='white', relief='flat', bd=0,
            padx=14, pady=7, cursor='hand2',
        ).pack(side='left', padx=(8, 0))
        tk.Label(top_bar, text='Search Products', bg='#f3f4f6', fg='#111827', font=('Arial', 11, 'bold')).pack(anchor='w', pady=(0, 6))
        search_row = tk.Frame(top_bar, bg='#f3f4f6')
        search_row.pack(fill='x')
        search_entry = tk.Entry(search_row, textvariable=self.home_search_var, font=('Arial', 11), bg='white', fg='#111827')
        search_entry.pack(side='left', fill='x', expand=True, ipady=6)
        search_entry.bind('<KeyRelease>', lambda event: self._refresh_home_search())
        if not self.user:
            self.home_cart_button = tk.Button(
                search_row, text=f'Cart ({len(self.guest_cart)})', command=self.open_guest_cart,
                bg='#0f766e', fg='white', activebackground='#115e59',
                activeforeground='white', relief='flat', bd=0,
                padx=14, cursor='hand2',
            )
            self.home_cart_button.pack(side='right', padx=(8, 0), fill='y')

        feed_wrapper = tk.Frame(self.Home_frame, bg='#f3f4f6')
        feed_wrapper.pack(fill='both', expand=True)
        self.home_feed_canvas = tk.Canvas(feed_wrapper, bg='#f3f4f6', highlightthickness=0)
        self.home_feed_canvas.pack(side='left', fill='both', expand=True)
        self.home_feed_scroll = tk.Scrollbar(feed_wrapper, orient='vertical', command=self.home_feed_canvas.yview)
        self.home_feed_scroll.pack(side='right', fill='y')
        self.home_feed_inner = tk.Frame(self.home_feed_canvas, bg='#f3f4f6')
        self.home_feed_window = self.home_feed_canvas.create_window(
            (0, 0), window=self.home_feed_inner, anchor='nw',
            width=max(320, self.Home_frame.winfo_width() - 20),
        )
        self.home_feed_canvas.configure(yscrollcommand=self._on_home_feed_scroll)
        self.home_grid_columns = self._get_home_columns_for_width()

        def resize_feed(event=None):
            self.home_feed_canvas.itemconfigure(self.home_feed_window, width=max(320, event.width))
            columns = self._get_home_columns_for_width()
            if columns != self.home_grid_columns:
                self.home_grid_columns = columns
                for child in self.home_feed_inner.winfo_children():
                    child.destroy()
                for column in range(columns):
                    self.home_feed_inner.columnconfigure(column, weight=1)
                for idx, product in enumerate(self.home_feed_products):
                    self._render_home_product_card(
                        self.home_feed_inner, product,
                        row=idx // columns, col=idx % columns,
                    )
            self.home_feed_canvas.configure(scrollregion=self.home_feed_canvas.bbox('all'))

        self.home_feed_canvas.bind('<Configure>', resize_feed)
        self.home_feed_inner.bind(
            '<Configure>',
            lambda event: self.home_feed_canvas.configure(scrollregion=self.home_feed_canvas.bbox('all')),
        )
        self.home_ui_ready = True
        self._begin_home_feed_search()

    def _begin_home_feed_search(self):
        self.home_search_job = None
        self.home_feed_request_id += 1
        self.home_feed_offset = 0
        self.home_feed_has_more = True
        self.home_feed_loading = False
        self.home_feed_products = []
        self.home_feed_all_products = []
        for widget in self.home_feed_inner.winfo_children():
            widget.destroy()
        self.home_feed_canvas.yview_moveto(0)
        self._load_next_home_batch()

    def _on_home_feed_scroll(self, first, last):
        self.home_feed_scroll.set(first, last)
        if float(last) >= 0.98 and self.home_feed_has_more and not self.home_feed_loading:
            self.after_idle(self._load_next_home_batch)

    def _load_next_home_batch(self):
        if self.home_feed_loading or not self.home_feed_has_more:
            return

        self.home_feed_loading = True
        query = (self.home_search_var.get() or '').strip()
        sql = 'SELECT * FROM product'
        values = []
        if query:
            pattern = f'%{query}%'
            sql += ' WHERE name LIKE ? OR code LIKE ? OR barcode LIKE ? OR at_shop LIKE ? OR description LIKE ?'
            values.extend([pattern] * 5)
        sql += ' ORDER BY id DESC LIMIT ? OFFSET ?'
        values.extend([self.home_feed_batch_size, self.home_feed_offset])
        request_id = self.home_feed_request_id
        offset = self.home_feed_offset
        link = getattr(self, 'Link', None)

        def fetch_batch():
            try:
                results = fetch_as_dict_list(link, sql, tuple(values)) or []
            except Exception:
                results = []
            shop_rows = []
            if offset == 0:
                try:
                    shop_rows = fetch_as_dict_list(
                        link,
                        'SELECT Shop_Id, Shop_name, Shop_brand_name, Shop_country, Shop_currency FROM Shops',
                        (),
                    ) or []
                except Exception:
                    shop_rows = []
                if not shop_rows:
                    try:
                        shop_rows = fetch_as_dict_list(
                            link,
                            'SELECT Shop_Id, Shop_name, Shop_brand_name, Shop_country FROM Shops',
                            (),
                        ) or []
                    except Exception:
                        shop_rows = []
            self.home_feed_results.put((request_id, offset, query, results, shop_rows))

        threading.Thread(target=fetch_batch, daemon=True).start()
        self.after(25, self._poll_home_feed_results)

    def _poll_home_feed_results(self):
        try:
            result = self.home_feed_results.get_nowait()
        except Empty:
            if self.home_feed_loading:
                self.after(25, self._poll_home_feed_results)
            return
        self._finish_home_feed_batch(*result)

    def _finish_home_feed_batch(self, request_id, offset, query, results, shop_rows):
        if request_id != self.home_feed_request_id:
            return

        for shop in shop_rows:
            try:
                currency = resolve_shop_currency(shop.get('Shop_country'), shop.get('Shop_currency'))
            except ValueError:
                currency = None
            if currency:
                for key in ('Shop_Id', 'Shop_name', 'Shop_brand_name'):
                    if shop.get(key) not in (None, ''):
                        self.home_shop_currency_map[str(shop[key]).casefold()] = currency

        self.home_feed_loading = False
        self.home_feed_offset += len(results)
        self.home_feed_has_more = len(results) == self.home_feed_batch_size
        if not results and not self.home_feed_products and not query:
            shop_name = self.Shops[0]['Shop_brand_name'] if self.Shops else 'Main Store'
            results = [{
                'id': 1,
                'name': 'Classic Essentials',
                'code': 'CE-01',
                'barcode': '1001',
                'at_shop': shop_name,
                'price': 129.99,
                'description': 'A ready-to-wear favorite with a premium finish.',
                'comments': [],
            }]
            self.home_feed_has_more = False

        first_new_index = len(self.home_feed_products)
        for product in results:
            shop_key = str(product.get('at_shop') or '').casefold()
            currency = self.home_shop_currency_map.get(shop_key)
            normalized = self.normalize_home_product(product, currency)
            if normalized:
                self.home_feed_products.append(normalized)
                self.home_feed_all_products.append(normalized)
                self.home_comments[str(normalized['id'])] = list(normalized.get('comments') or [])

        for idx in range(first_new_index, len(self.home_feed_products)):
            product = self.home_feed_products[idx]
            self._render_home_product_card(
                self.home_feed_inner, product,
                row=idx // self.home_grid_columns,
                col=idx % self.home_grid_columns,
            )

        self.home_feed_inner.update_idletasks()
        self.home_feed_canvas.configure(scrollregion=self.home_feed_canvas.bbox('all'))

    def _render_home_product_card(self, parent, product, row=0, col=0):
        card = tk.Frame(parent, bg='white', bd=1, relief='solid', highlightbackground='#e5e7eb', padx=12, pady=10)
        card.grid(row=row, column=col, sticky='nsew', padx=10, pady=10)
        parent.grid_columnconfigure(col, weight=1)

        header = tk.Frame(card, bg='white')
        header.pack(fill='x')

        avatar = tk.Label(header, text='◉', font=('Arial', 18, 'bold'), fg='#0f172a', bg='white')
        avatar.pack(side='left')

        shop_label = tk.Label(header, text=product['shop'], font=('Arial', 12, 'bold'), fg='#111827', bg='white')
        shop_label.pack(side='left', padx=(8, 0))

        follow_btn = tk.Button(header, text='Follow', font=('Arial', 9, 'bold'), bg='#f3f4f6', fg='#111827', bd=0, relief='flat', padx=8)
        follow_btn.pack(side='right')

        image_path = product['image']
        if os.path.exists(image_path):
            try:
                img = Image.open(image_path).convert('RGBA')
                img = img.resize((520, 520), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                image_label = tk.Label(card, image=photo, bg='white')
                image_label.image = photo
                image_label.pack(fill='x', pady=(12, 8))
            except Exception:
                image_label = tk.Label(card, text='Product Image', bg='#e5e7eb', height=18, font=('Arial', 12, 'bold'))
                image_label.pack(fill='x', pady=(12, 8))
        else:
            image_label = tk.Label(card, text='Product Image', bg='#e5e7eb', height=18, font=('Arial', 12, 'bold'))
            image_label.pack(fill='x', pady=(12, 8))

        meta = tk.Frame(card, bg='white')
        meta.pack(fill='x', pady=(0, 8))

        title = tk.Label(meta, text=product['name'], font=('Arial', 14, 'bold'), fg='#111827', bg='white')
        title.pack(anchor='w')

        desc = tk.Label(meta, text=product['description'], font=('Arial', 10), fg='#374151', bg='white', justify='left', wraplength=500)
        desc.pack(anchor='w', pady=(4, 0))

        price_label = tk.Label(meta, text=f'Price: {format_currency(product["price"], product.get("currency"))}', font=('Arial', 12, 'bold'), fg='#0f766e', bg='white')
        price_label.pack(anchor='w', pady=(6, 0))

        for clickable in (shop_label, image_label, title, desc, price_label):
            clickable.configure(cursor='hand2')
            clickable.bind('<Button-1>', lambda _event, selected=product: self.show_home_product_options(selected))

        action_row = tk.Frame(card, bg='white')
        action_row.pack(fill='x', pady=(8, 10))

        like_btn = tk.Button(action_row, text=f'❤ {product["likes"]}', bg='#f3f4f6', fg='#111827', font=('Arial', 10, 'bold'), relief='flat', bd=0, padx=10, command=lambda p=product: self.toggle_home_like(p))
        like_btn.pack(side='left', padx=(0, 8))

        comment_btn = tk.Button(action_row, text=f'💬 {product["comment_count"]}', bg='#f3f4f6', fg='#111827', font=('Arial', 10, 'bold'), relief='flat', bd=0, padx=10, command=lambda p=product: self.toggle_home_comments(p))
        comment_btn.pack(side='left', padx=(0, 8))

        share_btn = tk.Button(action_row, text='↗ Share', bg='#f3f4f6', fg='#111827', font=('Arial', 10, 'bold'), relief='flat', bd=0, padx=10, command=lambda p=product: self.share_home_product(p))
        share_btn.pack(side='left', padx=(0, 8))

        save_btn = tk.Button(action_row, text='Save', bg='#f3f4f6', fg='#111827', font=('Arial', 10, 'bold'), relief='flat', bd=0, padx=10, command=lambda p=product: self.toggle_home_saved(p))
        save_btn.pack(side='left', padx=(0, 8))

        cart_btn = tk.Button(action_row, text='Add to chart', bg='#2563eb', fg='white', font=('Arial', 10, 'bold'), relief='flat', bd=0, padx=12, command=lambda p=product: self.add_home_product_to_cart(p))
        cart_btn.pack(side='right')

        comment_frame = tk.Frame(card, bg='#f9fafb', bd=1, relief='solid', highlightbackground='#e5e7eb')
        comment_frame.pack(fill='x', pady=(4, 0))
        comment_frame.pack_forget()

        comment_label = tk.Label(comment_frame, text='Comments', bg='#f9fafb', fg='#111827', font=('Arial', 10, 'bold'), anchor='w')
        comment_label.pack(anchor='w', padx=8, pady=(8, 4))

        comments_box = tk.Frame(comment_frame, bg='#f9fafb')
        comments_box.pack(fill='x', padx=8, pady=(0, 8))

        comments = self.home_comments.get(str(product['id']), [])
        for index, comment in enumerate(comments[:4]):
            comment_row = tk.Frame(comments_box, bg='#ffffff', pady=6, padx=8, bd=1, relief='solid', highlightbackground='#e5e7eb')
            comment_row.pack(fill='x', pady=3)
            user_name = tk.Label(comment_row, text=comment.get('user', 'Guest') + ':', bg='white', fg='#111827', font=('Arial', 9, 'bold'), justify='left')
            user_name.pack(anchor='w')
            msg = tk.Label(comment_row, text=comment.get('text', ''), bg='white', fg='#374151', font=('Arial', 9), justify='left', wraplength=480)
            msg.pack(anchor='w', pady=(2, 0))

            reply_entry = tk.Entry(comment_row, font=('Arial', 9), width=32)
            reply_entry.pack(fill='x', pady=(6, 0))
            reply_btn = tk.Button(comment_row, text='Reply', bg='#e5e7eb', fg='#111827', relief='flat', bd=0, padx=8, command=lambda p=product, i=index, entry=reply_entry: self.add_home_reply(p, i, entry.get()))
            reply_btn.pack(anchor='e', pady=(4, 0))

            if comment.get('replies'):
                for reply in comment['replies']:
                    reply_row = tk.Frame(comment_row, bg='#f3f4f6', pady=4, padx=6)
                    reply_row.pack(fill='x', pady=(4, 0))
                    tk.Label(reply_row, text=f"{reply.get('user', 'Guest')}: {reply.get('text', '')}", bg='#f3f4f6', fg='#4b5563', font=('Arial', 8), justify='left', wraplength=440).pack(anchor='w')

        comment_input = tk.Entry(comment_frame, width=60, font=('Arial', 10))
        comment_input.pack(fill='x', padx=8, pady=(0, 8))

        post_button = tk.Button(comment_frame, text='Post Comment', bg='#2563eb', fg='white', relief='flat', bd=0, padx=12, command=lambda p=product, entry=comment_input: self.add_home_comment(p, entry.get()))
        post_button.pack(anchor='e', padx=8, pady=(0, 10))

        comment_btn.configure(command=lambda p=product, panel=comment_frame: self.toggle_home_comments(p, panel))
        product['_comment_panel'] = comment_frame
        product['_comment_input'] = comment_input

    def toggle_home_like(self, product):
        product['liked'] = not product.get('liked', False)
        if product['liked']:
            product['likes'] += 1
        else:
            product['likes'] = max(0, product['likes'] - 1)
        self.load_home_feed()

    def toggle_home_saved(self, product):
        product['saved'] = not product.get('saved', False)
        status = 'saved' if product['saved'] else 'removed from saved'
        tkmessagebox.showinfo('Saved', f"{product['name']} {status}.")

    def share_home_product(self, product):
        tkmessagebox.showinfo('Share', f"Share link for {product['name']} has been generated.")

    def toggle_home_comments(self, product, panel=None):
        panel = panel or product.get('_comment_panel')
        if panel is None:
            return
        if panel.winfo_ismapped():
            panel.pack_forget()
        else:
            panel.pack(fill='x', pady=(4, 0))

    def add_home_comment(self, product, text):
        if not text or not text.strip():
            return
        comment_key = str(product['id'])
        if comment_key not in self.home_comments:
            self.home_comments[comment_key] = []
        self.home_comments[comment_key].append({'user': self.user['User_name'] if hasattr(self, 'user') and self.user else 'Guest', 'text': text.strip(), 'replies': []})
        product['comments'] = list(self.home_comments[comment_key])
        product['comment_count'] = len(self.home_comments[comment_key])
        self.load_home_feed()

    def add_home_reply(self, product, comment_index, text):
        if not text or not text.strip():
            return
        comment_key = str(product['id'])
        if comment_key not in self.home_comments:
            self.home_comments[comment_key] = []
        if 0 <= comment_index < len(self.home_comments[comment_key]):
            self.home_comments[comment_key][comment_index].setdefault('replies', []).append({
                'user': self.user['User_name'] if hasattr(self, 'user') and self.user else 'Guest',
                'text': text.strip(),
            })
            product['comments'] = list(self.home_comments[comment_key])
            product['comment_count'] = len(self.home_comments[comment_key])
            self.load_home_feed()

    def add_home_product_to_cart(self, product):
        self.show_home_product_options(product)

    def show_home_product_options(self, product):
        existing_drawer = getattr(self, 'home_quick_drawer', None)
        if existing_drawer is not None and existing_drawer.winfo_exists():
            existing_drawer.destroy()

        variants = self.get_home_product_variants(product)
        self.home_quick_product = product
        self.home_quick_variants = variants

        frame_width = self.Home_frame.winfo_width()
        if frame_width <= 1:
            frame_width = self.winfo_screenwidth()
        frame_height = max(self.Home_frame.winfo_height(), 360)
        drawer_width = min(380, frame_width)
        drawer = tk.Frame(self.Home_frame, bg='white', bd=1, relief='solid', padx=20, pady=18)
        drawer.place(x=0, y=0, width=drawer_width, height=frame_height)
        self.home_quick_drawer = drawer

        header = tk.Frame(drawer, bg='white')
        header.pack(fill='x')
        tk.Label(header, text='Choose options', bg='white', fg='#111827', font=('Arial', 16, 'bold')).pack(side='left')
        tk.Button(
            header, text='X', command=self.close_home_product_options,
            bg='white', fg='#374151', relief='flat', bd=0, cursor='hand2',
        ).pack(side='right')

        tk.Label(drawer, text=product['name'], bg='white', fg='#111827', font=('Arial', 13, 'bold'), wraplength=320, justify='left').pack(anchor='w', pady=(22, 4))
        price_label = tk.Label(drawer, text=f"{product['shop']}  |  {format_currency(product['price'], product.get('currency'))}", bg='white', fg='#4b5563', font=('Arial', 10))
        price_label.pack(anchor='w', pady=(0, 18))
        self.home_quick_price_label = price_label

        tk.Label(drawer, text='Color', bg='white', fg='#374151', font=('Arial', 10, 'bold')).pack(anchor='w')
        color_values = list(dict.fromkeys(variant['color'] for variant in variants))
        color_box = ttk.Combobox(drawer, state='readonly', values=color_values)
        color_box.pack(fill='x', pady=(4, 14), ipady=3)
        self.home_quick_color = color_box

        tk.Label(drawer, text='Size', bg='white', fg='#374151', font=('Arial', 10, 'bold')).pack(anchor='w')
        size_box = ttk.Combobox(drawer, state='readonly')
        size_box.pack(fill='x', pady=(4, 14), ipady=3)
        self.home_quick_size = size_box

        option_label = tk.Label(drawer, text='Type', bg='white', fg='#374151', font=('Arial', 10, 'bold'))
        option_label.pack(anchor='w')
        option_box = ttk.Combobox(drawer, state='readonly')
        option_box.pack(fill='x', pady=(4, 14), ipady=3)
        self.home_quick_option = option_box

        tk.Label(drawer, text='Quantity', bg='white', fg='#374151', font=('Arial', 10, 'bold')).pack(anchor='w')
        quantity_box = ttk.Spinbox(drawer, from_=1, to=1, increment=1, width=8)
        quantity_box.set('1')
        quantity_box.pack(anchor='w', pady=(4, 10), ipady=3)
        self.home_quick_quantity = quantity_box

        stock_label = tk.Label(drawer, text='No stock available', bg='white', fg='#b91c1c', font=('Arial', 10))
        stock_label.pack(anchor='w', pady=(0, 16))
        self.home_quick_stock_label = stock_label

        status_label = tk.Label(drawer, text='', bg='white', fg='#b91c1c', font=('Arial', 9), wraplength=320, justify='left')
        status_label.pack(anchor='w', pady=(0, 8))
        self.home_quick_status_label = status_label

        add_button = tk.Button(
            drawer, text='Add to chart', command=self.confirm_home_product_to_cart,
            bg='#2563eb', fg='white', activebackground='#1d4ed8', activeforeground='white',
            font=('Arial', 11, 'bold'), relief='flat', bd=0, padx=14, pady=10, cursor='hand2',
        )
        add_button.pack(fill='x', side='bottom')
        self.home_quick_add_button = add_button

        def refresh_variant(*_args):
            matching_sizes = list(dict.fromkeys(
                variant['size'] for variant in variants
                if variant['color'] == color_box.get()
            ))
            size_box.configure(values=matching_sizes)
            if size_box.get() not in matching_sizes:
                size_box.set(matching_sizes[0] if matching_sizes else '')
            matching_variants = [
                variant for variant in variants
                if variant['color'] == color_box.get() and variant['size'] == size_box.get()
            ]
            option_values = list(dict.fromkeys(
                variant['type_label'] for variant in matching_variants if variant['type_label']
            ))
            if option_values:
                option_box.configure(values=option_values)
                if option_box.get() not in option_values:
                    option_box.set(option_values[0])
            else:
                option_label.pack_forget()
                option_box.pack_forget()
                option_box.set('')
            selected = next((
                variant for variant in matching_variants
                if variant['type_label'] == option_box.get()
            ), None)
            if selected:
                stock = selected['stock']
                quantity_box.configure(from_=1, to=max(1, int(stock)))
                quantity_box.set('1')
                stock_label.configure(text=f"{stock:g} available  |  Code {selected['code']}", fg='#047857')
                price_label.configure(text=f"{selected['shop']}  |  {format_currency(selected['price'], product.get('currency'))}")
                add_button.configure(state=tk.NORMAL)
            else:
                quantity_box.configure(from_=1, to=1)
                quantity_box.set('1')
                stock_label.configure(text='No stock available', fg='#b91c1c')
                add_button.configure(state=tk.DISABLED)
            status_label.configure(text='')

        color_box.bind('<<ComboboxSelected>>', refresh_variant)
        size_box.bind('<<ComboboxSelected>>', refresh_variant)
        option_box.bind('<<ComboboxSelected>>', refresh_variant)
        if color_values:
            color_box.current(0)
            refresh_variant()
        else:
            color_box.configure(state='disabled')
            size_box.configure(state='disabled')
            quantity_box.configure(state='disabled')
            add_button.configure(state=tk.DISABLED)

        self.home_quick_add_button.focus_set()

    def close_home_product_options(self):
        drawer = getattr(self, 'home_quick_drawer', None)
        if drawer is None or not drawer.winfo_exists():
            return
        drawer.destroy()

    @staticmethod
    def make_guest_cart_item(product, variant, quantity):
        source = product.get('_source') or product
        return {
            'product_id': product['id'],
            'name': product['name'],
            'code': variant['code'],
            'barcode': variant['barcode'],
            'shop': variant['shop'],
            'color': variant['color'],
            'size': variant['size'],
            'type_value': variant.get('type_value', ''),
            'quantity': quantity,
            'stock': variant['stock'],
            'price': variant['price'] or product['price'],
            'currency': product.get('currency'),
            'source': dict(source),
        }

    @staticmethod
    def add_guest_cart_item(cart, item):
        variant_key = ('product_id', 'code', 'barcode', 'shop', 'color', 'size', 'type_value')
        for existing in cart:
            if all(existing.get(key) == item.get(key) for key in variant_key):
                existing['quantity'] = min(
                    float(existing['stock']),
                    float(existing['quantity']) + float(item['quantity']),
                )
                return cart
        cart.append(item)
        return cart

    @staticmethod
    def guest_cart_total(cart):
        return sum(float(item['price']) * float(item['quantity']) for item in cart)

    @staticmethod
    def guest_cart_totals(cart):
        totals = {}
        for item in cart:
            currency = item.get('currency') or ''
            totals[currency] = totals.get(currency, 0.0) + float(item['price']) * float(item['quantity'])
        return totals

    def update_guest_cart_button(self):
        if self.home_cart_button is None:
            return
        try:
            self.home_cart_button.configure(text=f'Cart ({len(self.guest_cart)})')
        except tk.TclError:
            self.home_cart_button = None

    def open_guest_cart(self):
        drawer = getattr(self, 'home_quick_drawer', None)
        if drawer is not None and drawer.winfo_exists():
            drawer.destroy()

        frame_width = self.Home_frame.winfo_width()
        if frame_width <= 1:
            frame_width = self.winfo_screenwidth()
        frame_height = max(self.Home_frame.winfo_height(), 360)
        drawer_width = min(420, frame_width)
        target_x = frame_width - drawer_width
        drawer = tk.Frame(self.Home_frame, bg='white', bd=1, relief='solid', padx=18, pady=16)
        drawer.place(x=target_x, y=0, width=drawer_width, height=frame_height)
        self.home_quick_drawer = drawer

        header = tk.Frame(drawer, bg='white')
        header.pack(fill='x')
        tk.Label(header, text='Your cart', bg='white', fg='#111827', font=('Arial', 16, 'bold')).pack(side='left')
        tk.Button(
            header, text='X', command=self.close_home_product_options,
            bg='white', fg='#374151', relief='flat', bd=0, cursor='hand2',
        ).pack(side='right')

        self.home_cart_items_frame = tk.Frame(drawer, bg='white')
        self.home_cart_items_frame.pack(fill='both', expand=True, pady=(16, 8))
        self.home_cart_total_label = tk.Label(drawer, bg='white', fg='#111827', font=('Arial', 13, 'bold'))
        self.home_cart_total_label.pack(anchor='e', pady=(8, 12))
        self.home_cart_checkout_button = tk.Button(
            drawer, text='Checkout', command=self.begin_guest_checkout,
            bg='#0f766e', fg='white', activebackground='#115e59',
            activeforeground='white', font=('Arial', 11, 'bold'),
            relief='flat', bd=0, padx=14, pady=10, cursor='hand2',
        )
        self.home_cart_checkout_button.pack(fill='x', side='bottom')
        self.render_guest_cart()

    def render_guest_cart(self):
        frame = getattr(self, 'home_cart_items_frame', None)
        if frame is None or not frame.winfo_exists():
            return
        for child in frame.winfo_children():
            child.destroy()
        if not self.guest_cart:
            tk.Label(frame, text='Your cart is empty.', bg='white', fg='#6b7280', font=('Arial', 11)).pack(anchor='w')
        for index, item in enumerate(self.guest_cart):
            row = tk.Frame(frame, bg='#f8fafc', padx=10, pady=9)
            row.pack(fill='x', pady=4)
            tk.Label(row, text=item['name'], bg='#f8fafc', fg='#111827', font=('Arial', 10, 'bold'), wraplength=280, justify='left').pack(anchor='w')
            detail = f"{item['color']} / {item['size']}"
            if item.get('type_value'):
                detail += f" / {item['type_value']}"
            tk.Label(row, text=f"{detail}  |  {format_currency(item['price'], item.get('currency'))} each", bg='#f8fafc', fg='#4b5563', font=('Arial', 9)).pack(anchor='w', pady=(3, 6))
            controls = tk.Frame(row, bg='#f8fafc')
            controls.pack(fill='x')
            quantity = ttk.Spinbox(controls, from_=1, to=max(1, int(item['stock'])), width=5)
            quantity.set(str(item['quantity']))
            quantity.pack(side='left')
            tk.Button(
                controls, text='Update', command=lambda i=index, q=quantity: self.update_guest_cart_item(i, q.get()),
                bg='#e2e8f0', fg='#111827', relief='flat', bd=0, padx=8,
            ).pack(side='left', padx=(6, 0))
            tk.Button(
                controls, text='Remove', command=lambda i=index: self.remove_guest_cart_item(i),
                bg='#fee2e2', fg='#991b1b', relief='flat', bd=0, padx=8,
            ).pack(side='right')
        totals = self.guest_cart_totals(self.guest_cart)
        total_text = '  |  '.join(format_currency(amount, currency) for currency, amount in totals.items())
        self.home_cart_total_label.configure(text=f'Total: {total_text or format_currency(0, "")}')
        self.home_cart_checkout_button.configure(state=tk.NORMAL if self.guest_cart else tk.DISABLED)

    def update_guest_cart_item(self, index, quantity_text):
        try:
            quantity = int(quantity_text)
        except (TypeError, ValueError):
            return
        if not 0 < quantity <= self.guest_cart[index]['stock']:
            return
        self.guest_cart[index]['quantity'] = quantity
        self.render_guest_cart()
        self.update_guest_cart_button()

    def remove_guest_cart_item(self, index):
        if 0 <= index < len(self.guest_cart):
            self.guest_cart.pop(index)
        self.render_guest_cart()
        self.update_guest_cart_button()

    def begin_guest_checkout(self):
        tkmessagebox.showinfo(
            'Payment setup required',
            'The cart is ready, but this app has no configured card or account payment gateway. '
            'Choose a supported payment provider before guest checkout can charge an account.',
        )

    def confirm_home_product_to_cart(self):
        selected = next((
            variant for variant in self.home_quick_variants
            if variant['color'] == self.home_quick_color.get()
            and variant['size'] == self.home_quick_size.get()
            and variant['type_label'] == self.home_quick_option.get()
        ), None)
        if selected is None:
            self.home_quick_status_label.configure(text='Choose an in-stock color and size.')
            return
        try:
            quantity = float(self.home_quick_quantity.get())
        except (TypeError, ValueError):
            self.home_quick_status_label.configure(text='Enter a valid quantity.')
            return
        if quantity <= 0 or quantity > selected['stock']:
            self.home_quick_status_label.configure(text=f"Quantity must be between 1 and {selected['stock']:g}.")
            return

        product = self.home_quick_product
        source = dict(product.get('_source') or product)
        source.setdefault('id', product['id'])
        source.setdefault('name', product['name'])
        source.setdefault('code', product.get('code', ''))
        source.setdefault('barcode', product.get('barcode', ''))
        source.setdefault('price', product['price'])
        source.setdefault('include_tax', 0)
        source.setdefault('more_info', '')
        unit_price = selected['price'] or float(source['price'])
        type_selection = [[selected['type_value'], quantity, unit_price]] if selected['type_value'] else []
        item_info = {
            'values': source,
            'type': 'ITEM',
            'extra_data': [[selected['shop'], selected['code'], selected['color'], selected['size'], quantity, selected['stock'], selected['barcode'], type_selection]],
            'item_list': json.loads(source['more_info']) if isinstance(source['more_info'], str) and source['more_info'] else [],
        }
        selected_item = [
            item_info, str(source['id']), selected['code'], selected['barcode'], source['name'],
            selected['color'], selected['size'], quantity, selected['stock'], '',
            unit_price, source.get('include_tax', 0), quantity * unit_price, selected['shop'], '', selected['type_value'],
        ]
        if not self.user:
            cart_item = self.make_guest_cart_item(product, selected, quantity)
            self.guest_cart = self.add_guest_cart_item(self.guest_cart, cart_item)
            self.update_guest_cart_button()
            self.home_quick_status_label.configure(text='Added to cart.', fg='#047857')
            self.home_quick_add_button.configure(state=tk.DISABLED)
            self.after(100, self.close_home_product_options)
            self.after(120, self.open_guest_cart)
            return
        self.Selected_items.append([[selected_item], 'ITEM', source['name'], selected['barcode']])
        self.home_quick_status_label.configure(text='Added to chart.', fg='#047857')
        self.home_quick_add_button.configure(state=tk.DISABLED)
        self.after(100, self.close_home_product_options)
        self.after(140, self.Update_Selected_item)

    # display buttons profermans
