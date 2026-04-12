#include <sys/stat.h>
#include "Arduino.h"
#include <ESP8266WiFi.h>


class Internet{
  public:
    static const char* begin(const char* SSID, const char* password);
    static const char* sendHttpGet(const char* link);
    static const char* sendPostRequest(const char* link, const char* postData);
};