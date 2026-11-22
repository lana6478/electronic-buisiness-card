# Build guide

## Perfboard layout

![perfboard layout, front and back](layout.svg)

The layout is drawn for a **33 × 19 hole** perfboard (numbers 1–33 along
the long edge, letters A–S across the short edge, with a strip of long pads
beyond row A), about the size of a credit card. Hold it with **row S at the
top** and the long pads at the bottom. Both screens are then the right way
up. The screens, SuperMini and button go on the **front**. The wires run on
the **back**, with the battery and the TP4056 charger stuck flat on top of
them (insulated with tape).

The diagram shows both sides. The **back view is mirrored**, as if you'd
turned the board over, so it matches what you see while soldering. Every
wire is numbered, and the wire list gives the holes at both ends: tick them
off as you go.

Hole names are letter + number, as printed on the board:

- **TFT:** 8-pin header in **S4–S11** (GND at S4, BLK at S11). The screen
  covers the left part of the board. Put a strip of foam tape under the
  far edge of the module so it doesn't wobble.
- **SuperMini:** between the screens, with its USB-C over the top edge for
  programming. Its pins are in **columns 16 and 22, rows R to K**: 5V at R16
  and GPIO5 at R22.
- **OLED:** 4-pin header in **S27–S30** (GND, VDD, SCK, SDA).
- **Button:** below the SuperMini, legs in F18, F20, C18 and C20.
- **Slide switch:** on the right edge in E33, D33 and C33, lever sticking
  out sideways.
- **TP4056 (back):** behind the button area, with its USB-C over the
  bottom edge, so the two USB-C ports are easy to tell apart (charging vs
  programming).
- **LiPo (back):** behind the TFT, fitted last, on kapton tape.
- **Check the pin printing on your own boards** before soldering. If your
  TFT's pins run the other way (BLK at S4), or your SuperMini has 5V
  somewhere else, wire by the names, not the hole positions.

## Step by step

1. **Check the parts.** Before soldering, plug both screens and the button
   into a breadboard with jumper wires (same pins as
   [WIRING.md](WIRING.md)), flash the firmware and check that both screens
   light up and the button changes scenes. Do this on USB power only, **no
   battery yet**.
2. **Solder headers** onto the SuperMini (short male headers). Keep them
   straight by pushing them into the perfboard while you solder.
3. **Place the parts.** Push the screens, the SuperMini, the button and
   the switch through the perfboard. Bend one leg of each part to hold it, and check that the
   outline still fits within 85 × 54 mm.
4. **Solder all the pins** from the back.
5. **Run the power rails.** Use two wires: **3V3** to TFT VCC and OLED VCC,
   and **GND** to TFT GND, OLED GND and one leg of the button.
6. **Run the signal wires** one at a time using the table in
   [WIRING.md](WIRING.md), ticking each one off as you go. Keep the wires
   flat. The battery is going on top of them.
7. **Check for shorts** with the multimeter's continuity mode:
   - 3V3 to GND: must **not** beep
   - 5V to GND: must **not** beep
   - each wire end to end: **must** beep
8. **Test on USB** (still no battery). Check that the photo and name show,
   and that the button works.
9. **Fit the charger and battery.** See [WIRING.md](WIRING.md#battery-supermini--tp4056).
   1. Cover the back wiring with kapton or electrical tape.
   2. Solder the **1N5817 diode** (a 1N5818 or 1N5819 works too) from the switch's **outer** pin to the
      SuperMini's **5V** pin. The **stripe end goes towards 5V**.
   3. Wire TP4056 **OUT+** to the switch's **middle** pin, and **OUT−** to
      **GND**.
   4. Stick the TP4056 to the back with foam tape, with its USB-C over the
      edge.
   5. **Last:** solder the LiPo's **red** wire to **B+**, then its **black**
      wire to **B−**. Do one wire at a time so the bare ends never touch.
   6. Stick the battery down with foam tape.
10. **Finish.** Flip the switch on and it should boot from battery. Plug
    USB-C into the **TP4056** to charge (red LED = charging, blue/green =
    full).

## Keeping it thin

- The battery is 3 mm, the board 1.6 mm, and the TFT on its header about
  6–8 mm, so the card is about 12–14 mm thick in total.
- To go thinner, solder the SuperMini **flat** using its castellated edge
  pads, and solder the screens' header pins with the plastic spacer slid
  off.
