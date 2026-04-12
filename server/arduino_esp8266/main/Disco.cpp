#include "Disco.h"

Disco::Disco(int pin){
  Serial.begin(9600);
  _pin = pin;
}

void Disco::blink(){
  delay(1000);
  Serial.println(_pin++);
}