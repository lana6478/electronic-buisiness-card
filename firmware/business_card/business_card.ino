// =====================================================================
//  Dual-screen electronic business card
//  ESP32-C3 + 1.69" ST7789 colour TFT (photo) + 0.96" SSD1306 OLED (info)
//
//  Edit config.h for your name, board and pins.
//  Run tools/make_assets.py to turn your photo / QR link into
//  photo.h and qr.h (the sketch still works without them).
// =====================================================================
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ST7789.h>
#include <Adafruit_SSD1306.h>
#include "config.h"

#if __has_include("photo.h")
  #include "photo.h"
  #define HAVE_PHOTO 1
#else
  #define HAVE_PHOTO 0
#endif

#if __has_include("qr.h")
  #include "qr.h"
  #define HAVE_QR 1
#else
  #define HAVE_QR 0
#endif

Adafruit_ST7789  tft(&SPI, TFT_CS, TFT_DC, TFT_RST);
Adafruit_SSD1306 oled(128, 64, &Wire, -1);
bool oledOk = false;

// ---------------------------------------------------------------- TFT
void drawNameLabel() {
#if SHOW_NAME_ON_PHOTO
  tft.setTextSize(2);
  int16_t x1, y1; uint16_t w, h;
  tft.getTextBounds(CARD_NAME, 0, 0, &x1, &y1, &w, &h);
  int16_t bx = (TFT_WIDTH - (w + 16)) / 2;
  tft.fillRoundRect(bx, 10, w + 16, h + 10, 6, ST77XX_WHITE);
  tft.setTextColor(ST77XX_BLACK);
  tft.setCursor(bx + 8, 15);
  tft.print(CARD_NAME);
#endif
}

void drawPlaceholder() {
  // Vertical gradient + initials, shown until you add a photo
  for (int y = 0; y < TFT_HEIGHT; y++) {
    uint8_t t = map(y, 0, TFT_HEIGHT - 1, 0, 255);
    tft.drawFastHLine(0, y, TFT_WIDTH, tft.color565(40 + t / 3, 20, 120 - t / 3));
  }
  int cx = TFT_WIDTH / 2, cy = TFT_HEIGHT / 2;
  tft.fillCircle(cx, cy, 60, ST77XX_WHITE);
  tft.setTextSize(5);
  tft.setTextColor(tft.color565(60, 20, 110));
  int16_t x1, y1; uint16_t w, h;
  tft.getTextBounds(CARD_INITIALS, 0, 0, &x1, &y1, &w, &h);
  tft.setCursor(cx - w / 2, cy - h / 2);
  tft.print(CARD_INITIALS);
}

void showPhoto(uint8_t idx) {
#if HAVE_PHOTO
  tft.startWrite();
  tft.setAddrWindow(0, 0, PHOTO_W, PHOTO_H);
  tft.writePixels((uint16_t *)PHOTOS[idx], (uint32_t)PHOTO_W * PHOTO_H, true, false);
  tft.endWrite();
#else
  (void)idx;
  drawPlaceholder();
#endif
  drawNameLabel();
}

// --------------------------------------------------------------- OLED
// Yellow/blue OLEDs: the top 16 pixel rows are yellow, the rest blue.
void centerText(const char *s, int y, uint8_t size) {
  oled.setTextSize(size);
  int16_t x1, y1; uint16_t w, h;
  oled.getTextBounds(s, 0, 0, &x1, &y1, &w, &h);
  oled.setCursor((128 - (int)w) / 2, y);
  oled.print(s);
}

void pageMain() {                 // like the one in the video
  centerText(CARD_EMAIL, 4, 1);   // yellow strip
  centerText(CARD_NAME, 24, 2);
  centerText(CARD_TITLE, 46, 1);
}

void pageContact() {
  centerText("say hi!", 4, 1);
  centerText(CARD_EMAIL, 26, 1);
  centerText(CARD_WEBSITE, 42, 1);
}

#if HAVE_QR
void pageQr() {
  const int scale = 60 / QR_SIZE < 1 ? 1 : 60 / QR_SIZE;
  const int px = QR_SIZE * scale;
  const int x0 = 4 + 2, y0 = (64 - px) / 2;
  oled.fillRect(x0 - 2, y0 - 2, px + 4, px + 4, SSD1306_WHITE);   // quiet zone
  const int rowBytes = (QR_SIZE + 7) / 8;
  for (int y = 0; y < QR_SIZE; y++)
    for (int x = 0; x < QR_SIZE; x++)
      if (QR_BITS[y * rowBytes + x / 8] & (0x80 >> (x % 8)))
        oled.fillRect(x0 + x * scale, y0 + y * scale, scale, scale, SSD1306_BLACK);
  oled.setTextSize(1);
  oled.setCursor(x0 + px + 8, 20); oled.print("scan");
  oled.setCursor(x0 + px + 8, 32); oled.print("me :)");
}
#endif

typedef void (*PageFn)();
PageFn pages[] = { pageMain,
#if HAVE_QR
                   pageQr,
#endif
                   pageContact };
const uint8_t PAGE_COUNT = sizeof(pages) / sizeof(pages[0]);

void showPage(uint8_t i) {
  if (!oledOk) return;
  oled.clearDisplay();
  oled.setTextColor(SSD1306_WHITE);
  pages[i]();
  oled.display();
}

// -------------------------------------------------------------- setup
void setup() {
  // Backlight
  pinMode(TFT_BLK, OUTPUT);
  analogWrite(TFT_BLK, TFT_BRIGHTNESS);

  // Colour TFT (SPI, write-only so MISO = -1)
  SPI.begin(TFT_SCK, -1, TFT_MOSI, TFT_CS);
  tft.init(TFT_WIDTH, TFT_HEIGHT);
  tft.setSPISpeed(TFT_SPI_HZ);
  tft.setRotation(0);
  tft.fillScreen(ST77XX_BLACK);

  // OLED (I2C)
  Wire.begin(OLED_SDA, OLED_SCL);
  oledOk = oled.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR);

  showPhoto(0);
  showPage(0);
}

// --------------------------------------------------------------- loop
void loop() {
  static uint32_t lastPage = millis(), lastPhoto = millis();
  static uint8_t page = 0, photo = 0;
  uint32_t now = millis();

  if (PAGE_COUNT > 1 && now - lastPage >= OLED_PAGE_MS) {
    lastPage = now;
    page = (page + 1) % PAGE_COUNT;
    showPage(page);
  }

#if HAVE_PHOTO
  if (PHOTO_COUNT > 1 && now - lastPhoto >= PHOTO_MS) {
    lastPhoto = now;
    photo = (photo + 1) % PHOTO_COUNT;
    showPhoto(photo);
  }
#else
  (void)lastPhoto; (void)photo;
#endif
  delay(10);
}
