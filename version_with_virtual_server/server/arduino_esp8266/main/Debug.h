#include <Arduino.h>

class Debug{
  public:
  /*
    print all arguments in serial port

    @param count - count arguments after his
    @param ... more atguments is const char*
  */
    static void printAll(int count, ...);
};