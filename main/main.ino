#include <FastLED.h>

#define DATA_PIN      5
#define LED_TYPE      WS2811
#define COLOR_ORDER   RGB
#define NUM_LEDS      84

CRGBArray<NUM_LEDS> leds;

#define LED 2

void setup() {
  FastLED.addLeds<LED_TYPE, DATA_PIN>(leds, NUM_LEDS);
  pinMode(LED, OUTPUT);
}

void loop() {
  uint8_t hue = 0;
  uint8_t delay_time;
  delay_time = 30;
  uint8_t fade_time = 30;
  //fade everything out
  leds.fadeToBlackBy(fade_time);

  // let's set an led value
  //leds[i] = CHSV(hue++, 255, 255);

  // now, let's first 20 leds to the top 20 leds,
  //FastLED.delay(35);
  headlights(hue, delay_time, fade_time, true);
  Serial.println("Loop over");
}

void headlights(uint8_t hue, uint8_t delay_time, uint8_t fade_time, bool sequential) {
  uint8_t h = hue;
  if (sequential) {
    for (int i = 60; i < NUM_LEDS; i++) {
      leds[i] = CHSV(h++, 255, 255);
      FastLED.delay(delay_time);
      Serial.println(i);
    }
  } else {
    //for(CRGB & pixel : leds(61,NUM_LEDS)) { pixel = CRGB( r, g, b); }
    FastLED.show();
    FastLED.delay(delay_time);
  }
  //Serial.println("Red: " + r + ", Green: " + g + ", Blue: " + b);
}
