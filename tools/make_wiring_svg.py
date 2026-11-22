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
    a(f'<path d="{d}" stroke="{c}" stroke-width="{wd}" fill="none" stroke-linejoin="round"/>')
def dot(x, y, c="#111"):
    a(f'<circle cx="{x}" cy="{y}" r="4.5" fill="{c}"/>')
def gnd(x, y):
    a(f'<path d="M{x} {y} v10 M{x-10} {y+10} h20 M{x-6} {y+15} h12 M{x-2} {y+20} h4" stroke="#111" stroke-width="2.5" fill="none"/>')

W, H = 1000, 760
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
L = ["5V", "GND", "3V3", "GPIO4", "GPIO3", "GPIO2", "GPIO1", "GPIO0"]
R = ["GPIO5", "GPIO6", "GPIO7", "GPIO8", "GPIO9", "GPIO10", "GPIO20", "GPIO21"]
used = {"5V", "GND", "3V3", "GPIO4", "GPIO3", "GPIO1", "GPIO5", "GPIO6", "GPIO7", "GPIO8", "GPIO9", "GPIO10"}
py = {}
for i, n in enumerate(L):
    y = 180 + i * 34; py[n] = (430, y)
    t(438, y + 4, n, 11, "start", "#fff" if n in used else "#777", "bold" if n in used else "normal")
for i, n in enumerate(R):
    y = 180 + i * 34; py[n] = (590, y)
    t(582, y + 4, n, 11, "end", "#fff" if n in used else "#777", "bold" if n in used else "normal")
t(510, 438, "col 16 ← → col 22", 9.5, "middle", "#aaa")
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
wire(f"M430 {py['GND'][1]} H392 V100", GND); dot(392, 100)
wire(f"M430 {py['3V3'][1]} H378 V118", V3); dot(378, 118)
wire("M770 190 H738 V100", GND); dot(738, 100)
wire("M770 225 H724 V118", V3); dot(724, 118)

# TFT signals
def lab(x, y, s, c):
    t(x, y, s, 10.5, "start", c, "bold")
wire(f"M230 260 H330 V{py['GPIO4'][1]} H430", "#2a9d8f")
wire(f"M230 330 H315 V{py['GPIO1'][1]} H430", "#8338ec")
wire(f"M230 435 H345 V{py['GPIO3'][1]} H430", "#c9a227")
wire(f"M230 295 H285 V560 H690 V{py['GPIO6'][1]} H590", "#3a86ff")
wire(f"M230 400 H295 V545 H675 V{py['GPIO7'][1]} H590", "#6c757d")
wire(f"M230 365 H305 V530 H660 V{py['GPIO10'][1]} H590", "#ff006e")
# OLED signals
wire(f"M770 260 H640 V{py['GPIO9'][1]} H590", "#06a77d")
wire(f"M770 295 H625 V{py['GPIO8'][1]} H590", "#118ab2")

# button
a('<rect x="480" y="610" width="60" height="60" rx="6" fill="#444"/><circle cx="510" cy="640" r="17" fill="#e63946"/>')
t(510, 690, "button (F18 F20 C18 C20)", 11.5, "middle", "#222", "bold")
t(510, 705, "tap = next, hold = sleep", 10.5, "middle", "#555")
wire(f"M590 {py['GPIO5'][1]} H754 V640 H540", "#8d5524")
t(758, 420, "GPIO5", 10.5, "start", "#8d5524", "bold")
wire("M480 640 H455 V660", GND); gnd(455, 660)

# battery chain, bottom left
a('<rect x="40" y="610" width="90" height="56" rx="8" fill="#ffd166" stroke="#222"/>')
t(85, 634, "LiPo", 13, "middle", "#222", "bold"); t(85, 650, "3.7 V 250 mAh", 9.5, "middle", "#222")
a('<rect x="160" y="600" width="110" height="80" rx="6" fill="#1d3557"/>')
t(215, 637, "TP4056", 13, "middle", "#fff", "bold"); t(215, 652, "USB-C charger", 10, "middle", "#ccd")
t(166, 618, "B+", 10, "start", "#fff", "bold"); t(166, 675, "B−", 10, "start", "#fff", "bold")
t(264, 618, "OUT+", 10, "end", "#fff", "bold"); t(264, 675, "OUT−", 10, "end", "#fff", "bold")
wire("M130 620 H160", V3); wire("M130 656 H160", GND)
wire("M270 670 H290 V690", GND); gnd(290, 690)
# switch
wire("M270 614 H300", V5)
a('<rect x="300" y="604" width="40" height="20" rx="3" fill="#8d99ae" stroke="#555"/><rect x="306" y="597" width="10" height="9" fill="#333"/>')
t(320, 642, "switch", 11, "middle", "#222", "bold"); t(320, 656, "E33 D33 C33", 9.5, "middle", "#555")
# diode
wire("M340 614 H352", V5)
a('<polygon points="352,603 352,625 372,614" fill="#222"/><rect x="372" y="603" width="4" height="22" fill="#222"/>')
t(364, 642, "1N5817", 10.5, "middle", "#222", "bold"); t(364, 670, "stripe → 5V", 9.5, "middle", "#555")
wire(f"M376 614 H405 V{py['5V'][1]} H430", V5)
t(410, 595, "5V", 11, "start", V5, "bold")

t(40, 735, "Use the button's two diagonal legs. The ground symbol means connect to GND (the layout uses button leg C, which joins board GND Q16).", 12, "start", "#444")
t(40, 752, "Where each wire goes on the board: layout.svg.  Full pin table: WIRING.md.", 12, "start", "#444")
a("</svg>")
open(sys.argv[1], "w").write("\n".join(o))
