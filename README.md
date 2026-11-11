# Electronic Business Card (dual screen, credit-card size)

A cheap DIY electronic business card built on perfboard: a **colour screen
showing your photo** next to a **small OLED with your name, email and a
QR code**, driven by an ESP32-C3. It runs from USB-C and fits inside a
credit card's footprint (85.6 × 54 mm).

```
            70 mm (5×7 cm perfboard)
 ┌──────────────────────────────────────────────┐
 │ GND VCC SCL SDA RES DC CS BLK   GND VCC SCL SDA│
 │ ┌──────────────┐        ┌──────────────────┐ │
 │ │              │        │ you@email.com    │ │  50 mm
 │ │   1.69" TFT  │        │   Your Name      │ │
 │ │  your photo  │        │   engineer :3    │ │
 │ │              │        └──────────────────┘ │
 │ │              │        ┌──────────┐         │
 │ │              │        │ ESP32-C3 │▐ USB-C  │
 │ └──────────────┘        └──────────┘         │
 └──────────────────────────────────────────────┘
```

| | |
|---|---|
| **Cost** | about **£7–9** for the budget build ([BOM](docs/BOM.md)) |
| **Size** | 70 × 50 mm, about 12 mm thick (credit card = 85.6 × 54 mm) |
| **Skill** | beginner soldering, about 2–3 hours |
| **Software** | Arduino IDE, plus a small Python script for your photo |

## Contents

1. [Parts list and prices](docs/BOM.md)
2. [Wiring](docs/WIRING.md) ([diagram](docs/wiring.svg))
3. [Perfboard layout and build steps](docs/BUILD.md)
4. [Firmware: install, customise and flash](#firmware)
5. [Troubleshooting](docs/TROUBLESHOOTING.md)

![wiring](docs/wiring.svg)

## Parts (short version)

| Part | Budget pick | Approx. price |
|---|---|---|
| Microcontroller | ESP32-C3 SuperMini (or Seeed XIAO ESP32-C3) | £2 (XIAO £5–6) |
| Colour screen | 1.69" ST7789 240×280 SPI IPS, 8-pin | £3 |
| Info screen | 0.96" SSD1306 128×64 I2C OLED, 4-pin (yellow/blue) | £1.50 |
| Board | 5×7 cm double-sided perfboard | £0.30 |
| Wire + headers | 30 AWG wire-wrap or thin solid-core wire, pin headers | £0.50 |

Full details, links and search terms: **[docs/BOM.md](docs/BOM.md)**.

## Firmware

### 1. Set up the Arduino IDE

1. Install the [Arduino IDE 2](https://www.arduino.cc/en/software).
2. Open **File → Preferences → Additional boards manager URLs** and add
   `https://espressif.github.io/arduino-esp32/package_esp32_index.json`
3. Open **Tools → Board → Boards Manager**, search **esp32** and install
   *esp32 by Espressif Systems*.
4. Open **Tools → Manage Libraries** and install:
   - `Adafruit ST7735 and ST7789 Library`
   - `Adafruit SSD1306`
   - `Adafruit GFX Library` (it usually installs automatically with the two above)

### 2. Add your details

Open `firmware/business_card/business_card.ino`. Then, in the
`config.h` tab:

- pick your board (`BOARD_ESP32C3_SUPERMINI` or `BOARD_XIAO_ESP32C3`)
- fill in your name, title, email and website

### 3. Add your photo and QR code (optional, but that's the fun part)

```bash
pip install -r tools/requirements.txt
python3 tools/make_assets.py --photo me.jpg --qr https://github.com/yourname
```

This creates `photo.h` and `qr.h` inside `firmware/business_card/`. The
photo is cropped and resized for you. Give `--photo` several files for a
slideshow. Without these files the card shows a gradient with your
initials instead.

> `photo.h` and `qr.h` are listed in `.gitignore`, so your photo doesn't end
> up in a public repo by accident.

### 4. Flash it

1. Plug the board in with a USB-C **data** cable.
2. Choose **Tools → Board**:
   - SuperMini: **ESP32C3 Dev Module**, then set **USB CDC On Boot → Enabled**
   - XIAO: **XIAO_ESP32C3**
3. Choose the port and click **Upload**.
4. If the upload won't start, hold **BOOT**, tap **RESET**, release **BOOT**,
   then upload again.

## Make it yours

- **Battery:** the XIAO ESP32-C3 has battery pads and a LiPo charger on its
  underside. Add a 3.7 V 150–300 mAh LiPo (about 30 × 20 × 5 mm) to the back
  with a slide switch. The SuperMini has no charger, so power it from a phone
  or power bank, or add a TP4056 module.
- **Different screens:** for a 1.54" 240×240 screen, set `TFT_HEIGHT 240` and
  run the script with `--height 240`.
- **Pages:** each OLED page is one small function in `business_card.ino`
  (`pageMain`, `pageQr`, `pageContact`). Add your own to the `pages[]` list.

## Licence

MIT. Build it, change it, sell it, share it.
