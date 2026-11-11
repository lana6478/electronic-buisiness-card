# Bill of Materials

Prices are rough AliExpress / eBay figures in GBP (late 2026), including cheap
shipping. Amazon usually costs 2–3× more but arrives the next day. The search
terms are what to type into AliExpress.

## Budget build (~£7–9)

| # | Part | Qty | Search term | Approx. | Notes |
|---|---|---|---|---|---|
| 1 | ESP32-C3 SuperMini | 1 | `ESP32-C3 SuperMini` | £1.50–2.50 | Same chip as the XIAO, just cheaper. Often sold in packs of 3–5 |
| 2 | 1.69" IPS TFT, ST7789, 240×280, SPI | 1 | `1.69 inch TFT ST7789 240x280` | £2.50–3.50 | Make sure it has the **8-pin** header `GND VCC SCL SDA RES DC CS BLK` |
| 3 | 0.96" OLED, SSD1306, I2C | 1 | `0.96 OLED I2C SSD1306 yellow blue` | £1.20–2.00 | **4-pin** version `GND VCC SCL SDA`. Yellow/blue matches the video; plain white also works |
| 4 | Double-sided perfboard 5×7 cm | 1 | `5x7cm double sided prototype PCB` | £0.20 | Usually sold in packs of 10 for about £2. Green FR4 with plated holes |
| 5 | Wire | ~1 m | `30AWG wire wrap wire` | £0.30 | Thin wire makes the back neat. Solid-core bell wire also works |
| 6 | Male pin headers | 1 strip | `2.54mm pin header` | £0.10 | Displays and boards usually come with these |
| | **Total** | | | **≈ £6–9** | |

## "Same as the video" upgrade

| Part | Search term | Approx. |
|---|---|---|
| Seeed Studio XIAO ESP32-C3 (instead of the SuperMini) | `Seeed XIAO ESP32C3` | £5–6 |
| 3.7 V LiPo, 150–300 mAh, flat (optional) | `302030 lipo` / `402030 lipo` | £2–3 |
| Mini slide switch (optional, with the battery) | `SS12D00 slide switch` | £0.10 |

## Tools

- Soldering iron (a TS101, Pinecil or any cheap temperature-controlled iron), solder and flux
- Flush cutters and wire strippers
- Multimeter, for checking for shorts before you power it up
- Optional: double-sided foam tape and some M2 nylon standoffs

## Why these parts?

- **ESP32-C3:** costs less than an Arduino Nano, has 4 MB of flash (enough
  for about 6 full-screen photos), native USB-C, and fast SPI so the photo
  draws in a blink.
- **Two separate screens:** the colour TFT uses SPI and the OLED uses I2C, so
  they're on different buses and don't fight over pins.
- **5×7 cm perfboard:** at 70 × 50 mm it's already smaller than a credit card,
  and you need no PCB design or ordering.
