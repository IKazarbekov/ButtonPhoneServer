#include <cstring>
#include <sys/string.h>
#include "Internet.h"
#include <ESP8266HTTPClient.h>

/*
 * Connects ESP to WiFi network.
 * Blocks execution until connection is established.
 *
 * @param SSID - WiFi network name
 * @param password - WiFi password
 * @return status message
 */
const char* Internet::begin(const char* SSID, const  char* password){
    WiFi.begin(SSID, password);

    // Wait until connected
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
    }

    return "Connected";
};


/*
 * Sends HTTP GET request.
 *
 * ⚠️ PROBLEM:
 * Returns pointer to temporary String buffer (payload.c_str()).
 * This becomes invalid after function exits → undefined behavior.
 *
 * @param link - URL to request
 * @return response body (UNSAFE CURRENTLY)
 */
const char* Internet::sendHttpGet(const char* link) {
    if (WiFi.status() == WL_CONNECTED) {
        WiFiClient client;
        HTTPClient http;
        
        http.begin(client, link);
        int httpCode = http.GET();
        
        if (httpCode > 0) {
            if (httpCode == HTTP_CODE_OK) {

                // String exists only inside this scope
                const String payload = http.getString();

                http.end();

                // return result
                char* result = new char[payload.length() + 1];
                strcpy(result, payload.c_str());
                return result;
            }
        } else {
            http.end();
            Serial.printf("HTTP error: %s\n", http.errorToString(httpCode).c_str());
        }
    }

    return "Error";
}


/*
 * Sends HTTP POST request with form data:
 * page=<HTML or data>
 *
 * Uses PROGMEM string for pageData.
 *
 * @param link - URL
 * @param pageData - data stored in PROGMEM
 * @return response string with HTTP code and optional body
 */
const char* Internet::sendPostRequest(const char* link, const char* pageData) {
    WiFiClient client;
    HTTPClient http;
    
    http.begin(client, link);

    // Set content type for form submission
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");
    
    // Calculate required buffer size:
    // "page=" (5 chars) + data + null terminator
    int lengthData = 6 + strlen_P(pageData) + 1;

    // Allocate buffer for POST data
    char* data = new char[lengthData];

    // Copy "page=" into buffer
    strcpy(data, "page=");

    // Append PROGMEM string safely
    strcat_P(data, pageData);

    // Send POST request
    int httpCode = http.POST(data);

    //Clear data
    delete[] data;

    // Allocate buffer for response text
    char* responseAndCode = new char[200]();
    
    if (httpCode > 0) {
        // Write HTTP status code into buffer
        sprintf(responseAndCode, "HTTP Code: %d\n", httpCode);

        if (httpCode == HTTP_CODE_OK) {

            // Get response body
            String response = http.getString();
            // BUG: possible buffer overflow (responseAndCode too small)
            strcat(responseAndCode, response.c_str());
        }

        } else {
            // Write error message
            sprintf(responseAndCode, "Error %s\n", http.errorToString(httpCode).c_str());
        }
    
    http.end();

    return responseAndCode;
}

bool Internet::isConnectWiFi(){
    return WiFi.status() == WL_CONNECTED;
};

void Internet::reconnect(){
    WiFi.reconnect();
};