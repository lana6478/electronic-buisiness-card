# Bill of Materials

Prices are rough AliExpress / eBay figures in GBP (late 2026), including cheap
shipping. Amazon usually costs 2–3× more but arrives the next day. The search
terms are what to type into AliExpress.

> **Want the links?** See **[BUY.md](BUY.md)** for a shopping list with links for every part.

## Main build: battery + button (~£10)

| # | Part | Qty | Search term | Approx. | Notes |
|---|---|---|---|---|---|
| 1 | ESP32-C3 SuperMini | 1 | `ESP32-C3 SuperMini` | £1.50–2.50 | Usually sold in packs of 3 for even less each |
| 2 | 1.69" IPS TFT, ST7789, 240×280, SPI | 1 | `1.69 inch TFT ST7789 240x280` | £2.50–3.50 | Make sure it has the **8-pin** header `GND VCC SCL SDA RES DC CS BLK` |
| 3 | 0.96" OLED, SSD1306, I2C | 1 | `0.96 OLED I2C SSD1306` | £1.20–2.00 | **4-pin** version `GND VCC SCL SDA`. Yellow/blue matches the video, plain white is often cheaper |
| 4 | 3.7 V LiPo, ~250 mAh, flat | 1 | `302030 lipo 3.7v` | £1.50–2.50 | 3 × 20 × 30 mm. Get one **with a protection circuit** |
| 5 | TP4056 USB-C charger module **with protection** | 1 | `TP4056 type-c protection` | £0.30–0.50 | The version with **6 pads** (B+ B− OUT+ OUT− IN+ IN−) and two little chips. Usually sold in packs of 5–10 |
| 6 | Schottky diode 1N5817, 1N5818 or 1N5819 (any of them) | 1 | `1N5817` | £0.02 | Stops USB power flowing back into the battery |
| 7 | Mini slide switch, 3-pin, 2.54 mm pitch | 1 | `SS12D00G3 slide switch` | £0.05 | Battery on/off |
| 8 | Tactile push button 6×6 mm | 1 | `6x6 tactile switch 4.3mm` | £0.03 | Changes scenes and sleeps |
| 9 | Double-sided perfboard 5×7 cm | 1 | `5x7cm double sided prototype PCB` | £0.20 | Usually sold in packs of 10 for about £2 |
| 10 | Wire | ~1 m | `30AWG wire wrap wire` | £0.30 | Thin wire keeps the back flat for the battery |
| 11 | Kapton or electrical tape | a bit | `kapton tape` | £0.50 | Insulates the back wiring from the battery |
| | **Total** | | | **≈ £9–11** | |

## Ways to make it even cheaper

- **No battery (~£7):** skip parts 4, 5, 6, 7 and 11. The card then runs
  whenever it's plugged into USB-C (a phone, power bank or charger). The
  button still works.
- **Buy in packs and make 2–3:** the SuperMini, perfboard, switches,
  buttons, diodes and TP4056 are all cheapest in packs. With friends, each
  card costs about £7–8 *with* a battery.
- **Use a white OLED** instead of yellow/blue: it's often £0.30 cheaper.
- **Use AliExpress "Choice" / bundle deals:** shipping is free over about
  £10, so order everything from Choice sellers in one basket.

## Easier but pricier option: Seeed XIAO ESP32-C3 (+£4)

The XIAO (`Seeed XIAO ESP32C3`, about £5–6) has a battery charger built
in, so you can skip the TP4056 and the diode and charge through the same
USB-C you program with. Set `BOARD_XIAO_ESP32C3` in `config.h`. It's
neater, but the total comes to about £14.

## Tools

- Soldering iron (a TS101, Pinecil or any cheap temperature-controlled iron), solder and flux
- Flush cutters and wire strippers
- Multimeter. **Essential with a battery:** check for shorts before connecting it
- Double-sided foam tape

## Battery life (rough)

| State | Current | 250 mAh lasts |
|---|---|---|
| Screens on, brightness 180 | ~50–60 mA | ~3–4 hours |
| Screens on, brightness 80 | ~40 mA | ~5 hours |
| Asleep (hold button, or auto-off after 5 min) | ~1–3 mA* | 3–8 days |
| Slide switch off | 0 | months |

\* The SuperMini's red power LED alone uses about 1–2 mA. For the longest
sleep time, remove it: carefully scrape it off or desolder it. Otherwise just
flip the slide switch off when the card goes in your pocket.

## Why these parts?

- **ESP32-C3 SuperMini:** cheaper than an Arduino Nano, but with 4 MB of
  flash for a full-screen photo, native USB-C and fast SPI.
- **TP4056 with protection:** safely charges the LiPo from USB-C and cuts
  it off before it over-discharges.
- **Two separate screens:** the colour TFT uses SPI and the OLED uses I2C,
  so they're on different buses and don't fight over pins.
- **5×7 cm perfboard:** at 70 × 50 mm it's already smaller than a credit
  card, and you need no PCB design or ordering.
