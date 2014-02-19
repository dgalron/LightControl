#include <Arduino.h>
#include <Adafruit_CC3000.h>
#include <SPI.h>

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

#define WLAN_SSID       "xxx"        // cannot be longer than 32 characters!
#define WLAN_PASS       "yyy"
// Security can be WLAN_SEC_UNSEC, WLAN_SEC_WEP, WLAN_SEC_WPA or WLAN_SEC_WPA2
#define WLAN_SECURITY   WLAN_SEC_WPA2

#define LISTEN_PORT           1234    // What TCP port to listen on for connections.

Adafruit_CC3000_Server lightServer(LISTEN_PORT);

void setup(void)
{
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
     char buffer[64];
     uint32_t i = 0;
     if (client.available() > 0) {
       // Read a byte and write it to all clients.
       uint8_t ch = client.read();
       lightServer.write(ch
       buffer[i++] = ch;
     }
     buffer[i++] = 0;
     Serial.print(buffer);
     Serial.println(F(""));
  }
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
