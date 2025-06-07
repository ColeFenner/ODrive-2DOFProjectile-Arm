//Code that is uploaded to the esp32 through Ardino IDE 
//
//
//

#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "admin";
const char* password = "admin";

WebServer server(80);

const int switchPin = 2;  // GPIO pin connected to your switch
const int relayPin = 4;  // GPIO pin connected to your switch


bool switchState = false;

void handleToggle() {
  switchState = !switchState;
  digitalWrite(switchPin, switchState ? HIGH : LOW);
  digitalWrite(relayPin, switchState ? HIGH : LOW);



  server.send(200, "text/plain", switchState ? "ON" : "OFF");
}

void setup() {
  Serial.begin(115200);
  pinMode(switchPin, OUTPUT);
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, LOW);
  digitalWrite(switchPin, LOW);

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected!");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  server.on("/toggle", handleToggle);
  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
}
