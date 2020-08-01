#include <FastLED.h>

#define DATA_PIN      5
#define LED_TYPE      WS2811
#define COLOR_ORDER   RGB
#define NUM_LEDS      54

CRGBArray<NUM_LEDS> leds;

#define LED 2

void setup() {
  FastLED.addLeds<LED_TYPE, DATA_PIN>(leds, NUM_LEDS);
  pinMode(LED, OUTPUT);
}

void loop(){ 
  static uint8_t hue;
  for(int i = 0; i < NUM_LEDS; i++) {   
    // fade everything out
    leds.fadeToBlackBy(40);

    // let's set an led value
    leds[i] = CHSV(hue++,255,255);

    // now, let's first 20 leds to the top 20 leds, 
    FastLED.delay(35);
  }
}
