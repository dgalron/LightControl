#include <Arduino.h>
#include <Adafruit_CC3000.h>
#include <SPI.h>
#include <String.h>

#include <utility/debug.h>

// These are the interrupt and control pins
#define ADAFRUIT_CC3000_IRQ   3  // MUST be an interrupt pin!
// These can be any two pins
#define ADAFRUIT_CC3000_VBAT  5
#define ADAFRUIT_CC3000_CS    10
// Use hardware SPI for the remaining pins
// On an UNO, SCK = 13, MISO = 12, and MOSI = 11
Adafruit_CC3000 cc3000 = Adafruit_CC3000(ADAFRUIT_CC3000_CS, ADAFRUIT_CC3000_IRQ, ADAFRUIT_CC3000_VBAT,
                                         SPI_CLOCK_DIVIDER); // you can change this clock speed

#define WLAN_SSID       "Q82L9ETY6"        // cannot be longer than 32 characters!
#define WLAN_PASS       "tardis_5811!#"
// Security can be WLAN_SEC_UNSEC, WLAN_SEC_WEP, WLAN_SEC_WPA or WLAN_SEC_WPA2
#define WLAN_SECURITY   WLAN_SEC_WPA2

#define LISTEN_PORT           1234    // What TCP port to listen on for connections.

#define WARM_PIN 1
#define COOL_PIN 0


Adafruit_CC3000_Server lightServer(LISTEN_PORT);

uint8_t powerState;
uint8_t brightnessState;
uint8_t redValue;
uint8_t greenValue;
uint8_t blueValue;
uint32_t colorPattern;

uint8_t lightstate[8];
uint8_t ix = 0;

#define PROTOCOL_BLUE_STATE_IX 3
#define PROTOCOL_GREEN_STATE_IX 4
#define PROTOCOL_RED_STATE_IX 5
#define PROTOCOL_BRIGHT_STATE_IX 6
#define PROTOCOL_POWER_STATE_IX 7

void setup(void)
{
  analogWrite(WARM_PIN, 0);
  analogWrite(COOL_PIN, 0);
  Serial.begin(115200);
  Serial.println(F("Initializing light control server"));
  Serial.print("Free Ram: ");
  Serial.println(getFreeRam(), DEC);
  
  if (!cc3000.begin()) {
    Serial.println(F("Couldn't begin c3000 chip. Check wiring"));
    while(1);
  }
  
  if (!cc3000.connectToAP(WLAN_SSID, WLAN_PASS, WLAN_SECURITY)) {
    Serial.println(F("Failed to connect to network!"));
    while(1);
  }
  
  Serial.println(F("Connected! Requesting DHCP"));
  while (!cc3000.checkDHCP()) {
    delay(100);
  }
  while(!displayConnectionDetails()) {
    delay(1000);
  }
  lightServer.begin();
  Serial.println(F("Listening for connections..."));
}

void loop(void)
{
  Adafruit_CC3000_ClientRef client = lightServer.available();
  if (client) {
    // Check if there is data available to read.
    if (client.available() > 0) {
      lightstate[ix++] = client.read();
      Serial.print("lightstate ");
      for (int i = 0; i < 8; ++i) {
        String string = String(lightstate[i], BIN);
        Serial.print(string);
        Serial.print(" ");
      }
      Serial.println("");
    }
  }
  // At this point we've read in a full packet
  if (ix == 8) {
    powerState = lightstate[PROTOCOL_POWER_STATE_IX];
    brightnessState = lightstate[PROTOCOL_POWER_STATE_IX];
    redValue = lightstate[PROTOCOL_RED_STATE_IX];
    greenValue = lightstate[PROTOCOL_GREEN_STATE_IX];
    blueValue = lightstate[PROTOCOL_BLUE_STATE_IX];
    for (uint8_t i = 2; i >= 0; i--) {
      colorPattern = (colorPattern << 8) | lightstate[i];
    }
    setLightState();
    ix = 0;
  }
}

void setLightState(void)
{
  if !(powerState & 0x80) {
    turnOff();
  }
}

void turnOff(void)
{
  analogWrite(WARM_PIN, 0);
  analogWrite(COOL_PIN, 0);
}

bool displayConnectionDetails(void)
{
  uint32_t ipAddress, netmask, gateway, dhcpserv, dnsserv;
  
  if(!cc3000.getIPAddress(&ipAddress, &netmask, &gateway, &dhcpserv, &dnsserv))
  {
    Serial.println(F("Unable to retrieve the IP Address!\r\n"));
    return false;
  }
  else
  {
    Serial.print(F("\nIP Addr: ")); cc3000.printIPdotsRev(ipAddress);
    Serial.print(F("\nNetmask: ")); cc3000.printIPdotsRev(netmask);
    Serial.print(F("\nGateway: ")); cc3000.printIPdotsRev(gateway);
    Serial.print(F("\nDHCPsrv: ")); cc3000.printIPdotsRev(dhcpserv);
    Serial.print(F("\nDNSserv: ")); cc3000.printIPdotsRev(dnsserv);
    Serial.println();
    return true;
  }
}
