# Troubleshooting

| Problem | Fix |
|---|---|
| Upload fails / no port shows up | Use a USB-C **data** cable, not a charge-only one. Hold BOOT, tap RESET, release BOOT, then upload |
| Uploads but nothing at all happens (SuperMini) | Set **Tools → USB CDC On Boot → Enabled**, then re-upload |
| TFT stays black | Check VCC, GND and BLK. If you skipped the BLK wire, the backlight may still be on. Check CS, DC and RES |
| TFT is white or shows noise | SCL and SDA are swapped, or DC isn't connected. Try `TFT_SPI_HZ 20000000UL` in `config.h` |
| Picture is shifted with a band of garbage at the top or bottom | Wrong screen size. A 240×240 screen needs `TFT_HEIGHT 240` (and `--height 240` in the script) |
| Colours inverted (negative image) | Add `tft.invertDisplay(false);` after `tft.init(...)` in `setup()`. Some clone screens need this |
| Colours look wrong (blue face) | Run the script again. If it's still wrong, swap the bytes by changing `writePixels(..., true, false)` to `..., true, true)` |
| OLED stays blank | Swap SDA and SCL, or try `OLED_ADDR 0x3D`. Check that the OLED's VCC/GND order matches your wiring |
| QR won't scan | Use a shorter link (a link shortener or a short domain). Aim for 25 modules or fewer. The script warns if the code is too dense |
| `photo.h` too big / sketch won't fit | Use fewer photos (each one is about 134 KB). Or choose **Tools → Partition Scheme → Huge APP** |
| Compile error about `__has_include` | Update the ESP32 board package to 2.0.x or newer (3.x recommended) |
| Button does nothing | Check that the button goes from the button pin to **GND**. Wire it across opposite corners: the legs on the same long side are connected internally |
| Screens off and won't come back | It's asleep. Tap the button. If that doesn't work, press RESET or turn the switch off and on |
| Upload fails while the card is asleep | Wake it first (tap), or hold BOOT + tap RESET to enter upload mode |
| Won't run on battery | Is the switch on? Check the battery polarity (red → BAT+) and measure the battery: it should read 3.3–4.2 V. A flat LiPo needs about an hour on USB |
| Charge LED flickers with no battery | Normal on the XIAO when no battery is connected |
| Battery gets hot or puffy | **Unplug and disconnect it right away.** Check for shorts and reversed polarity. Never use a swollen LiPo |
