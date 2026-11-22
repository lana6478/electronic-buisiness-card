"""Draw docs/layout.svg: the perfboard from the front (parts) and from the back
(soldering side, mirrored), with every wire numbered.

    python3 tools/make_layout_svg.py docs/layout.svg

Part positions are in (column, row) hole numbers as seen from the FRONT.
No extra libraries needed.
"""
import math, sys

P = 26            # px per hole
COLS, ROWS = 24, 18
BX = 70           # board left x
W = 1100

def X(c, view):
    return BX + ((c - 0.5) if view == "front" else (24.5 - c)) * P

def Y(r, by):
    return by + (r - 0.5) * P

out = []
def add(s): out.append(s)

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def text(x, y, s, size=11, anchor="start", fill="#222", weight="normal", rot=None, halo=False, italic=False):
    if rot is not None:
        pos = f'x="0" y="0" transform="translate({x:.1f} {y:.1f}) rotate({rot})"'
    else:
        pos = f'x="{x:.1f}" y="{y:.1f}"'
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
TFT = {n: (3 + i, 1) for i, n in enumerate(TFT_PINS)}
OLED_PINS = ["GND", "VCC", "SCL", "SDA"]
OLED = {n: (17 + i, 1) for i, n in enumerate(OLED_PINS)}
MCU_TOP = ["GPIO0", "GPIO1", "GPIO2", "GPIO3", "GPIO4", "3V3", "GND", "5V"]
MCU_BOT = ["GPIO21", "GPIO20", "GPIO10", "GPIO9", "GPIO8", "GPIO7", "GPIO6", "GPIO5"]
MCU = {}
for i, n in enumerate(MCU_TOP): MCU[n] = (16 + i, 12)
for i, n in enumerate(MCU_BOT): MCU[n] = (16 + i, 18)
BTN = [(13, 13), (15, 13), (13, 15), (15, 15)]
SW = [(5, 18), (6, 18), (7, 18)]
USED_MCU = {"GPIO1", "GPIO3", "GPIO4", "3V3", "GND", "5V", "GPIO10", "GPIO9", "GPIO8", "GPIO7", "GPIO6", "GPIO5"}

ALL_PINS = list(TFT.values()) + list(OLED.values()) + list(MCU.values()) + BTN + SW

# TP4056 and LiPo sit on the back (front coords)
TP = (-0.6, 9.6, 9.4, 16.2)        # c1 c2 r1 r2 ; USB-C at the c1 end
TP_PADS = {"OUT+": (9.0, 10.1), "B+": (9.0, 12.0), "B-": (9.0, 13.6), "OUT-": (9.0, 15.5)}
BAT = (12.2, 24.2, 2.0, 9.9)
BAT_LEADS = {"red": (12.2, 5.2), "black": (12.2, 6.6)}

# ---------------------------------------------------------------- wires
GND_C, V33_C, V5_C = "#111111", "#e63946", "#f77f00"
wires = [
    # n, from, to, colour, label, group, bend override
    (1, TFT["GND"], OLED["GND"], GND_C, "TFT GND → OLED GND", "Power (3V3 + GND)", 2.4),
    (2, OLED["GND"], MCU["GND"], GND_C, "OLED GND → board GND", "Power (3V3 + GND)", None),
    (3, BTN[0], MCU["GND"], GND_C, "Button leg A → board GND", "Power (3V3 + GND)", None),
    (4, TFT["VCC"], OLED["VCC"], V33_C, "TFT VCC → OLED VCC", "Power (3V3 + GND)", 3.4),
    (5, OLED["VCC"], MCU["3V3"], V33_C, "OLED VCC → board 3V3", "Power (3V3 + GND)", None),
    (6, TFT["SCL"], MCU["GPIO4"], "#2a9d8f", "TFT SCL → GPIO4", "Screen + button signals", None),
    (7, TFT["SDA"], MCU["GPIO6"], "#3a86ff", "TFT SDA → GPIO6", "Screen + button signals", None),
    (8, TFT["RES"], MCU["GPIO1"], "#8338ec", "TFT RES → GPIO1", "Screen + button signals", None),
    (9, TFT["DC"], MCU["GPIO10"], "#ff006e", "TFT DC → GPIO10", "Screen + button signals", None),
    (10, TFT["CS"], MCU["GPIO7"], "#6c757d", "TFT CS → GPIO7", "Screen + button signals", None),
    (11, TFT["BLK"], MCU["GPIO3"], "#c9a227", "TFT BLK → GPIO3", "Screen + button signals", None),
    (12, OLED["SCL"], MCU["GPIO9"], "#06a77d", "OLED SCL → GPIO9", "Screen + button signals", None),
    (13, OLED["SDA"], MCU["GPIO8"], "#118ab2", "OLED SDA → GPIO8", "Screen + button signals", None),
    (14, BTN[3], MCU["GPIO5"], "#8d5524", "Button leg D → GPIO5", "Screen + button signals", None),
    (15, SW[2], MCU["5V"], V5_C, "Switch outer pin → diode → 5V", "Battery (do last)", None),
    (16, TP_PADS["OUT+"], SW[1], V5_C, "TP4056 OUT+ → switch middle", "Battery (do last)", None),
    (17, TP_PADS["OUT-"], BTN[0], GND_C, "TP4056 OUT− → button leg A (GND)", "Battery (do last)", None),
    (18, BAT_LEADS["red"], TP_PADS["B+"], V33_C, "LiPo red → TP4056 B+", "Battery (do last)", None),
    (19, BAT_LEADS["black"], TP_PADS["B-"], GND_C, "LiPo black → TP4056 B−", "Battery (do last)", None),
]

def bez(a, ctrl, b, t):
    u = 1 - t
    return (u*u*a[0] + 2*u*t*ctrl[0] + t*t*b[0], u*u*a[1] + 2*u*t*ctrl[1] + t*t*b[1])

def control(a, b, k):
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    return (mx + nx * k, my + ny * k)

def clearance(a, b, k):
    c = control(a, b, k)
    worst = 9
    for i in range(1, 60):
        p = bez(a, c, b, i / 60)
        for q in ALL_PINS:
            if math.dist(q, a) < 0.1 or math.dist(q, b) < 0.1:
                continue
            worst = min(worst, math.dist(p, q))
    return worst

def pick_bend(a, b):
    for k in [0, 0.5, -0.5, 0.8, -0.8, 1.1, -1.1, 1.5, -1.5, 2, -2, 2.5, -2.5, 3, -3]:
        if clearance(a, b, k) > 0.42:
            return k
    return 0

# ---------------------------------------------------------------- drawing helpers
def holes(view, by):
    for c in range(1, COLS + 1):
        for r in range(1, ROWS + 1):
            add(f'<circle cx="{X(c, view):.1f}" cy="{Y(r, by):.1f}" r="4.2" fill="#d4a65a" stroke="#a87b33" stroke-width="0.8"/>'
                f'<circle cx="{X(c, view):.1f}" cy="{Y(r, by):.1f}" r="1.6" fill="#5b4a2a"/>')

def board(view, by):
    add(f'<rect x="{BX}" y="{by}" width="{COLS * P}" height="{ROWS * P}" rx="6" fill="#efe3c4" stroke="#8a7650" stroke-width="2"/>')
    holes(view, by)
    for c in range(1, COLS + 1):
        if c in (1, 5, 10, 15, 20, 24):
            text(X(c, view), by + ROWS * P + 15, str(c), 10, "middle", "#776")
    for r in range(1, ROWS + 1):
        if r in (1, 5, 10, 12, 15, 18):
            text(BX - 8, Y(r, by) + 4, str(r), 10, "end", "#776")
    text(BX - 8, by + ROWS * P + 15, "col", 9, "end", "#998", italic=True)
    text(BX - 26, Y(1, by) + 4, "row", 9, "end", "#998", italic=True)

def pin(c, r, view, by, fill="#c0c0c0"):
    add(f'<rect x="{X(c, view) - 5:.1f}" y="{Y(r, by) - 5:.1f}" width="10" height="10" rx="1.5" fill="{fill}" stroke="#555" stroke-width="1"/>')

def solder(c, r, view, by):
    add(f'<circle cx="{X(c, view):.1f}" cy="{Y(r, by):.1f}" r="5.6" fill="#d9d9d9" stroke="#666" stroke-width="1.2"/>')

def header_labels(pins, prefix, view, by):
    for n, (c, r) in pins.items():
        text(X(c, view) + 4, by - 6, n, 10.5, "start", "#222", "bold", rot=-90)
    cs = [X(c, view) for c, _ in pins.values()]
    xa, xb = min(cs), max(cs)
    add(f'<path d="M{xa - 6:.1f} {by - 40:.1f} H{xb + 6:.1f}" stroke="#555" stroke-width="1.2"/>')
    text((xa + xb) / 2, by - 45, prefix, 12, "middle", "#222", "bold")

def mcu_labels(view, by, dark):
    col = "#fff" if dark else "#222"
    for n, (c, r) in MCU.items():
        used = n in USED_MCU
        fill = col if used else ("#999" if dark else "#999")
        w = "bold" if used else "normal"
        if r == 12:
            text(X(c, view) + 3.5, Y(r, by) + 9, n, 9.5, "start", fill, w, rot=90, halo=not dark)
        else:
            text(X(c, view) + 3.5, Y(r, by) - 9, n, 9.5, "start", fill, w, rot=-90, halo=not dark)

# ================================================================= FRONT VIEW
add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} HEIGHT" font-family="Helvetica, Arial, sans-serif">')
add(f'<rect width="{W}" height="HEIGHT" fill="#ffffff"/>')
text(W / 2, 32, "Perfboard layout: ESP32-C3 SuperMini", 22, "middle", "#222", "bold")
text(W / 2, 54, "Top: the front, where the parts go.  Bottom: the back, where you solder. It is flipped left-to-right, like turning the board over.", 13, "middle", "#555")

FY = 140
text(BX, FY - 62, "1  FRONT  (parts side)", 16, "start", "#1d3557", "bold")
board("front", FY)
v = "front"
# TFT module
rect_cr(0.6, 12.4, 0.45, 15.1, v, FY, rx=6, fill="#1d3557", opacity="0.96")
rect_cr(1.6, 11.4, 2.3, 14.3, v, FY, rx=14, fill="#a8dadc")
text((X(0.6, v) + X(12.4, v)) / 2, Y(8, FY), '1.69" TFT', 15, "middle", "#1d3557", "bold")
text((X(0.6, v) + X(12.4, v)) / 2, Y(8, FY) + 18, "photo screen", 12, "middle", "#1d3557")
for c, r in TFT.values(): pin(c, r, v, FY)
header_labels(TFT, "TFT header (8 pins)", v, FY)
# OLED
rect_cr(13.1, 23.9, 0.45, 11.4, v, FY, rx=6, fill="#1d3557", opacity="0.96")
rect_cr(14.0, 23.0, 2.6, 4.1, v, FY, fill="#ffd60a")
rect_cr(14.0, 23.0, 4.1, 9.0, v, FY, fill="#4cc9f0")
text((X(13.1, v) + X(23.9, v)) / 2, Y(10.3, FY), '0.96" OLED', 12, "middle", "#fff", "bold")
for c, r in OLED.values(): pin(c, r, v, FY)
header_labels(OLED, "OLED header (4 pins)", v, FY)
# MCU
rect_cr(15.3, 24.0, 11.5, 18.55, v, FY, rx=4, fill="#2b2b2b")
rect_cr(23.3, 25.2, 13.6, 16.4, v, FY, rx=3, fill="#b8b8b8", stroke="#666")
text(X(25.0, v) + 8, Y(14.6, FY), "USB-C", 11, "start", "#222", "bold")
text(X(25.0, v) + 8, Y(15.4, FY) + 2, "(programming)", 10, "start", "#555")
add(f'<rect x="{X(18.3, v):.1f}" y="{Y(14.3, FY):.1f}" width="{2.4 * P:.1f}" height="{1.4 * P:.1f}" fill="#444" stroke="#777"/>')
text(X(19.5, v), Y(15.05, FY) + 3, "ESP32-C3", 9, "middle", "#ddd", "bold")
for n, (c, r) in MCU.items(): pin(c, r, v, FY, "#d9b84a")
mcu_labels(v, FY, True)
# Button
rect_cr(12.6, 15.4, 12.6, 15.4, v, FY, rx=3, fill="#3a3a3a")
add(f'<circle cx="{(X(12.6, v) + X(15.4, v)) / 2:.1f}" cy="{Y(14, FY):.1f}" r="{P * 0.8:.1f}" fill="#e63946"/>')
for i, (c, r) in enumerate(BTN): pin(c, r, v, FY)
text(X(14, v), Y(16.2, FY) + 2, "button", 10.5, "middle", "#222", "bold", halo=True)
# Switch
rect_cr(3.8, 8.2, 17.35, 18.85, v, FY, rx=2, fill="#8d99ae", stroke="#555")
rect_cr(5.4, 6.4, 18.6, 19.5, v, FY, rx=1, fill="#333")
for c, r in SW: pin(c, r, v, FY)
text(X(6, v), Y(16.6, FY), "on/off switch", 10.5, "middle", "#222", "bold", halo=True)
text(X(6, v), Y(20.2, FY) + 4, "lever sticks out of the bottom edge", 10, "middle", "#555")

# front-view notes on the right
NX = BX + COLS * P + 105
ny = FY + 4
def note_block(lines, y, x=NX):
    for i, (s, b) in enumerate(lines):
        text(x, y + i * 17, s, 12.5, "start", "#222" if b else "#444", "bold" if b else "normal")
    return y + len(lines) * 17
ny = note_block([
    ("What goes where", True),
    ("Both screens sit along the top edge,", False),
    ("with their header pins in row 1.", False),
    ("The SuperMini lies sideways in the", False),
    ("bottom right. Its USB-C hangs over", False),
    ("the right edge so you can plug it in.", False),
    ("The button goes in the gap between", False),
    ("the TFT and the SuperMini.", False),
    ("The switch goes on the bottom edge.", False),
    ("", False),
    ("Nothing else goes on the front.", True),
    ("The wires, the TP4056 charger and", False),
    ("the battery all go on the back.", False),
    ("", False),
    ("Check the sizes first", True),
    ("Drawn for a 30 × 37 mm TFT board,", False),
    ("a 27 × 27 mm OLED board and a", False),
    ("22.5 × 18 mm SuperMini. Sellers' boards", False),
    ("vary a little. Push everything into", False),
    ("the holes before soldering, then move", False),
    ("a part by one hole if it doesn't fit.", False),
], ny)

# ================================================================= BACK VIEW
BY = FY + ROWS * P + 150
v = "back"
text(BX, BY - 62, "2  BACK  (soldering side, board turned over)", 16, "start", "#7b2d26", "bold")
board(v, BY)
# ghost outlines of front parts
for (c1, c2, r1, r2, name) in [(0.6, 12.4, 0.45, 15.1, "TFT (on the other side)"),
                               (13.1, 23.9, 0.45, 11.4, "OLED (other side)"),
                               (15.3, 24.0, 11.5, 18.55, "")]:
    rect_cr(c1, c2, r1, r2, v, BY, rx=5, fill="none", stroke="#9aa", stroke_width="1.3", stroke_dasharray="5 4")
rect_cr(23.3, 25.2, 13.6, 16.4, v, BY, rx=3, fill="#e3e3e3", stroke="#888", stroke_dasharray="4 3")
text(X(25.0, v) - 8, Y(14.6, BY), "USB-C", 11, "end", "#444", "bold")
text(X(25.0, v) - 8, Y(15.4, BY) + 2, "(SuperMini)", 10, "end", "#666")

# solder joints
for (c, r) in ALL_PINS:
    solder(c, r, v, BY)
header_labels(TFT, "TFT pins", v, BY)
header_labels(OLED, "OLED pins", v, BY)
text(X(14, v), Y(16.3, BY) + 2, "button", 10, "middle", "#333", "bold", halo=True)
for lab, (c, r) in zip(["A", "B", "C", "D"], BTN):
    if lab in ("A", "D"):
        text(X(c, v) + (9 if lab == "A" else -9), Y(r, BY) - 7, lab, 10, "middle", "#000", "bold", halo=True)
text(X(6, v), Y(19.75, BY) + 4, "switch", 10, "middle", "#333", "bold")
text(X(7, v) - 4, Y(18.8, BY) + 3, "outer", 8.5, "end", "#333")
text(X(6, v) + 4, Y(18.8, BY) + 3, "middle", 8.5, "start", "#333")

# wires
def to_px(pt, view, by):
    return (X(pt[0], view), Y(pt[1], by))

badge_pos = []
wire_svgs = []
for (n, a, b, colr, label, group, k) in wires:
    if k is None:
        k = pick_bend(a, b)
    c = control(a, b, k)
    A, C, B = to_px(a, v, BY), to_px(c, v, BY), to_px(b, v, BY)
    d = f"M{A[0]:.1f} {A[1]:.1f} Q{C[0]:.1f} {C[1]:.1f} {B[0]:.1f} {B[1]:.1f}"
    wire_svgs.append(f'<path d="{d}" stroke="#ffffff" stroke-width="6" fill="none" stroke-linecap="round" opacity="0.9"/>'
                     f'<path d="{d}" stroke="{colr}" stroke-width="3.2" fill="none" stroke-linecap="round"/>')
    # badge: choose t that is far from other badges
    best = None
    for t in [0.5, 0.4, 0.6, 0.3, 0.7, 0.25, 0.75, 0.35, 0.65]:
        p = bez(a, c, b, t)
        dmin = min([math.dist(p, q) for q in badge_pos] + [9])
        dpin = min(math.dist(p, q) for q in ALL_PINS)
        score = min(dmin, 1.4) + min(dpin, 0.8)
        if best is None or score > best[0] + 1e-6:
            best = (score, t, p)
    _, t, p = best
    if n == 15:   # diode wire: put the diode symbol, not a badge, at 0.8 and badge at 0.35
        t, p = 0.62, bez(a, c, b, 0.62)
    badge_pos.append(p)
    wire_svgs.append(("badge", n, p, colr))
    if n == 15:
        q1, q2 = bez(a, c, b, 0.26), bez(a, c, b, 0.34)
        ang = math.degrees(math.atan2((Y(q2[1], BY) - Y(q1[1], BY)), (X(q2[0], v) - X(q1[0], v))))
        dp = to_px(bez(a, c, b, 0.3), v, BY)
        wire_svgs.append(("diode", dp, ang))

for w in wire_svgs:
    if isinstance(w, str):
        add(w)

mcu_labels(v, BY, False)

# TP4056 + battery (drawn over the wires, see-through)
rect_cr(TP[0], TP[1], TP[2], TP[3], v, BY, rx=4, fill="none", stroke="#1d3557", stroke_width="2.2", stroke_dasharray="7 4")
rect_cr(-1.1, 1.0, 11.6, 14.0, v, BY, rx=3, fill="#c8c8c8", stroke="#666")
text(X(-1.1, v) - 6, Y(12.6, BY), "USB-C", 11, "end", "#222", "bold")
text(X(-1.1, v) - 6, Y(13.4, BY) + 2, "(charging)", 10, "end", "#555")
text(X(4.6, v), Y(10.6, BY), "TP4056", 13, "middle", "#1d3557", "bold", halo=True)
text(X(4.6, v), Y(11.4, BY) + 2, "charger, foam-taped on", 9.5, "middle", "#1d3557", halo=True)
for name, (c, r) in TP_PADS.items():
    x, y = X(c, v), Y(r, BY)
    add(f'<rect x="{x - 6:.1f}" y="{y - 4:.1f}" width="12" height="8" rx="1" fill="#e0b050" stroke="#7a5a1a"/>')
    text(x - 10, y + 4, name.replace("-", "−"), 9.5, "end", "#1d3557", "bold", halo=True)
rect_cr(BAT[0], BAT[1], BAT[2], BAT[3], v, BY, rx=8, fill="none", stroke="#b8860b", stroke_width="2.2", stroke_dasharray="7 4")
bx_mid = (X(BAT[0], v) + X(BAT[1], v)) / 2
add(f'<rect x="{bx_mid - 150:.1f}" y="{Y(BAT[2], BY) - 10:.1f}" width="300" height="20" rx="4" fill="#fff3cf" stroke="#b8860b" stroke-width="1.5"/>')
text(bx_mid, Y(BAT[2], BY) + 4.5, "LiPo battery: goes on LAST, on top of kapton tape", 11, "middle", "#7a5a00", "bold")
for colr, (c, r) in [("#e63946", BAT_LEADS["red"]), ("#111", BAT_LEADS["black"])]:
    add(f'<circle cx="{X(c, v):.1f}" cy="{Y(r, BY):.1f}" r="4" fill="{colr}" stroke="#fff" stroke-width="1"/>')

# diode + badges on top
for w in wire_svgs:
    if isinstance(w, tuple) and w[0] == "diode":
        _, (dx, dy), ang = w
        ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        def pt(u, w_):
            return f"{dx + u * ca - w_ * sa:.1f},{dy + u * sa + w_ * ca:.1f}"
        add(f'<polygon points="{pt(-16,-7)} {pt(16,-7)} {pt(16,7)} {pt(-16,7)}" fill="#222" stroke="#fff" stroke-width="1.5" stroke-linejoin="round"/>')
        add(f'<polygon points="{pt(8,-7)} {pt(13,-7)} {pt(13,7)} {pt(8,7)}" fill="#e6e6e6"/>')
        text(dx, dy - 30, "1N5817 diode", 10.5, "middle", "#000", "bold", halo=True)
        text(dx, dy - 17, "stripe end towards 5V", 10, "middle", "#000", halo=True)
for w in wire_svgs:
    if isinstance(w, tuple) and w[0] == "badge":
        _, n, p, colr = w
        x, y = to_px(p, v, BY)
        add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="{colr}" stroke="#fff" stroke-width="1.8"/>')
        text(x, y + 4, str(n), 10.5, "middle", "#fff", "bold")

# ---------------------------------------------------------------- wire list
lx = NX
ly = BY - 40
text(lx, ly, "Wire list (tick them off)", 15, "start", "#222", "bold")
ly += 10
group = None
for (n, a, b, colr, label, g, k) in wires:
    if g != group:
        group = g
        ly += 22
        text(lx, ly, g, 12.5, "start", "#555", "bold")
        ly += 6
    ly += 19
    add(f'<rect x="{lx:.1f}" y="{ly - 11:.1f}" width="12" height="12" rx="2" fill="none" stroke="#777"/>')
    add(f'<circle cx="{lx + 28:.1f}" cy="{ly - 5:.1f}" r="8.5" fill="{colr}"/>')
    text(lx + 28, ly - 1, str(n), 10, "middle", "#fff", "bold")
    text(lx + 42, ly, label, 12, "start", "#222")
ly += 34
ly = note_block([
    ("Tips", True),
    ("Wires are drawn straight here. Real ones can", False),
    ("bend however you like: keep them flat.", False),
    ("A wire that only passes a pin isn't joined", False),
    ("to it. Joins are only at the wire ends.", False),
    ("Board GND takes wires 2 and 3. Button leg A", False),
    ("takes wires 3 and 17 (both GND).", False),
    ("Button: use the diagonal legs A and D.", False),
    ("Check every pin name against the printing", False),
    ("on your own boards before soldering.", False),
], ly)

H = max(ly, BY + ROWS * P + 40) + 30
foot = BY + ROWS * P + 62
text(BX, foot, "Seen from the back, the TFT is on the RIGHT and the SuperMini on the LEFT.", 12.5, "start", "#7b2d26", "bold")
text(BX, foot + 18, "Column numbers run 24 → 1. Full pin table: WIRING.md", 12, "start", "#555")
H = max(H, foot + 40)
add("</svg>")
svg = "\n".join(out).replace("HEIGHT", str(int(H)))
open(sys.argv[1], "w").write(svg)
print("height", H)
for (n, a, b, colr, label, g, k) in wires:
    kk = k if k is not None else pick_bend(a, b)
    print(n, label, "bend", kk, "clear", round(clearance(a, b, kk), 2))
