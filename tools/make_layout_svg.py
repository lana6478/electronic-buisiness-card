"""Draw docs/layout.svg: the perfboard from the front (parts) and from the back
(soldering side, mirrored), with every wire numbered.

    python3 tools/make_layout_svg.py docs/layout.svg

The board is 33 x 19 holes (numbers 1-33 along the long edge, letters A-S
across the short edge), with a strip of long pads beyond row A. It's drawn
with the S edge (where the screen header pins are) at the top.

Positions in this file are (number, row) seen from the FRONT, where row 1 is
letter S and row 19 is letter A. No extra libraries needed.
"""
import math, sys

P = 26                 # px per hole
NC, NR = 33, 19        # numbers, letters
BX = 64                # board left x
W = 1330

def letter(r): return chr(ord("S") - (r - 1))
def hole(c, r): return f"{letter(r)}{c}"

def X(c, view):
    return BX + ((c - 0.5) if view == "front" else (NC + 0.5 - c)) * P
def Y(r, by):
    return by + (r - 0.5) * P

out = []
def add(s): out.append(s)
def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def text(x, y, s, size=11, anchor="start", fill="#222", weight="normal", rot=None, halo=False, italic=False):
    pos = (f'x="0" y="0" transform="translate({x:.1f} {y:.1f}) rotate({rot})"' if rot is not None
           else f'x="{x:.1f}" y="{y:.1f}"')
    st = ' font-style="italic"' if italic else ""
    base = f'font-size="{size}" text-anchor="{anchor}" font-weight="{weight}"{st}'
    if halo:
        add(f'<text {pos} {base} fill="#ffffff" stroke="#ffffff" stroke-width="3.5" stroke-linejoin="round">{esc(s)}</text>')
    add(f'<text {pos} {base} fill="{fill}">{esc(s)}</text>')

def rect_cr(c1, c2, r1, r2, view, by, **kw):
    xa, xb = sorted((X(c1, view), X(c2, view)))
    ya, yb = Y(r1, by), Y(r2, by)
    attrs = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in kw.items())
    add(f'<rect x="{xa:.1f}" y="{ya:.1f}" width="{xb - xa:.1f}" height="{yb - ya:.1f}" {attrs}/>')

# ---------------------------------------------------------------- parts (front coords)
TFT_PINS = ["GND", "VCC", "SCL", "SDA", "RES", "DC", "CS", "BLK"]
TFT = {n: (4 + i, 1) for i, n in enumerate(TFT_PINS)}            # S4-S11
OLED_PINS = ["GND", "VDD", "SCK", "SDA"]
OLED = {n: (27 + i, 1) for i, n in enumerate(OLED_PINS)}          # S27-S30
MCU_L = ["5V", "GND", "3V3", "GPIO4", "GPIO3", "GPIO2", "GPIO1", "GPIO0"]       # number 16, R..K
MCU_R = ["GPIO5", "GPIO6", "GPIO7", "GPIO8", "GPIO9", "GPIO10", "GPIO20", "GPIO21"]  # number 22, R..K
MCU = {}
for i, n in enumerate(MCU_L): MCU[n] = (16, 2 + i)
for i, n in enumerate(MCU_R): MCU[n] = (22, 2 + i)
USED_MCU = {"5V", "GND", "3V3", "GPIO4", "GPIO3", "GPIO1", "GPIO5", "GPIO6", "GPIO7", "GPIO8", "GPIO9", "GPIO10"}
BTN = {"A": (18, 14), "B": (20, 14), "C": (18, 17), "D": (20, 17)}   # F18 F20 C18 C20
SW = [(33, 15), (33, 16), (33, 17)]                                  # E33 D33 C33
ALL_PINS = list(TFT.values()) + list(OLED.values()) + list(MCU.values()) + list(BTN.values()) + SW

# on the back (front coords)
TP = (23.6, 30.4, 10.6, 19.9)          # c1 c2 r1 r2, USB-C at the bottom end
TP_USB = (25.6, 28.4, 19.0, 21.2)
TP_PADS = {"OUT+": (24.3, 11.3), "B+": (26.1, 11.3), "B-": (27.9, 11.3), "OUT-": (29.7, 11.3)}
BAT = (1.6, 13.4, 3.0, 11.0)
BAT_LEADS = {"red": (13.4, 6.4), "black": (13.4, 7.6)}

GND_C, V33_C, V5_C = "#111111", "#e63946", "#f77f00"
G_PWR, G_SIG, G_BAT = "Power (3V3 + GND)", "Screen + button signals", "Battery (do last)"
def nm(p):
    return hole(*p) if isinstance(p[0], int) else ""
wires = [
    (1, TFT["GND"], MCU["GND"], GND_C, "TFT GND → board GND", G_PWR),
    (2, TFT["VCC"], MCU["3V3"], V33_C, "TFT VCC → board 3V3", G_PWR),
    (3, OLED["GND"], MCU["GND"], GND_C, "OLED GND → board GND", G_PWR),
    (4, OLED["VDD"], MCU["3V3"], V33_C, "OLED VDD → board 3V3", G_PWR),
    (5, BTN["C"], MCU["GND"], GND_C, "Button leg C → board GND", G_PWR),
    (6, TFT["SCL"], MCU["GPIO4"], "#2a9d8f", "TFT SCL → GPIO4", G_SIG),
    (7, TFT["SDA"], MCU["GPIO6"], "#3a86ff", "TFT SDA → GPIO6", G_SIG),
    (8, TFT["RES"], MCU["GPIO1"], "#8338ec", "TFT RES → GPIO1", G_SIG),
    (9, TFT["DC"], MCU["GPIO10"], "#ff006e", "TFT DC → GPIO10", G_SIG),
    (10, TFT["CS"], MCU["GPIO7"], "#6c757d", "TFT CS → GPIO7", G_SIG),
    (11, TFT["BLK"], MCU["GPIO3"], "#c9a227", "TFT BLK → GPIO3", G_SIG),
    (12, OLED["SCK"], MCU["GPIO9"], "#06a77d", "OLED SCK → GPIO9", G_SIG),
    (13, OLED["SDA"], MCU["GPIO8"], "#118ab2", "OLED SDA → GPIO8", G_SIG),
    (14, BTN["B"], MCU["GPIO5"], "#8d5524", "Button leg B → GPIO5", G_SIG),
    (15, SW[2], MCU["5V"], V5_C, "Switch outer pin → diode → 5V", G_BAT),
    (16, TP_PADS["OUT+"], SW[1], V5_C, "TP4056 OUT+ → switch middle", G_BAT),
    (17, TP_PADS["OUT-"], BTN["C"], GND_C, "TP4056 OUT− → button leg C (GND)", G_BAT),
    (18, BAT_LEADS["red"], TP_PADS["B+"], V33_C, "LiPo red → TP4056 B+", G_BAT),
    (19, BAT_LEADS["black"], TP_PADS["B-"], GND_C, "LiPo black → TP4056 B−", G_BAT),
]
BEND = {}   # manual bend overrides by wire number

def bez(a, ctrl, b, t):
    u = 1 - t
    return (u*u*a[0] + 2*u*t*ctrl[0] + t*t*b[0], u*u*a[1] + 2*u*t*ctrl[1] + t*t*b[1])

def control(a, b, k):
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy) or 1
    return (mx - dy / L * k, my + dx / L * k)

def clearance(a, b, k):
    c = control(a, b, k)
    worst = 9
    for i in range(1, 80):
        p = bez(a, c, b, i / 80)
        for q in ALL_PINS:
            if math.dist(q, a) < 0.1 or math.dist(q, b) < 0.1:
                continue
            worst = min(worst, math.dist(p, q))
    return worst

def pick_bend(a, b):
    for k in [0, 0.5, -0.5, 0.8, -0.8, 1.1, -1.1, 1.5, -1.5, 2, -2, 2.5, -2.5, 3, -3, 4, -4]:
        if clearance(a, b, k) > 0.42:
            return k
    return 0

# ---------------------------------------------------------------- drawing helpers
def board(view, by):
    add(f'<rect x="{BX - 0.3 * P:.1f}" y="{by - 0.25 * P:.1f}" width="{(NC + 0.6) * P:.1f}" height="{(NR + 1.55) * P:.1f}" rx="7" fill="#efe3c4" stroke="#8a7650" stroke-width="2"/>')
    for c in range(1, NC + 1):
        for r in range(1, NR + 1):
            add(f'<circle cx="{X(c, view):.1f}" cy="{Y(r, by):.1f}" r="4.2" fill="#d4a65a" stroke="#a87b33" stroke-width="0.8"/>'
                f'<circle cx="{X(c, view):.1f}" cy="{Y(r, by):.1f}" r="1.6" fill="#5b4a2a"/>')
        # long pads strip beyond row A
        add(f'<rect x="{X(c, view) - 5:.1f}" y="{Y(NR + 0.65, by):.1f}" width="10" height="{0.75 * P:.1f}" rx="3" fill="#cfcfcf" stroke="#999" stroke-width="0.8"/>')
    for c in range(1, NC + 1):
        if c in (1, 33) or c % 5 == 0 or c in (4, 11, 16, 22, 27, 30):
            text(X(c, view), by + (NR + 1.3) * P + 14, str(c), 10, "middle", "#665")
    for r in range(1, NR + 1):
        text(BX - 0.3 * P - 6, Y(r, by) + 4, letter(r), 10, "end", "#665", "bold")

def pin(c, r, view, by, fill="#c0c0c0"):
    add(f'<rect x="{X(c, view) - 5:.1f}" y="{Y(r, by) - 5:.1f}" width="10" height="10" rx="1.5" fill="{fill}" stroke="#555" stroke-width="1"/>')

def solder(c, r, view, by):
    add(f'<circle cx="{X(c, view):.1f}" cy="{Y(r, by):.1f}" r="5.6" fill="#d9d9d9" stroke="#666" stroke-width="1.2"/>')

def header_labels(pins, title, view, by):
    for n, (c, r) in pins.items():
        text(X(c, view) + 4, by - 0.25 * P - 6, n, 10.5, "start", "#222", "bold", rot=-90)
    cs = [X(c, view) for c, _ in pins.values()]
    xa, xb = min(cs), max(cs)
    add(f'<path d="M{xa - 6:.1f} {by - 46:.1f} H{xb + 6:.1f}" stroke="#555" stroke-width="1.2"/>')
    text((xa + xb) / 2, by - 51, title, 12, "middle", "#222", "bold")

def mcu_labels(view, by, dark):
    col = "#fff" if dark else "#222"
    cx = (X(16, view) + X(22, view)) / 2
    for n, (c, r) in MCU.items():
        used = n in USED_MCU
        fill = col if used else "#999"
        x = X(c, view)
        if x < cx:
            text(x + 9, Y(r, by) + 3.5, n, 9.5, "start", fill, "bold" if used else "normal", halo=not dark)
        else:
            text(x - 9, Y(r, by) + 3.5, n, 9.5, "end", fill, "bold" if used else "normal", halo=not dark)

def mcu_body(view, by, ghost=False):
    if ghost:
        rect_cr(15.35, 22.65, 1.0, 9.9, view, by, rx=4, fill="none", stroke="#9aa", stroke_width="1.3", stroke_dasharray="5 4")
        rect_cr(17.6, 20.4, -0.9, 1.6, view, by, rx=3, fill="#e3e3e3", stroke="#888", stroke_dasharray="4 3")
    else:
        rect_cr(15.35, 22.65, 1.0, 9.9, view, by, rx=4, fill="#2b2b2b")
        rect_cr(17.6, 20.4, -0.9, 1.6, view, by, rx=3, fill="#b8b8b8", stroke="#666")

# ================================================================= FRONT
add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} HEIGHT" font-family="Helvetica, Arial, sans-serif">')
add(f'<rect width="{W}" height="HEIGHT" fill="#ffffff"/>')
text(W / 2, 32, "Perfboard layout: ESP32-C3 SuperMini, 33 × 19 hole board", 22, "middle", "#222", "bold")
text(W / 2, 54, "Top: the front, where the parts go.  Bottom: the back, where you solder, flipped left-to-right like turning the board over.", 13, "middle", "#555")
text(W / 2, 72, "Holes are named letter + number, like on the board: S4 = row S, column 4.", 13, "middle", "#555")

FY = 170
v = "front"
text(BX, FY - 78, "1  FRONT  (parts side)", 16, "start", "#1d3557", "bold")
board(v, FY)
# TFT
rect_cr(0.4, 14.6, 0.35, 19.9, v, FY, rx=6, fill="#1d3557", opacity="0.96")
rect_cr(1.6, 13.4, 2.6, 18.2, v, FY, rx=10, fill="#a8dadc")
mx = (X(0.4, v) + X(14.6, v)) / 2
text(mx, Y(9.8, FY), '1.69" TFT', 16, "middle", "#1d3557", "bold")
text(mx, Y(9.8, FY) + 18, "photo screen", 12, "middle", "#1d3557")
text(mx, Y(9.8, FY) + 34, "pins in S4 – S11", 12, "middle", "#1d3557", "bold")
for c, r in TFT.values(): pin(c, r, v, FY)
header_labels(TFT, "TFT pins: S4 – S11", v, FY)
# OLED
rect_cr(23.9, 33.9, 0.35, 11.0, v, FY, rx=6, fill="#1d3557", opacity="0.96")
rect_cr(24.8, 33.0, 2.6, 4.0, v, FY, fill="#ffd60a")
rect_cr(24.8, 33.0, 4.0, 8.6, v, FY, fill="#4cc9f0")
mx = (X(23.9, v) + X(33.9, v)) / 2
text(mx, Y(9.6, FY) + 4, '0.96" OLED', 12, "middle", "#fff", "bold")
for c, r in OLED.values(): pin(c, r, v, FY)
header_labels(OLED, "OLED pins: S27 – S30", v, FY)
# MCU
mcu_body(v, FY)
text(X(19, v), Y(-0.9, FY) - 4, "USB-C (programming) over the top edge", 11, "middle", "#222", "bold")
add(f'<rect x="{X(17.9, v):.1f}" y="{Y(5.2, FY):.1f}" width="{2.2 * P:.1f}" height="{1.6 * P:.1f}" fill="#444" stroke="#777"/>')
text(X(19, v), Y(6.0, FY) + 3, "C3", 10, "middle", "#ddd", "bold")
for n, (c, r) in MCU.items(): pin(c, r, v, FY, "#d9b84a")
mcu_labels(v, FY, True)
text(X(19, v), Y(10.7, FY) + 4, "SuperMini: pins in columns 16 and 22, rows R – K", 10.5, "middle", "#222", "bold", halo=True)
# button
rect_cr(17.7, 20.3, 14.4, 16.6, v, FY, rx=3, fill="#3a3a3a")
add(f'<circle cx="{X(19, v):.1f}" cy="{Y(15.5, FY):.1f}" r="{P * 0.75:.1f}" fill="#e63946"/>')
for lab, (c, r) in BTN.items():
    pin(c, r, v, FY)
    text(X(c, v) + (-10 if c == 18 else 10), Y(r, FY) + 4, lab, 10, "end" if c == 18 else "start", "#000", "bold", halo=True)
text(X(19, v), Y(18.4, FY) + 4, "button: legs F18 F20 C18 C20", 10.5, "middle", "#222", "bold", halo=True)
# switch
rect_cr(32.3, 33.7, 14.0, 18.0, v, FY, rx=2, fill="#8d99ae", stroke="#555")
rect_cr(33.5, 34.6, 15.5, 16.5, v, FY, rx=1, fill="#333")
for c, r in SW: pin(c, r, v, FY)
text(X(32.1, v), Y(16, FY) - 30, "on/off switch", 10.5, "end", "#222", "bold", halo=True)
text(X(32.1, v), Y(16, FY) - 17, "E33 D33 C33", 10, "end", "#222", halo=True)
text(X(32.1, v), Y(16, FY) - 4, "lever out of the right edge", 10, "end", "#444", halo=True)

NX = BX + NC * P + 50
def note_block(lines, y, x=NX):
    for i, (s, b) in enumerate(lines):
        text(x, y + i * 17, s, 12.5, "start", "#222" if b else "#444", "bold" if b else "normal")
    return y + len(lines) * 17
note_block([
    ("Hold it this way up", True),
    ("Screen pins (row S) at the top, the", False),
    ("long pads at the bottom. Both screens", False),
    ("are then the right way up, so the", False),
    ("firmware needs no changes.", False),
    ("", False),
    ("From your photo", True),
    ("TFT pins: S4 – S11", False),
    ("SuperMini: top edge R16 – R22", False),
    ("OLED pins: S27 – S30", False),
    ("", False),
    ("Check before soldering", True),
    ("The TFT pin order (GND at S4) and the", False),
    ("SuperMini pins (5V at R16, GPIO5 at", False),
    ("R22) are the usual ones. Check them", False),
    ("against the printing on your boards.", False),
    ("The button and switch holes are my", False),
    ("guess: any holes work, just keep the", False),
    ("same legs on the same wires.", False),
], FY - 10)

# ================================================================= BACK
BY = FY + (NR + 1.6) * P + 150
v = "back"
text(BX, BY - 78, "2  BACK  (soldering side, board turned over)", 16, "start", "#7b2d26", "bold")
board(v, BY)
rect_cr(0.4, 14.6, 0.35, 19.9, v, BY, rx=5, fill="none", stroke="#9aa", stroke_width="1.3", stroke_dasharray="5 4")
rect_cr(23.9, 33.9, 0.35, 11.0, v, BY, rx=5, fill="none", stroke="#9aa", stroke_width="1.3", stroke_dasharray="5 4")
mcu_body(v, BY, ghost=True)
text(X(19, v), Y(-0.9, BY) - 4, "USB-C (SuperMini)", 11, "middle", "#444", "bold")
for p in ALL_PINS: solder(p[0], p[1], v, BY)
header_labels(TFT, "TFT pins: S4 – S11", v, BY)
header_labels(OLED, "OLED pins: S27 – S30", v, BY)

badge_pos, layers = [], []
for (n, a, b, colr, label, group) in wires:
    k = BEND.get(n, pick_bend(a, b))
    c = control(a, b, k)
    A = (X(a[0], v), Y(a[1], BY)); C = (X(c[0], v), Y(c[1], BY)); B = (X(b[0], v), Y(b[1], BY))
    d = f"M{A[0]:.1f} {A[1]:.1f} Q{C[0]:.1f} {C[1]:.1f} {B[0]:.1f} {B[1]:.1f}"
    add(f'<path d="{d}" stroke="#ffffff" stroke-width="6" fill="none" stroke-linecap="round" opacity="0.9"/>'
        f'<path d="{d}" stroke="{colr}" stroke-width="3.2" fill="none" stroke-linecap="round"/>')
    if n == 15:
        t = 0.8
    else:
        best = None
        for t_ in [0.5, 0.4, 0.6, 0.3, 0.7, 0.25, 0.75, 0.35, 0.65]:
            p = bez(a, c, b, t_)
            score = min(min([math.dist(p, q) for q in badge_pos] + [9]), 1.6) + min(min(math.dist(p, q) for q in ALL_PINS), 0.8)
            if best is None or score > best[0] + 1e-6:
                best = (score, t_)
        t = best[1]
    p = bez(a, c, b, t)
    badge_pos.append(p)
    layers.append(("badge", n, p, colr))
    if n == 15:
        q1, q2 = bez(a, c, b, 0.47), bez(a, c, b, 0.53)
        ang = math.degrees(math.atan2(Y(q2[1], BY) - Y(q1[1], BY), X(q2[0], v) - X(q1[0], v)))
        dp = bez(a, c, b, 0.5)
        badge_pos.append(dp)
        layers.append(("diode", (X(dp[0], v), Y(dp[1], BY)), ang))

mcu_labels(v, BY, False)
for lab, (c, r) in BTN.items():
    if lab in ("B", "C"):
        text(X(c, v) + (10 if c == 18 else -10), Y(r, BY) + 4, lab, 10, "start" if c == 18 else "end", "#000", "bold", halo=True)
text(X(19, v), Y(18.4, BY) + 4, "button (use legs B and C)", 10, "middle", "#333", "bold", halo=True)
text(X(33, v) + 10, Y(15, BY) + 4, "switch", 10, "start", "#333", "bold", halo=True)
text(X(33, v) + 10, Y(16, BY) + 4, "middle", 9, "start", "#333", halo=True)
text(X(33, v) + 10, Y(17, BY) + 4, "outer", 9, "start", "#333", halo=True)

# TP4056 + battery outlines on top
rect_cr(*TP, v, BY, rx=4, fill="none", stroke="#1d3557", stroke_width="2.2", stroke_dasharray="7 4")
rect_cr(*TP_USB, v, BY, rx=3, fill="#c8c8c8", stroke="#666")
mx = (X(TP[0], v) + X(TP[1], v)) / 2
text(mx, Y(14.6, BY), "TP4056", 13, "middle", "#1d3557", "bold", halo=True)
text(mx, Y(15.4, BY) + 2, "charger, foam-taped on", 9.5, "middle", "#1d3557", halo=True)
text(mx, Y(21.6, BY) + 8, "USB-C (charging) over the bottom edge", 10.5, "middle", "#1d3557", "bold")
for name, (c, r) in TP_PADS.items():
    x, y = X(c, v), Y(r, BY)
    add(f'<rect x="{x - 5:.1f}" y="{y - 6:.1f}" width="10" height="12" rx="1" fill="#e0b050" stroke="#7a5a1a"/>')
    text(x, y + 18, name.replace("-", "−"), 9.5, "middle", "#1d3557", "bold", halo=True)
rect_cr(*BAT, v, BY, rx=8, fill="none", stroke="#b8860b", stroke_width="2.2", stroke_dasharray="7 4")
bx_mid = (X(BAT[0], v) + X(BAT[1], v)) / 2
add(f'<rect x="{bx_mid - 140:.1f}" y="{Y(BAT[3], BY) - 10:.1f}" width="280" height="20" rx="4" fill="#fff3cf" stroke="#b8860b" stroke-width="1.5"/>')
text(bx_mid, Y(BAT[3], BY) + 4.5, "LiPo: goes on LAST, on kapton tape", 11, "middle", "#7a5a00", "bold")
for colr, (c, r) in [("#e63946", BAT_LEADS["red"]), ("#111", BAT_LEADS["black"])]:
    add(f'<circle cx="{X(c, v):.1f}" cy="{Y(r, BY):.1f}" r="4" fill="{colr}" stroke="#fff" stroke-width="1"/>')

for w in layers:
    if w[0] == "diode":
        _, (dx, dy), ang = w
        ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        pt = lambda u, w_: f"{dx + u * ca - w_ * sa:.1f},{dy + u * sa + w_ * ca:.1f}"
        add(f'<polygon points="{pt(-16,-7)} {pt(16,-7)} {pt(16,7)} {pt(-16,7)}" fill="#222" stroke="#fff" stroke-width="1.5" stroke-linejoin="round"/>')
        add(f'<polygon points="{pt(8,-7)} {pt(13,-7)} {pt(13,7)} {pt(8,7)}" fill="#e6e6e6"/>')
        text(dx, dy - 30, "1N5817 diode", 10.5, "middle", "#000", "bold", halo=True)
        text(dx, dy - 17, "stripe end towards 5V", 10, "middle", "#000", halo=True)
for w in layers:
    if w[0] == "badge":
        _, n, p, colr = w
        x, y = X(p[0], v), Y(p[1], BY)
        add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="{colr}" stroke="#fff" stroke-width="1.8"/>')
        text(x, y + 4, str(n), 10.5, "middle", "#fff", "bold")

# wire list
lx, ly = NX, BY - 60
text(lx, ly, "Wire list (tick them off)", 15, "start", "#222", "bold")
group = None
for (n, a, b, colr, label, g) in wires:
    if g != group:
        group = g
        ly += 26
        text(lx, ly, g, 12.5, "start", "#555", "bold")
        ly += 4
    ly += 19
    add(f'<rect x="{lx:.1f}" y="{ly - 11:.1f}" width="12" height="12" rx="2" fill="none" stroke="#777"/>')
    add(f'<circle cx="{lx + 28:.1f}" cy="{ly - 5:.1f}" r="8.5" fill="{colr}"/>')
    text(lx + 28, ly - 1, str(n), 10, "middle", "#fff", "bold")
    ends = " ".join(x for x in (nm(a), nm(b)) if x)
    text(lx + 42, ly, label + (f"  ({ends.replace(' ', ' → ')})" if ends else ""), 11.5, "start", "#222")
ly = note_block([
    ("Tips", True),
    ("Real wires don't have to follow these lines:", False),
    ("keep them flat. A wire only joins a pin at", False),
    ("its ends. Board GND (Q16) takes wires 1, 3", False),
    ("and 5. Button leg C takes wires 5 and 17.", False),
], ly + 34)

foot = BY + (NR + 1.3) * P + 74
text(BX, foot, "Seen from the back, the TFT is on the RIGHT and the OLED on the LEFT. Numbers run 33 → 1.", 12.5, "start", "#7b2d26", "bold")
text(BX, foot + 18, "Full pin table: WIRING.md", 12, "start", "#555")
H = max(ly, foot + 18) + 30
add("</svg>")
open(sys.argv[1], "w").write("\n".join(out).replace("HEIGHT", str(int(H))))
for (n, a, b, colr, label, g) in wires:
    k = BEND.get(n, pick_bend(a, b))
    print(n, label, "bend", k, "clear", round(clearance(a, b, k), 2))
