#include "Arduino.h"

class Disco{
  public:
    Disco(int pin);

    void blink();
  private:
    int _pin;
};