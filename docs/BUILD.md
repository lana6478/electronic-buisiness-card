# Build guide

## Perfboard layout (front view)

The board is a 5×7 cm perfboard (24 × 18 holes, 2.54 mm pitch) used in
landscape. Everything goes on the **front** and all wires run on the
**back**.

```
 col: 1         5        10        15        20      24
 row ┌────────────────────────────────────────────────┐
  1  │ ○ ● ● ● ● ● ● ● ●  ○ ○ ○ ○  ● ● ● ●  ○ ○ ○ ○ ○ ○ │  ● = header pins
  2  │ ┌───────────────┐          ┌──────────────┐      │
  3  │ │               │          │              │      │
  4  │ │               │          │  0.96" OLED  │      │
  5  │ │               │          │  (27×27 mm)  │      │
  6  │ │   1.69" TFT   │          │              │      │
  7  │ │  (≈31×38 mm)  │          │              │      │
  8  │ │               │          └──────────────┘      │
  9  │ │               │                                │
 10  │ │               │    ┌────────────────────┐      │
 11  │ │               │    │                    │      │
 12  │ │               │    │  ESP32-C3 board,   │══ USB-C (points off
 13  │ │               │    │  lying sideways    │      the right edge)
 14  │ │               │    │                    │      │
 15  │ └───────────────┘    └────────────────────┘      │
 16  │                                                  │
 17  │  (wire on the back between rows)                 │
 18  └────────────────────────────────────────────────┘
```

- **TFT:** 8-pin header along row 1, columns 2–9. The screen sits above the
  board on its own header; put a strip of double-sided foam tape under its
  bottom edge so it doesn't wobble.
- **OLED:** 4-pin header in row 1, columns 15–18.
- **ESP32-C3:** lying sideways in the bottom right with USB-C sticking out
  past the right edge, so a cable plugs in easily.
- Module sizes vary a little between sellers. Lay everything out
  **before** soldering and adjust.

## Step by step

1. **Check the parts.** Before soldering, plug both screens into a
   breadboard with jumper wires (same pins as [WIRING.md](WIRING.md)), flash
   the firmware and check that both light up. Dead screens are much easier
   to spot now than after soldering.
2. **Solder headers to the ESP32 board.** Use the short male headers. Keep
   them straight by pushing them into the perfboard while you solder.
3. **Place the parts.** Push all three modules through the perfboard in
   their positions. Bend one leg of each on the back to hold it, and check
   that the outline still fits within 85 × 54 mm.
4. **Solder the module pins** to the perfboard from the back.
5. **Run the power rails first.** Use two wires: **3V3** to TFT VCC and
   OLED VCC, and **GND** to TFT GND and OLED GND.
6. **Run the signal wires** one at a time using the table in
   [WIRING.md](WIRING.md), and tick each one off as you go. Strip about 2 mm,
   tin it, then lay it on the pin and reflow. Keep the wires flat against the
   board.
7. **Check for shorts.** Before plugging in, use the multimeter's continuity
   mode to check:
   - 3V3 to GND: must **not** beep
   - each signal pin to its neighbour: must **not** beep
   - each wire end to end: **must** beep
8. **Power up** over USB-C. You should see the placeholder (your initials)
   or your photo on the TFT, and your name on the OLED.
9. **Finish.** Trim the leads flush on the back. Optionally cover the back
   with a piece of clear tape or kapton, or a thin 3D-printed or laser-cut
   back plate, so it doesn't scratch things in your wallet or pocket.

## Keeping it thin

- Solder the ESP32 board **flat** without headers (castellated pads plus
  short wire bits) to save about 8 mm. The SuperMini and XIAO both allow
  this.
- Use 30 AWG wire-wrap wire on the back.
- The TFT is the tallest part. You can mount it with low-profile female
  headers, or solder its pins directly.
