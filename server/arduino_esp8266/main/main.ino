#include <ESP8266WiFi.h>
#include "Internet.h"
#include "Page.h"

// Настройки Wi-Fi
const char* ssid = "FreeBashnl";
const char* password = "18042026";
const char* linkGet PROGMEM = "http://ikazarbekov.alwaysdata.net/server/get?password=wig";
const char* linkSend PROGMEM = "http://ikazarbekov.alwaysdata.net/server/send?password=wig";

void setup() {
    Serial.begin(115200);
    delay(1000);
    Serial.println();

    Serial.println("Connect to WiFi...");
    const char* result = Internet::begin(ssid, password);
    Serial.println(result);

    Internet::sendHttpGet(linkGet);
    /*
    // Ждём подключения
    Serial.print("Подключение");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    
    Serial.println();
    Serial.println("✅ Wi-Fi подключён!");
    Serial.print("IP адрес: ");
    Serial.println(WiFi.localIP());
    Serial.print("Сила сигнала: ");
    Serial.print(WiFi.RSSI());
    Serial.println(" dBm");*/
}

void loop() {
    static ushort count_iteration = 0;
    Serial.println("\n\n\n---------------------");
    Serial.printf("ITERATION #%d\n", count_iteration++);
    Serial.printf("Free heap: %u bytes\n\n", ESP.getFreeHeap());

    Serial.println("checked requests...");
    const char* data = Internet::sendHttpGet(linkGet);
    Serial.printf("Result: %s\n", data);

    if (strcmp(data, "none") != 0) {
        Serial.println("Send answer...");
        const char* response = Internet::sendPostRequest(linkSend, Page::login);
        Serial.println(response);
        delete[] response;
    }

    delay(1000);
    /*
    // Проверяем соединение каждые 10 секунд
    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("❌ Соединение потеряно! Переподключаюсь...");
        WiFi.reconnect();
        delay(1000);
    }
    delay(10000);

    


    */
}