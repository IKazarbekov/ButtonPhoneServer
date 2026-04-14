#include <Arduino.h>

class Backand{
  public:
    /*  
        input_data - const cstring with arguments, example "log;bob;1234"
        it must not be more than 100 bytes, otherwise the stack will overflow
      
        return - const cstring page html or wml
    */
    static const char* main_processing_request(const char* request);

};