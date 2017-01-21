#include "Arduino.h"

int i = 0;
unsigned long last_heartbeat = 0;

void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);

  last_heartbeat = millis();
}

void loop() {
  unsigned long now = millis();
  if (now - last_heartbeat > 10) {
    last_heartbeat = now;
    Serial.println(i);
    i++;
  }

  if (Serial.available()) {
    Serial.write(Serial.read());
  }
}
