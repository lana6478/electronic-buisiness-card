# Bill of Materials

Prices are rough AliExpress / eBay figures in GBP (late 2026), including cheap
shipping. Amazon usually costs 2–3× more but arrives the next day. The search
terms are what to type into AliExpress.

## Main build: battery + button (~£15–17)

| # | Part | Qty | Search term | Approx. | Notes |
|---|---|---|---|---|---|
| 1 | Seeed Studio XIAO ESP32-C3 | 1 | `Seeed XIAO ESP32C3` | £5–6 | Has a **built-in LiPo charger** and battery pads underneath |
| 2 | 1.69" IPS TFT, ST7789, 240×280, SPI | 1 | `1.69 inch TFT ST7789 240x280` | £2.50–3.50 | Make sure it has the **8-pin** header `GND VCC SCL SDA RES DC CS BLK` |
| 3 | 0.96" OLED, SSD1306, I2C | 1 | `0.96 OLED I2C SSD1306 yellow blue` | £1.20–2.00 | **4-pin** version `GND VCC SCL SDA`. Yellow/blue matches the video |
| 4 | 3.7 V LiPo, ~250 mAh, flat | 1 | `302030 lipo 3.7v` (or `402030`) | £2–3 | 3 × 20 × 30 mm. Get one with a **protection circuit** (most have one), JST plug optional |
| 5 | Mini slide switch, 3-pin, 2.54 mm pitch | 1 | `SS12D00G3 slide switch` | £0.10 | Battery on/off. Usually sold in packs of 20–50 |
| 6 | Tactile push button 6×6 mm | 1 | `6x6 tactile switch 4.3mm` | £0.05 | The 4.3 mm height sits nice and flat. Usually sold in packs of 50–100 |
| 7 | Double-sided perfboard 5×7 cm | 1 | `5x7cm double sided prototype PCB` | £0.20 | Usually sold in packs of 10 for about £2 |
| 8 | Wire | ~1 m | `30AWG wire wrap wire` | £0.30 | Thin wire keeps the back flat for the battery |
| 9 | Kapton or electrical tape | a bit | `kapton tape` | £1 | Insulates the back wiring from the battery |
| | **Total** | | | **≈ £13–17** | |

## Cheapest build: USB power only (~£7–9)

Swap the XIAO for an **ESP32-C3 SuperMini** (`ESP32-C3 SuperMini`, about
£2) and skip parts 4, 5 and 9. The button still works. The SuperMini has
no battery charger, so it runs only while plugged in (a phone, power bank
or charger). Set `BOARD_ESP32C3_SUPERMINI` in `config.h`.

## Tools

- Soldering iron (a TS101, Pinecil or any cheap temperature-controlled iron), solder and flux
- Flush cutters and wire strippers
- Multimeter. **Essential with a battery:** check for shorts before connecting it
- Double-sided foam tape

## Battery life (rough)

| State | Current | 250 mAh lasts |
|---|---|---|
| Screens on, brightness 180 | ~50–60 mA | ~4 hours |
| Screens on, brightness 80 | ~40 mA | ~6 hours |
| Asleep (hold button) | ~1–2 mA | days |
| Slide switch off | 0 | months |

Plugging in USB-C charges the battery while the switch is **on**. The
XIAO's charge LED lights up while charging.

## Why these parts?

- **ESP32-C3:** has 4 MB of flash (about 6 full-screen photos), native
  USB-C and fast SPI. On the XIAO, the LiPo charger is free.
- **Two separate screens:** the colour TFT uses SPI and the OLED uses I2C,
  so they're on different buses and don't fight over pins.
- **5×7 cm perfboard:** at 70 × 50 mm it's already smaller than a credit
  card, and you need no PCB design or ordering.
