# Wiring

![wiring diagram](wiring.svg)

Every connection, for both supported boards. **GPIO numbers are what the
firmware uses** (see `firmware/business_card/config.h`).

## Colour TFT (1.69" ST7789, SPI)

| TFT pin | Function | ESP32-C3 SuperMini | XIAO ESP32-C3 |
|---|---|---|---|
| GND | Ground | GND | GND |
| VCC | Power | 3V3 | 3V3 |
| SCL | SPI clock (SCK) | GPIO4 | D8 (GPIO8) |
| SDA | SPI data (MOSI) | GPIO6 | D10 (GPIO10) |
| RES | Reset | GPIO1 | D0 (GPIO2) |
| DC | Data/command | GPIO10 | D1 (GPIO3) |
| CS | Chip select | GPIO7 | D2 (GPIO4) |
| BLK | Backlight (PWM) | GPIO3 | D3 (GPIO5) |

> The labels "SCL/SDA" on the TFT are misleading: this screen uses **SPI**,
> not I2C. SCL = clock and SDA = data in.

## Info OLED (0.96" SSD1306, I2C)

| OLED pin | ESP32-C3 SuperMini | XIAO ESP32-C3 |
|---|---|---|
| GND | GND | GND |
| VCC | 3V3 | 3V3 |
| SCL | GPIO9 | D5 (GPIO7) |
| SDA | GPIO8 | D4 (GPIO6) |

> **Check your OLED's pin order.** Some boards are `VCC GND SCL SDA`. Swapping
> VCC and GND can kill the screen.

## Board pinouts (top view, USB-C at the top)

```
   ESP32-C3 SuperMini                  Seeed XIAO ESP32-C3
      ┌──[USB-C]──┐                      ┌──[USB-C]──┐
  5V  ●           ● GPIO5            D0  ●           ● 5V
  GND ●           ● GPIO6  TFT SDA   D1  ●           ● GND
  3V3 ●           ● GPIO7  TFT CS    D2  ●           ● 3V3
TFT SCL GPIO4 ●   ● GPIO8  OLED SDA  D3  ●           ● D10  TFT SDA
TFT BLK GPIO3 ●   ● GPIO9  OLED SCL  D4  ●           ● D9   (spare)
      GPIO2 ●     ● GPIO10 TFT DC    D5  ●           ● D8   TFT SCL
TFT RES GPIO1 ●   ● GPIO20           D6  ●           ● D7   (spare)
      GPIO0 ●     ● GPIO21               └───────────┘
      └───────────┘                  D0 RES, D1 DC, D2 CS, D3 BLK,
                                     D4 OLED SDA, D5 OLED SCL
```

**Board revisions differ, so always check the silkscreen on your board**
before soldering. If the pins differ, change the numbers in `config.h`.

## Power

- Both screens are powered from **3V3**. They draw about 30–60 mA together,
  well within the regulator's limit.
- All grounds are joined.
- Power comes from USB-C (phone charger, laptop or power bank). For a battery
  see the README.

## Notes on pin choices

- The TFT and the OLED are on **separate buses** (SPI vs I2C), so they can't
  conflict.
- On the ESP32-C3, GPIO2, 8 and 9 are boot-strapping pins. They're used here
  only for signals that sit high at power-up (I2C pull-ups, reset), so the
  board boots normally.
- The SuperMini's blue LED shares GPIO8 with OLED SDA, so it flickers faintly.
  That's normal.
