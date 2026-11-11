# Wiring

![wiring diagram](wiring.svg)

Every connection, for both supported boards. **GPIO numbers are what the
firmware uses** (see `firmware/business_card/config.h`).

## Colour TFT (1.69" ST7789, SPI)

| TFT pin | Function | XIAO ESP32-C3 | ESP32-C3 SuperMini |
|---|---|---|---|
| GND | Ground | GND | GND |
| VCC | Power | 3V3 | 3V3 |
| SCL | SPI clock (SCK) | D8 (GPIO8) | GPIO4 |
| SDA | SPI data (MOSI) | D10 (GPIO10) | GPIO6 |
| RES | Reset | D0 (GPIO2) | GPIO1 |
| DC | Data/command | D1 (GPIO3) | GPIO10 |
| CS | Chip select | D2 (GPIO4) | GPIO7 |
| BLK | Backlight (PWM) | D3 (GPIO5) | GPIO3 |

> The labels "SCL/SDA" on the TFT are misleading: this screen uses **SPI**,
> not I2C. SCL = clock and SDA = data in.

## Info OLED (0.96" SSD1306, I2C)

| OLED pin | XIAO ESP32-C3 | ESP32-C3 SuperMini |
|---|---|---|
| GND | GND | GND |
| VCC | 3V3 | 3V3 |
| SCL | D5 (GPIO7) | GPIO9 |
| SDA | D4 (GPIO6) | GPIO8 |

> **Check your OLED's pin order.** Some boards are `VCC GND SCL SDA`. Swapping
> VCC and GND can kill the screen.

## Button

| Button leg | XIAO ESP32-C3 | ESP32-C3 SuperMini |
|---|---|---|
| one side | D7 (GPIO20) | GPIO5 |
| other side | GND | GND |

No resistor is needed, because the chip's internal pull-up is used. A
6×6 mm tactile button has 4 legs, which are **connected in pairs** along
the long side. Wire across the button **diagonally** (opposite corners)
and it will always be right.

- **Tap:** next scene (changes both screens)
- **Hold 1 s:** screens off and low-power sleep. **Tap** to wake.

## Battery (XIAO only)

```
 LiPo red (+) ──── switch middle pin
                   switch outer pin ──── XIAO BAT+ pad (underside)
 LiPo black (−) ──────────────────────── XIAO BAT− pad (underside)
```

- The **BAT+ / BAT− pads are on the underside** of the XIAO. Solder thin
  wires to them **before** soldering the XIAO onto the perfboard, then pass
  the wires through a spare hole to the back.
- **Polarity matters.** Red goes to +. Getting it wrong can destroy the
  XIAO. Many cheap LiPos have the JST wires the "wrong" way round, so trust
  the wire colours and a multimeter, not the plug.
- Never let the bare battery wires touch. Cut and solder them **one at a
  time**.
- Charging: plug in USB-C with the switch **on**. The XIAO's LED lights
  while charging.

## Board pinouts (top view, USB-C at the top)

```
          Seeed XIAO ESP32-C3
             ┌──[USB-C]──┐
  TFT RES  D0 ●           ● 5V
  TFT DC   D1 ●           ● GND      ← all grounds
  TFT CS   D2 ●           ● 3V3      ← both screens' VCC
  TFT BLK  D3 ●           ● D10  TFT SDA
  OLED SDA D4 ●           ● D9   (spare)
  OLED SCL D5 ●           ● D8   TFT SCL
  (spare)  D6 ●           ● D7   BUTTON
             └───────────┘
        [BAT+] [BAT−] pads on the underside


          ESP32-C3 SuperMini
             ┌──[USB-C]──┐
           5V ●           ● GPIO5   BUTTON
          GND ●           ● GPIO6   TFT SDA
          3V3 ●           ● GPIO7   TFT CS
  TFT SCL GPIO4 ●         ● GPIO8   OLED SDA
  TFT BLK GPIO3 ●         ● GPIO9   OLED SCL
  (spare) GPIO2 ●         ● GPIO10  TFT DC
  TFT RES GPIO1 ●         ● GPIO20  (spare)
  (spare) GPIO0 ●         ● GPIO21  (spare)
             └───────────┘
```

XIAO summary: D0 RES · D1 DC · D2 CS · D3 BLK · D4 OLED SDA · D5 OLED SCL ·
D7 button · D8 TFT SCL · D10 TFT SDA.

**Board revisions differ, so always check the silkscreen on your board**
before soldering. If the pins differ, change the numbers in `config.h`.

## Power

- Both screens are powered from **3V3**. They draw about 30–60 mA together.
- All grounds are joined.
- XIAO: runs from the battery or USB-C, and USB-C charges the battery.
- SuperMini: USB-C only.

## Notes on pin choices

- The TFT and the OLED are on **separate buses** (SPI vs I2C), so they can't
  conflict.
- On the ESP32-C3, GPIO2, 8 and 9 are boot-strapping pins. They're used here
  only for signals that sit high at power-up, so the board boots normally.
- The button is on a pin that is **not** a strapping pin, so holding it while
  plugging in won't put the board into bootloader mode.
