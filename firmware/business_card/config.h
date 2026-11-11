// =====================================================================
//  config.h  -  EVERYTHING YOU NEED TO EDIT IS IN THIS FILE
// =====================================================================
#pragma once

// ---------------------------------------------------------------------
// 1. Which microcontroller board are you using?  Uncomment ONE line.
// ---------------------------------------------------------------------
#define BOARD_ESP32C3_SUPERMINI      // cheapest (~£2)  <- default
// #define BOARD_XIAO_ESP32C3        // Seeed Studio XIAO ESP32-C3 (~£5-6)

// ---------------------------------------------------------------------
// 2. Your details (shown on the small OLED screen)
// ---------------------------------------------------------------------
#define CARD_NAME     "Your Name"
#define CARD_TITLE    "engineer :3"
#define CARD_EMAIL    "you@email.com"
#define CARD_WEBSITE  "github.com/you"
#define CARD_INITIALS "YN"            // used if you have no photo yet

// Show your name in a little label on top of the photo (1 = yes, 0 = no)
#define SHOW_NAME_ON_PHOTO 1

// ---------------------------------------------------------------------
// 3. Colour screen size. The 1.69" ST7789 is 240x280 (default).
//    For a 1.54" or 1.3" ST7789 use 240 x 240.
// ---------------------------------------------------------------------
#define TFT_WIDTH   240
#define TFT_HEIGHT  280

// ---------------------------------------------------------------------
// 4. Timing and brightness
// ---------------------------------------------------------------------
#define OLED_PAGE_MS     4000   // how long each OLED page stays up
#define PHOTO_MS         6000   // slideshow speed (only if >1 photo)
#define TFT_BRIGHTNESS   200    // 0-255 backlight brightness
#define TFT_SPI_HZ       40000000UL  // drop to 20000000UL if the picture glitches

// ---------------------------------------------------------------------
// 5. Pin mapping - matches docs/WIRING.md. Only change it if you wire
//    it differently. Numbers are GPIO numbers.
// ---------------------------------------------------------------------
#if defined(BOARD_XIAO_ESP32C3)
  //            GPIO      XIAO label
  #define TFT_SCK    8    // D8
  #define TFT_MOSI  10    // D10
  #define TFT_RST    2    // D0
  #define TFT_DC     3    // D1
  #define TFT_CS     4    // D2
  #define TFT_BLK    5    // D3
  #define OLED_SDA   6    // D4
  #define OLED_SCL   7    // D5
#elif defined(BOARD_ESP32C3_SUPERMINI)
  #define TFT_SCK    4
  #define TFT_MOSI   6
  #define TFT_RST    1
  #define TFT_DC    10
  #define TFT_CS     7
  #define TFT_BLK    3
  #define OLED_SDA   8
  #define OLED_SCL   9
#else
  #error "Pick a board at the top of config.h"
#endif

#define OLED_ADDR 0x3C   // most 0.96" OLEDs. Try 0x3D if the screen stays blank.
