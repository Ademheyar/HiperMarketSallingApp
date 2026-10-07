"""Pure helpers that turn raw user / shop rows into the values the profile UI shows.

This module performs no database access and no widget work, so it can be unit
tested on its own and reused by any panel that needs a summary of a staff
member's account.
"""
import json

from M.Preferences import format_currency, resolve_shop_currency


SEPARATORS = (',', '|', '+', ';')


def count_items(value):
    """Best-effort count of the entries stored in a loosely typed column."""
    if value is None:
        return 0
    if isinstance(value, (list, tuple, set, dict)):
        return len(value)
    text = str(value).strip()
    if text in ('', 'None', 'null', 'N/A', '[]', '{}'):
        return 0
    try:
        parsed = json.loads(text)
    except (ValueError, TypeError):
        parsed = None
    if parsed is not None:
        if isinstance(parsed, (list, tuple, set, dict)):
            return len(parsed)
        return 0
    for separator in SEPARATORS:
        if separator in text:
            parts = [part for part in text.split(separator) if part.strip()]
            if parts:
                return len(parts)
    return 1


def _work_shop_entries(user):
    raw = user.get('User_work_shop')
    if not raw:
        return []
    if isinstance(raw, (list, tuple)):
        return list(raw)
    try:
        parsed = json.loads(raw)
    except (ValueError, TypeError):
        return []
    return list(parsed) if isinstance(parsed, (list, tuple)) else []


ROLE_BY_LEVEL = (
    ('Owner', 10),
    ('Manager', 9),
    ('Supervisor', 5),
    ('Seller', 1),
)


def _role_from_level(level):
    try:
        numeric = float(level)
    except (TypeError, ValueError):
        return None
    for title, threshold in ROLE_BY_LEVEL:
        if numeric >= threshold:
            return title
    return 'Cashier'


def resolve_role(user, shop):
    """Return the staff member's role for ``shop`` (falls back to their type)."""
    shop_name = str((shop or {}).get('Shop_name') or '')
    brand_name = str((shop or {}).get('Shop_brand_name') or '')
    for entry in _work_shop_entries(user):
        if not isinstance(entry, (list, tuple)) or len(entry) < 4:
            continue
        entry_name = str(entry[1]) if len(entry) > 1 else ''
        entry_brand = str(entry[2]) if len(entry) > 2 else ''
        matches_name = not shop_name or entry_name == shop_name
        matches_brand = not brand_name or entry_brand == brand_name
        if not (matches_name and matches_brand):
            continue
        levels = entry[3]
        level = levels[0] if isinstance(levels, (list, tuple)) and levels else levels
        role = _role_from_level(level)
        if role:
            return role
    declared = str(user.get('User_type') or '').strip()
    return declared or 'Staff'


def _display(value, fallback='N/A'):
    text = str(value or '').strip()
    return text if text else fallback


def build_summary(user, shops, on_shop=0):
    """Collect every value the profile header renders into a single dict."""
    user = user or {}
    shops = shops or []
    shop = None
    if shops:
        index = on_shop if isinstance(on_shop, int) and 0 <= on_shop < len(shops) else 0
        shop = shops[index]

    first_name = str(user.get('User_fname') or '').strip()
    last_name = str(user.get('User_Lname') or '').strip()
    full_name = ' '.join(part for part in (first_name, last_name) if part)
    user_name = str(user.get('User_name') or '').strip()

    return {
        'user_id': user.get('User_id'),
        'user_name': user_name,
        'handle': '@' + (user_name or 'user'),
        'full_name': full_name or user_name or 'Unnamed user',
        'role': resolve_role(user, shop),
        'shop_name': _display((shop or {}).get('Shop_brand_name') or (shop or {}).get('Shop_name'), ''),
        'location': _display(user.get('User_address') or user.get('User_country')),
        'email': _display(user.get('User_email')),
        'about': str(user.get('User_about') or '').strip(),
        'following': count_items(user.get('User_following_shop')),
        'likes': count_items(user.get('User_likes')),
        'saved': count_items(user.get('User_favoraite_items')),
    }


def build_messages(summary, shops):
    """Short conversations shown under the ``Messages`` tab."""
    messages = []
    shop_label = summary.get('shop_name') or 'your shop'
    if summary.get('shop_name'):
        messages.append({
            'sender': 'System Admin',
            'preview': f"Your daily POS shift report for {shop_label} has been verified.",
        })
    for shop in shops or []:
        name = str(shop.get('Shop_brand_name') or shop.get('Shop_name') or '').strip()
        if not name:
            continue
        messages.append({
            'sender': 'Warehouse Manager',
            'preview': f"Stock received for {name} is ready to be counted.",
        })
    if not messages:
        messages.append({
            'sender': 'System Admin',
            'preview': 'Welcome to Hiper Market. Complete your profile to get started.',
        })
    return messages


def build_notifications(summary, shops):
    """Alerts shown under the ``Notif`` tab."""
    notifications = []
    for shop in shops or []:
        name = str(shop.get('Shop_name') or shop.get('Shop_brand_name') or '').strip()
        online_id = shop.get('Shop_online_id')
        if name and not online_id:
            notifications.append({
                'title': 'Not uploaded',
                'text': f"{name} data has not been uploaded yet.",
            })
    if summary.get('role'):
        notifications.append({
            'title': 'Role assigned',
            'text': f"You are signed in as {summary['role']}.",
        })
    if not notifications:
        notifications.append({
            'title': 'All clear',
            'text': 'No new notifications right now.',
        })
    return notifications


def format_history_rows(rows, shops, on_shop=0):
    """Turn ``doc_table`` rows into displayable history entries."""
    currency = None
    shops = shops or []
    if shops:
        index = on_shop if isinstance(on_shop, int) and 0 <= on_shop < len(shops) else 0
        shop = shops[index]
        try:
            currency = resolve_shop_currency(shop.get('Shop_country'), shop.get('Shop_currency'))
        except (ValueError, AttributeError):
            currency = None

    history = []
    for row in rows or []:
        total = row.get('total')
        if total is None:
            total = row.get('price')
        try:
            total_value = float(total or 0)
        except (TypeError, ValueError):
            total_value = 0.0
        history.append({
            'barcode': _display(row.get('doc_barcode'), 'N/A'),
            'date': _display(row.get('doc_created_date'), 'Unknown date'),
            'amount': format_currency(total_value, currency),
        })
    return history
