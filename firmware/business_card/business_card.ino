// =====================================================================
//  Dual-screen electronic business card
//  ESP32-C3 + 1.69" ST7789 colour TFT + 0.96" SSD1306 OLED + 1 button
//
//  Button:  tap        -> next scene (changes BOTH screens)
//           hold 1 sec -> screens off + low-power sleep (tap to wake)
//  Auto-off: goes to sleep by itself after AUTO_SLEEP_MS with no presses
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
#include "esp_sleep.h"
#include "driver/gpio.h"
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

// ------------------------------------------------------------ scenes
// A scene = what the colour screen shows + what the OLED shows.
enum SceneType : uint8_t { SC_CARD, SC_QR, SC_INFO, SC_HELP };
SceneType scenes[4];
uint8_t sceneCount = 0, scene = 0;

void buildScenes() {
  scenes[sceneCount++] = SC_CARD;                     // photo + name
#if HAVE_QR
  scenes[sceneCount++] = SC_QR;                       // big QR + "scan me"
#endif
  scenes[sceneCount++] = SC_INFO;                     // text card + contact
  scenes[sceneCount++] = SC_HELP;                     // how to use the button
}

// --------------------------------------------------------------- TFT
// Print centred text, shrinking it if it is too wide for the screen.
void tftCenter(const char *s, int y, uint8_t size, uint16_t color) {
  int16_t x1, y1; uint16_t w, h;
  do {
    tft.setTextSize(size);
    tft.getTextBounds(s, 0, 0, &x1, &y1, &w, &h);
  } while (w > TFT_WIDTH - 8 && --size > 1);
  tft.setTextColor(color);
  tft.setCursor((TFT_WIDTH - (int)w) / 2, y);
  tft.print(s);
}

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

void drawGradient() {
  for (int y = 0; y < TFT_HEIGHT; y++) {
    uint8_t t = map(y, 0, TFT_HEIGHT - 1, 0, 255);
    tft.drawFastHLine(0, y, TFT_WIDTH, tft.color565(40 + t / 3, 20, 120 - t / 3));
  }
}

void tftPhoto() {
#if HAVE_PHOTO
  tft.startWrite();
  tft.setAddrWindow(0, 0, PHOTO_W, PHOTO_H);
  tft.writePixels((uint16_t *)PHOTO, (uint32_t)PHOTO_W * PHOTO_H, true, false);
  tft.endWrite();
#else
  // placeholder until you add a photo
  drawGradient();
  tft.fillCircle(TFT_WIDTH / 2, TFT_HEIGHT / 2, 60, ST77XX_WHITE);
  tftCenter(CARD_INITIALS, TFT_HEIGHT / 2 - 17, 5, tft.color565(60, 20, 110));
#endif
  drawNameLabel();
}

void tftInfo() {
  drawGradient();
  tftCenter(CARD_NAME, 60, 3, ST77XX_WHITE);
  tftCenter(CARD_TITLE, 100, 2, ST77XX_YELLOW);
  tft.drawFastHLine(40, 135, TFT_WIDTH - 80, ST77XX_WHITE);
  tftCenter(CARD_EMAIL, 160, 2, ST77XX_WHITE);
  tftCenter(CARD_WEBSITE, 195, 2, ST77XX_CYAN);
}

#if HAVE_QR
void tftQr() {
  tft.fillScreen(ST77XX_WHITE);
  int scale = 200 / QR_SIZE; if (scale < 1) scale = 1;
  const int px = QR_SIZE * scale;
  const int x0 = (TFT_WIDTH - px) / 2, y0 = (TFT_HEIGHT - px) / 2 - 10;
  const int rowBytes = (QR_SIZE + 7) / 8;
  tft.startWrite();
  for (int y = 0; y < QR_SIZE; y++)
    for (int x = 0; x < QR_SIZE; x++)
      if (QR_BITS[y * rowBytes + x / 8] & (0x80 >> (x % 8)))
        tft.writeFillRect(x0 + x * scale, y0 + y * scale, scale, scale, ST77XX_BLACK);
  tft.endWrite();
  tftCenter("scan me :)", y0 + px + 14, 2, ST77XX_BLACK);
}
#endif

void tftHelp() {
  const uint16_t bg = tft.color565(20, 24, 40);
  const uint16_t card = tft.color565(45, 52, 80);
  tft.fillScreen(bg);
  tftCenter("HOW TO USE", 18, 3, ST77XX_YELLOW);
  tftCenter("the button", 48, 2, ST77XX_WHITE);

  struct { const char *head, *l1, *l2; uint16_t col; } rows[] = {
    { "TAP",         "next page",       "",                  ST77XX_CYAN   },
    { "HOLD 1 SEC",  "screens off",     "(sleep)",           ST77XX_YELLOW },
    { "WHEN ASLEEP", "tap to wake up",  "",                  ST77XX_GREEN  },
  };
  int y = 78;
  for (auto &r : rows) {
    tft.fillRoundRect(12, y, TFT_WIDTH - 24, 52, 8, card);
    tftCenter(r.head, y + 8, 2, r.col);
    String line = String(r.l1) + (r.l2[0] ? String(" ") + r.l2 : String(""));
    tftCenter(line.c_str(), y + 32, 1, ST77XX_WHITE);
    y += 60;
  }
#if AUTO_SLEEP_MS > 0
  char buf[40];
  snprintf(buf, sizeof(buf), "turns off by itself after %lu min", (unsigned long)(AUTO_SLEEP_MS / 60000UL));
  tftCenter(buf, y + 4, 1, tft.color565(170, 170, 190));
#endif
}

// -------------------------------------------------------------- OLED
// Yellow/blue OLEDs: the top 16 pixel rows are yellow, the rest blue.
void oledCenter(const char *s, int y, uint8_t size) {
  int16_t x1, y1; uint16_t w, h;
  do {
    oled.setTextSize(size);
    oled.getTextBounds(s, 0, 0, &x1, &y1, &w, &h);
  } while (w > 126 && --size > 1);
  oled.setCursor((128 - (int)w) / 2, y);
  oled.print(s);
}

void oledDots() {               // little "which scene am I on" dots
  int x = 64 - (sceneCount - 1) * 4;
  for (uint8_t i = 0; i < sceneCount; i++, x += 8)
    i == scene ? oled.fillCircle(x, 61, 2, SSD1306_WHITE)
               : oled.drawCircle(x, 61, 2, SSD1306_WHITE);
}

void oledShow(SceneType t) {
  if (!oledOk) return;
  oled.clearDisplay();
  oled.setTextColor(SSD1306_WHITE);
  switch (t) {
    case SC_CARD:
      oledCenter(CARD_EMAIL, 4, 1);           // yellow strip
      oledCenter(CARD_NAME, 22, 2);
      oledCenter(CARD_TITLE, 42, 1);
      break;
    case SC_QR:
      oledCenter("<- scan me", 4, 1);
      oledCenter(CARD_WEBSITE, 28, 1);
      break;
    case SC_INFO:
      oledCenter("say hi!", 4, 1);
      oledCenter(CARD_EMAIL, 24, 1);
      oledCenter(CARD_WEBSITE, 38, 1);
      break;
    case SC_HELP:
      oledCenter("BUTTON HELP", 4, 1);
      oled.setTextSize(1);
      oled.setCursor(4, 20); oled.print("tap   = next page");
      oled.setCursor(4, 31); oled.print("hold  = sleep");
      oled.setCursor(4, 42); oled.print("tap again = wake");
      break;
  }
  oledDots();
  oled.display();
}

// ------------------------------------------------------------- show
void showScene() {
  switch (scenes[scene]) {
    case SC_CARD:  tftPhoto(); break;
    case SC_INFO:  tftInfo();  break;
    case SC_HELP:  tftHelp();  break;
#if HAVE_QR
    case SC_QR:    tftQr();    break;
#endif
    default: break;
  }
  oledShow(scenes[scene]);
}

void nextScene() {
  scene = (scene + 1) % sceneCount;
  showScene();
}

// ------------------------------------------------------------ sleep
// Screens off, CPU in light sleep (~1 mA) until the button is pressed.
void waitRelease() {
  while (digitalRead(BTN_PIN) == LOW) delay(10);
  delay(50);
}

void sleepUntilButton() {
  analogWrite(TFT_BLK, 0);
  tft.enableSleep(true);
  if (oledOk) oled.ssd1306_command(SSD1306_DISPLAYOFF);
  waitRelease();

  gpio_wakeup_enable((gpio_num_t)BTN_PIN, GPIO_INTR_LOW_LEVEL);
  esp_sleep_enable_gpio_wakeup();
  esp_light_sleep_start();                 // ...zzz...
  gpio_wakeup_disable((gpio_num_t)BTN_PIN);

  waitRelease();                           // the wake-up press isn't a "tap"
  tft.enableSleep(false);
  delay(120);
  if (oledOk) oled.ssd1306_command(SSD1306_DISPLAYON);
  showScene();
  analogWrite(TFT_BLK, TFT_BRIGHTNESS);
}

// ------------------------------------------------------------ setup
void setup() {
  setCpuFrequencyMhz(80);                  // plenty fast, saves battery

  pinMode(BTN_PIN, INPUT_PULLUP);
  pinMode(TFT_BLK, OUTPUT);
  analogWrite(TFT_BLK, 0);                 // backlight on after first draw

  SPI.begin(TFT_SCK, -1, TFT_MOSI, TFT_CS);
  tft.init(TFT_WIDTH, TFT_HEIGHT);
  tft.setSPISpeed(TFT_SPI_HZ);
  tft.setRotation(0);
  tft.fillScreen(ST77XX_BLACK);

  Wire.begin(OLED_SDA, OLED_SCL);
  oledOk = oled.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR);

  buildScenes();
  showScene();
  analogWrite(TFT_BLK, TFT_BRIGHTNESS);
}

// ------------------------------------------------------------- loop
void loop() {
  static bool     held = false, longDone = false;
  static uint32_t pressedAt = 0, lastAuto = millis(), lastPress = millis();
  const uint32_t  now  = millis();
  const bool      down = digitalRead(BTN_PIN) == LOW;

  if (down && !held) {                       // just pressed
    delay(20);                               // debounce
    if (digitalRead(BTN_PIN) == LOW) { held = true; longDone = false; pressedAt = now; lastPress = now; }
  } else if (down && held && !longDone && now - pressedAt >= LONG_PRESS_MS) {
    longDone = true;                         // held long enough -> sleep
    sleepUntilButton();
    held = false;
    lastAuto = lastPress = millis();
  } else if (!down && held) {                // released
    held = false;
    if (!longDone) { nextScene(); lastAuto = now; }
    delay(20);
  }

#if AUTO_SLEEP_MS > 0                        // auto-off after no presses
  if (!held && now - lastPress >= AUTO_SLEEP_MS) {
    sleepUntilButton();
    lastAuto = lastPress = millis();
    return;
  }
#else
  (void)lastPress;
#endif

#if AUTO_ADVANCE_MS > 0
  if (!held && now - lastAuto >= AUTO_ADVANCE_MS) { lastAuto = now; nextScene(); }
#else
  (void)lastAuto;
#endif
  delay(5);
}
