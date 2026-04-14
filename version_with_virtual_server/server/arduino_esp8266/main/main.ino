#include <ESP8266WiFi.h>
#include "Internet.h"
#include "Page.h"
#include "Backand.h"
#include "Session.h"

// Настройки Wi-Fi
//const char* ssid = "FreeBashnl";
//const char* password = "18042026";
//const char* linkGet PROGMEM = "http://ikazarbekov.alwaysdata.net/server/get?password=wig";
//const char* linkSend PROGMEM = "http://ikazarbekov.alwaysdata.net/server/send?password=wig";
const char* ssid = "KazarbekovGadget";
const char* password = "12345678";
const char* linkGet PROGMEM = "http://10.42.0.1:8080/server/get?password=wig";
const char* linkSend PROGMEM = "http://10.42.0.1:8080/server/send?password=wig";

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
    Serial.println(F("\n\n\n---------------------"));
    Serial.printf("ITERATION #%d\n", count_iteration++);
    Serial.printf("Free heap: %u bytes\n\n", ESP.getFreeHeap());
    delay(1000);

    // get data from client
    Serial.println(F("checked requests..."));
    const char* data = Internet::sendHttpGet(linkGet);
    Serial.printf("Result: %s\n", data);

    // if exists requests from client
    if (strcmp(data, "none") != 0) {
        // processing data and create answer
        const char* answer = Backand::main_processing_request(data);

        Serial.println("Send answer...");
        const char* response = Internet::sendPostRequest(linkSend, answer);
        Serial.println(response);
        delete[] response;
    }

    delete[] data;
    
    while (!Internet::isConnectWiFi()){
        Serial.println("\n\n\n\nConnection failed.\nReconected...");
        Internet::reconnect();
        delay(5000);
    }
}