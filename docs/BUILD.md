# Build guide

## Perfboard layout

The board is a 5×7 cm perfboard (24 × 18 holes, 2.54 mm pitch) used in
landscape. The screens, XIAO, button and switch go on the **front**. The
wires run on the **back**, with the battery stuck flat on top of them
(insulated with tape).

### Front

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
 10  │ │               │   ┌───┐ ┌──────────────────┐   │
 11  │ │               │   │ ◉ │ │                  │   │
 12  │ │               │   └───┘ │  XIAO ESP32-C3   │══ USB-C (sticks out
 13  │ │               │  button │  lying sideways  │   │    of the right edge)
 14  │ │               │         │                  │   │
 15  │ └───────────────┘         └──────────────────┘   │
 16  │                    ┌──┐                          │
 17  │                    │▐ │ slide switch             │
 18  └────────────────────┴──┴──────────────────────────┘
                     lever pokes out of the bottom edge
```

### Back

```
 ┌────────────────────────────────────────────────┐
 │  wires (30 AWG) ...  covered with kapton tape  │
 │        ┌──────────────────────────┐            │
 │        │   LiPo 302030 (3×20×30)  │            │
 │        │   stuck on with foam tape│            │
 │        └──────────────────────────┘            │
 └────────────────────────────────────────────────┘
```

- **TFT:** 8-pin header along row 1, columns 2–9. Put a strip of foam tape
  under the bottom edge of the screen module so it doesn't wobble.
- **OLED:** 4-pin header in row 1, columns 15–18.
- **XIAO:** lying sideways in the bottom right with USB-C over the right
  edge.
- **Button:** between the TFT and the XIAO, where your thumb lands.
- **Slide switch:** on the bottom edge, with the lever pointing outwards.
- Module sizes vary a little between sellers. Lay everything out
  **before** soldering and adjust.

## Step by step

1. **Check the parts.** Before soldering, plug both screens and the button
   into a breadboard with jumper wires (same pins as
   [WIRING.md](WIRING.md)), flash the firmware and check that both screens
   light up and the button changes scenes. Do this on USB power only, **no
   battery yet**.
2. **Prepare the XIAO.** Solder about 6 cm of red wire to the **BAT+** pad
   and black wire to the **BAT−** pad on the **underside**, then solder on
   the male headers.
3. **Place the parts.** Push all the modules, the button and the switch
   through the perfboard. Feed the XIAO's battery wires through a spare hole
   to the back. Bend one leg of each part to hold it, and check that the
   outline still fits within 85 × 54 mm.
4. **Solder all the pins** from the back.
5. **Run the power rails.** Use two wires: **3V3** to TFT VCC and OLED VCC,
   and **GND** to TFT GND, OLED GND and one leg of the button.
6. **Run the signal wires** one at a time using the table in
   [WIRING.md](WIRING.md), ticking each one off as you go. Keep the wires
   flat. The battery is going on top of them.
7. **Check for shorts** with the multimeter's continuity mode:
   - 3V3 to GND: must **not** beep
   - BAT+ wire to BAT− wire: must **not** beep
   - each wire end to end: **must** beep
8. **Test on USB** (still no battery). Check that the photo and name show,
   and that the button works.
9. **Fit the battery.**
   1. Cover the back wiring with kapton or electrical tape.
   2. Solder the XIAO's **BAT+** wire to one **outer** switch pin.
   3. With the switch **off**, solder the LiPo's **red** wire to the
      switch's **middle** pin.
   4. Solder the LiPo's **black** wire to the XIAO's **BAT−** wire, and
      cover the joint with heat-shrink or tape.
   5. Stick the battery down with foam tape.
   Work on one battery wire at a time so the bare ends never touch.
10. **Finish.** Flip the switch on and it should boot from battery. Plug in
    USB-C to charge.

## Keeping it thin

- The battery is 3 mm, the board 1.6 mm, and the TFT on its header about
  6–8 mm, so the card is about 12–14 mm thick in total.
- To go thinner, solder the XIAO **flat** using its castellated edge pads
  (attach the battery wires to its underside first), and solder the screens'
  header pins with the plastic spacer slid off.
