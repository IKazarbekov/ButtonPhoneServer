#include "Debug.h"

void Debug::printAll(int count, ...){
  va_list args;
  va_start(args, count);

  for (int i = 0; i < count, i++){
    Serial.printf("", args);
    va_arg(args, const char*);
  }


  va_end(args);
}