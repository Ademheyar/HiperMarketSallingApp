"""Small vector icon renderer for the logged-user profile panel.

tkinter cannot render SVG without extra dependencies, so every icon used by
:mod:`M.UserProfile` is drawn with canvas primitives. Each icon is defined
inside a normalised ``[-0.5, 0.5]`` box and scaled to the requested size, so a
single definition works at any resolution.
"""
import tkinter as tk


# Each drawing function receives (canvas, scale, line_width, cx, cy, color) and
# paints a single icon centred on (cx, cy).
def _draw_chat(canvas, s, w, cx, cy, color):
    canvas.create_rectangle(cx - 0.5 * s, cy - 0.38 * s, cx + 0.5 * s, cy + 0.22 * s,
                            outline=color, width=w)
    canvas.create_polygon(cx + 0.16 * s, cy + 0.22 * s,
                          cx + 0.16 * s, cy + 0.46 * s,
                          cx - 0.06 * s, cy + 0.22 * s,
                          outline=color, fill=color, width=w)


def _draw_bell(canvas, s, w, cx, cy, color):
    canvas.create_arc(cx - 0.38 * s, cy - 0.44 * s, cx + 0.38 * s, cy + 0.30 * s,
                      start=0, extent=180, style='arc', outline=color, width=w)
    canvas.create_line(cx - 0.38 * s, cy - 0.06 * s, cx - 0.38 * s, cy + 0.26 * s,
                       fill=color, width=w)
    canvas.create_line(cx + 0.38 * s, cy - 0.06 * s, cx + 0.38 * s, cy + 0.26 * s,
                       fill=color, width=w)
    canvas.create_line(cx - 0.48 * s, cy + 0.26 * s, cx + 0.48 * s, cy + 0.26 * s,
                       fill=color, width=w)
    canvas.create_oval(cx - 0.1 * s, cy + 0.30 * s, cx + 0.1 * s, cy + 0.46 * s,
                       outline=color, fill=color)


def _draw_clock(canvas, s, w, cx, cy, color):
    canvas.create_oval(cx - 0.45 * s, cy - 0.45 * s, cx + 0.45 * s, cy + 0.45 * s,
                       outline=color, width=w)
    canvas.create_line(cx, cy, cx, cy - 0.28 * s, fill=color, width=w)
    canvas.create_line(cx, cy, cx + 0.24 * s, cy + 0.12 * s, fill=color, width=w)


def _draw_briefcase(canvas, s, w, cx, cy, color):
    canvas.create_rectangle(cx - 0.48 * s, cy - 0.24 * s, cx + 0.48 * s, cy + 0.42 * s,
                            outline=color, width=w)
    canvas.create_rectangle(cx - 0.18 * s, cy - 0.44 * s, cx + 0.18 * s, cy - 0.24 * s,
                            outline=color, width=w)
    canvas.create_line(cx - 0.48 * s, cy + 0.06 * s, cx + 0.48 * s, cy + 0.06 * s,
                       fill=color, width=w)


def _draw_store(canvas, s, w, cx, cy, color):
    canvas.create_polygon(cx - 0.5 * s, cy - 0.24 * s,
                          cx - 0.34 * s, cy - 0.46 * s,
                          cx + 0.34 * s, cy - 0.46 * s,
                          cx + 0.5 * s, cy - 0.24 * s,
                          outline=color, width=w)
    canvas.create_rectangle(cx - 0.42 * s, cy - 0.24 * s, cx + 0.42 * s, cy + 0.44 * s,
                            outline=color, width=w)
    canvas.create_rectangle(cx - 0.12 * s, cy + 0.06 * s, cx + 0.12 * s, cy + 0.44 * s,
                            outline=color, width=w)


def _draw_pin(canvas, s, w, cx, cy, color):
    canvas.create_oval(cx - 0.32 * s, cy - 0.48 * s, cx + 0.32 * s, cy + 0.16 * s,
                       outline=color, width=w)
    canvas.create_polygon(cx - 0.24 * s, cy + 0.02 * s,
                          cx + 0.24 * s, cy + 0.02 * s,
                          cx, cy + 0.5 * s,
                          outline=color, width=w)
    canvas.create_oval(cx - 0.1 * s, cy - 0.28 * s, cx + 0.1 * s, cy - 0.08 * s,
                       outline=color)


def _draw_mail(canvas, s, w, cx, cy, color):
    canvas.create_rectangle(cx - 0.5 * s, cy - 0.32 * s, cx + 0.5 * s, cy + 0.32 * s,
                            outline=color, width=w)
    canvas.create_line(cx - 0.5 * s, cy - 0.32 * s, cx, cy + 0.04 * s,
                       fill=color, width=w)
    canvas.create_line(cx + 0.5 * s, cy - 0.32 * s, cx, cy + 0.04 * s,
                       fill=color, width=w)


def _draw_verified(canvas, s, w, cx, cy, color):
    canvas.create_oval(cx - 0.5 * s, cy - 0.5 * s, cx + 0.5 * s, cy + 0.5 * s,
                       outline=color, fill=color)
    canvas.create_line(cx - 0.24 * s, cy + 0.02 * s, cx - 0.06 * s, cy + 0.2 * s,
                       fill='#ffffff', width=w + 1)
    canvas.create_line(cx - 0.06 * s, cy + 0.2 * s, cx + 0.26 * s, cy - 0.2 * s,
                       fill='#ffffff', width=w + 1)


def _draw_logout(canvas, s, w, cx, cy, color):
    canvas.create_line(cx - 0.46 * s, cy - 0.4 * s, cx - 0.14 * s, cy - 0.4 * s,
                       fill=color, width=w)
    canvas.create_line(cx - 0.46 * s, cy - 0.4 * s, cx - 0.46 * s, cy + 0.4 * s,
                       fill=color, width=w)
    canvas.create_line(cx - 0.46 * s, cy + 0.4 * s, cx - 0.14 * s, cy + 0.4 * s,
                       fill=color, width=w)
    canvas.create_line(cx - 0.12 * s, cy, cx + 0.46 * s, cy, fill=color, width=w)
    canvas.create_polygon(cx + 0.46 * s, cy,
                          cx + 0.2 * s, cy - 0.16 * s,
                          cx + 0.2 * s, cy + 0.16 * s,
                          fill=color)


def _draw_edit(canvas, s, w, cx, cy, color):
    canvas.create_polygon(cx - 0.42 * s, cy + 0.42 * s,
                          cx - 0.24 * s, cy + 0.34 * s,
                          cx + 0.36 * s, cy - 0.26 * s,
                          cx + 0.18 * s, cy - 0.44 * s,
                          cx - 0.42 * s, cy + 0.16 * s,
                          outline=color, width=w)
    canvas.create_line(cx - 0.42 * s, cy + 0.42 * s, cx + 0.5 * s, cy + 0.42 * s,
                       fill=color, width=w)


def _draw_shield(canvas, s, w, cx, cy, color):
    canvas.create_polygon(cx, cy - 0.5 * s,
                          cx + 0.42 * s, cy - 0.28 * s,
                          cx + 0.42 * s, cy + 0.12 * s,
                          cx, cy + 0.5 * s,
                          cx - 0.42 * s, cy + 0.12 * s,
                          cx - 0.42 * s, cy - 0.28 * s,
                          outline=color, fill=color, width=w)
    canvas.create_line(cx - 0.2 * s, cy, cx - 0.02 * s, cy + 0.18 * s,
                       fill='#ffffff', width=w)
    canvas.create_line(cx - 0.02 * s, cy + 0.18 * s, cx + 0.22 * s, cy - 0.14 * s,
                       fill='#ffffff', width=w)


def _draw_pos(canvas, s, w, cx, cy, color):
    canvas.create_rectangle(cx - 0.4 * s, cy - 0.5 * s, cx + 0.4 * s, cy + 0.5 * s,
                            outline=color, width=w)
    canvas.create_rectangle(cx - 0.28 * s, cy - 0.38 * s, cx + 0.28 * s, cy - 0.18 * s,
                            outline=color, width=w)
    for row in range(2):
        for col in range(3):
            x = cx - 0.24 * s + col * 0.24 * s
            y = cy + 0.02 * s + row * 0.24 * s
            canvas.create_oval(x - 0.05 * s, y - 0.05 * s, x + 0.05 * s, y + 0.05 * s,
                               outline=color, fill=color)


ICON_DRAWERS = {
    'chat': _draw_chat,
    'bell': _draw_bell,
    'clock': _draw_clock,
    'briefcase': _draw_briefcase,
    'store': _draw_store,
    'pin': _draw_pin,
    'mail': _draw_mail,
    'verified': _draw_verified,
    'logout': _draw_logout,
    'edit': _draw_edit,
    'shield': _draw_shield,
    'pos': _draw_pos,
}


def draw_icon(canvas, kind, size, color, cx, cy, width=None):
    """Draw ``kind`` on ``canvas`` centred at ``(cx, cy)`` scaled to ``size``."""
    drawer = ICON_DRAWERS.get(kind)
    if drawer is None:
        return
    line_width = width if width else max(1, int(round(size / 9)))
    drawer(canvas, size, line_width, cx, cy, color)


def icon_label(parent, kind, size, color, bg, padx=0, pady=0, cursor=''):
    """Return a tiny :class:`tk.Canvas` that renders a single icon."""
    canvas = tk.Canvas(parent, width=size + padx, height=size + pady,
                       bg=bg, highlightthickness=0, bd=0)
    if cursor:
        canvas.configure(cursor=cursor)
    cx = (size + padx) / 2
    cy = (size + pady) / 2
    draw_icon(canvas, kind, size, color, cx, cy)
    return canvas
