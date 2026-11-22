"""Draw docs/wiring.svg: the wiring diagram, with the parts placed as on the
board (TFT left, SuperMini middle, OLED right).

    python3 tools/make_wiring_svg.py docs/wiring.svg
"""
import sys
o = []
a = o.append
def t(x, y, s, size=12, anchor="start", fill="#222", w="normal"):
    a(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{fill}" font-weight="{w}">{s}</text>')
def wire(d, c, wd=3):
    a(f'<path d="{d}" stroke="#ffffff" stroke-width="{wd + 4}" fill="none" stroke-linejoin="round"/>')
    a(f'<path d="{d}" stroke="{c}" stroke-width="{wd}" fill="none" stroke-linejoin="round"/>')
def dot(x, y, c="#111"):
    a(f'<circle cx="{x}" cy="{y}" r="4.5" fill="{c}"/>')
def gnd(x, y):
    a(f'<path d="M{x} {y} v10 M{x-10} {y+10} h20 M{x-6} {y+15} h12 M{x-2} {y+20} h4" stroke="#111" stroke-width="2.5" fill="none"/>')

W, H = 1000, 800
a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Helvetica, Arial, sans-serif">')
a(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
t(W/2, 32, "Wiring: ESP32-C3 SuperMini (parts placed as on the board)", 20, "middle", "#222", "bold")
t(W/2, 52, "Lines only join where there is a dot. Lines that just cross are not connected.", 12.5, "middle", "#555")

GND, V3, V5 = "#111", "#e63946", "#f77f00"
# rails
wire("M262 100 H738", GND, 3.5); t(500, 94, "GND", 12, "middle", GND, "bold")
wire("M276 118 H724", V3, 3.5); t(560, 136, "3V3", 12, "middle", V3, "bold")

# TFT
a('<rect x="40" y="160" width="190" height="320" rx="10" fill="#1d3557"/>')
a('<rect x="58" y="300" width="110" height="150" rx="12" fill="#a8dadc"/>')
t(113, 370, '1.69" TFT', 13, "middle", "#1d3557", "bold"); t(113, 388, "ST7789", 11, "middle", "#1d3557")
t(60, 182, "pins S4 – S11", 11, "start", "#cde")
tft = [("GND", 190), ("VCC", 225), ("SCL", 260), ("SDA", 295), ("RES", 330), ("DC", 365), ("CS", 400), ("BLK", 435)]
for n, y in tft:
    t(222, y + 4, n, 12, "end", "#fff", "bold")
# MCU
a('<rect x="430" y="150" width="160" height="295" rx="8" fill="#2a2a2a"/>')
a('<rect x="485" y="126" width="50" height="28" rx="5" fill="#aaa"/>'); t(510, 145, "USB-C", 10, "middle", "#222", "bold")
t(510, 300, "ESP32-C3", 13, "middle", "#fff", "bold"); t(510, 317, "SuperMini", 11, "middle", "#ccc")
L = ["GPIO5", "GPIO6", "GPIO7", "GPIO8", "GPIO9", "GPIO10", "GPIO20", "GPIO21"]   # column 16
R = ["5V", "GND", "3V3", "GPIO4", "GPIO3", "GPIO2", "GPIO1", "GPIO0"]           # column 22
used = {"5V", "GND", "3V3", "GPIO4", "GPIO3", "GPIO1", "GPIO5", "GPIO6", "GPIO7", "GPIO8", "GPIO9", "GPIO10"}
py = {}
for i, n in enumerate(L):
    y = 180 + i * 34; py[n] = (430, y)
    t(438, y + 4, n, 11, "start", "#fff" if n in used else "#777", "bold" if n in used else "normal")
for i, n in enumerate(R):
    y = 180 + i * 34; py[n] = (590, y)
    t(582, y + 4, n, 11, "end", "#fff" if n in used else "#777", "bold" if n in used else "normal")
t(510, 438, "col 16       col 22", 9.5, "middle", "#aaa")
# OLED
a('<rect x="770" y="160" width="190" height="170" rx="10" fill="#1d3557"/>')
a('<rect x="840" y="200" width="105" height="18" fill="#ffd60a"/><rect x="840" y="218" width="105" height="70" fill="#4cc9f0"/>')
t(892, 310, '0.96" OLED', 12, "middle", "#fff", "bold")
t(940, 182, "pins S27 – S30", 10.5, "end", "#cde")
oled = [("GND", 190), ("VDD", 225), ("SCK", 260), ("SDA", 295)]
for n, y in oled:
    t(778, y + 4, n, 12, "start", "#fff", "bold")

# power to rails
wire("M230 190 H262 V100", GND); dot(262, 100)
wire("M230 225 H276 V118", V3); dot(276, 118)
wire(f"M590 {py['GND'][1]} H704 V100", GND); dot(704, 100)
wire(f"M590 {py['3V3'][1]} H690 V118", V3); dot(690, 118)
wire("M770 190 H738 V100", GND); dot(738, 100)
wire("M770 225 H724 V118", V3); dot(724, 118)

# TFT -> left column (GPIO6, GPIO7, GPIO10)
wire(f"M230 295 H330 V{py['GPIO6'][1]} H430", "#3a86ff")
wire(f"M230 400 H345 V{py['GPIO7'][1]} H430", "#6c757d")
wire(f"M230 365 H360 V{py['GPIO10'][1]} H430", "#ff006e")
# TFT -> right column (GPIO4, GPIO3, GPIO1), under the SuperMini
wire(f"M230 260 H285 V560 H634 V{py['GPIO4'][1]} H590", "#2a9d8f")
wire(f"M230 435 H297 V545 H620 V{py['GPIO3'][1]} H590", "#c9a227")
wire(f"M230 330 H309 V530 H606 V{py['GPIO1'][1]} H590", "#8338ec")
# OLED -> left column (GPIO8, GPIO9), under everything
wire(f"M770 295 H750 V590 H390 V{py['GPIO8'][1]} H430", "#118ab2")
wire(f"M770 260 H760 V605 H380 V{py['GPIO9'][1]} H430", "#06a77d")

# button (brown tags = joined to each other)
def tag(x, y, s, anchor):
    w = 7 * len(s) + 12
    x0 = x - w if anchor == "end" else x
    a(f'<rect x="{x0}" y="{y - 10}" width="{w}" height="20" rx="10" fill="#8d5524"/>')
    t(x0 + w / 2, y + 4, s, 10.5, "middle", "#fff", "bold")
wire(f"M430 {py['GPIO5'][1]} H404", "#8d5524"); tag(404, py['GPIO5'][1], "to button", "end")
a('<rect x="470" y="640" width="60" height="60" rx="6" fill="#444"/><circle cx="500" cy="670" r="17" fill="#e63946"/>')
t(500, 718, "button (F18 F20 C18 C20)", 11.5, "middle", "#222", "bold")
t(500, 733, "tap = next, hold = sleep", 10.5, "middle", "#555")
wire("M470 670 H446", "#8d5524"); tag(446, 670, "to GPIO5", "end")
t(462, 660, "F18", 9.5, "end", "#555")
wire("M530 670 H552 V688", GND); gnd(552, 688); t(538, 660, "C20", 9.5, "start", "#555")

# battery chain, bottom right: LiPo -> TP4056 -> switch -> diode -> 5V
wire(f"M590 {py['5V'][1]} H660 V644 H664", V5)
t(666, 400, "5V", 11, "start", V5, "bold")
a('<polygon points="684,633 684,655 666,644" fill="#222"/><rect x="662" y="633" width="4" height="22" fill="#222"/>')
t(674, 672, "1N5817", 10.5, "middle", "#222", "bold"); t(674, 686, "stripe → 5V", 9.5, "middle", "#555")
wire("M684 644 H700", V5)
a('<rect x="700" y="634" width="40" height="20" rx="3" fill="#8d99ae" stroke="#555"/><rect x="724" y="627" width="10" height="9" fill="#333"/>')
t(728, 686, "switch", 11, "middle", "#222", "bold"); t(742, 700, "E33 D33 C33", 9.5, "middle", "#555")
wire("M740 644 H770", V5)
a('<rect x="770" y="626" width="110" height="80" rx="6" fill="#1d3557"/>')
t(825, 662, "TP4056", 13, "middle", "#fff", "bold"); t(825, 677, "USB-C charger", 10, "middle", "#ccd")
t(776, 644, "OUT+", 10, "start", "#fff", "bold"); t(776, 700, "OUT−", 10, "start", "#fff", "bold")
t(874, 644, "B+", 10, "end", "#fff", "bold"); t(874, 700, "B−", 10, "end", "#fff", "bold")
wire("M770 696 H756 V712", GND); gnd(756, 712)
a('<rect x="900" y="634" width="70" height="62" rx="8" fill="#ffd166" stroke="#222"/>')
t(935, 662, "LiPo", 13, "middle", "#222", "bold"); t(935, 678, "250 mAh", 9.5, "middle", "#222")
wire("M880 640 H900", V3); wire("M880 690 H900", GND)

t(40, 765, "The ground symbol means connect to GND (the layout uses button leg D, C20, which joins board GND Q22). Brown tags are joined.", 12, "start", "#444")
t(40, 782, "Where each wire goes on the board: layout.svg.  Full pin table: WIRING.md.", 12, "start", "#444")
a("</svg>")
open(sys.argv[1], "w").write("\n".join(o))
