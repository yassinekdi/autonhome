#include <BH1750.h>
#include <Wire.h>


const char* WIFI_SSID = "Bbox-32BE8614";
const char* WIFI_PASSWORD = "PcPQPfmPXTqVShDF6F";

String FIREBASE_HOST = "https://autonhome-af7ba-default-rtdb.europe-west1.firebasedatabase.app/";
String FIREBASE_AUTH = "idCrjvKYAhGFV56Yfnx8FbGtEzBDOzDGuvA40v7L";
String UserId = "8";

BH1750 lightMeter(0x23);

void setup() {
  Serial.begin(115200);

  // Initialize the I2C bus (BH1750 library doesn't do this automatically)
  Wire.begin();

  // Configure the BH1750 sensor
  if (lightMeter.begin(BH1750::CONTINUOUS_HIGH_RES_MODE)) {
    Serial.println(F("BH1750 sensor is configured."));
  } else {
    Serial.println(F("Error: BH1750 sensor not configured!"));
  }
}

void loop() {
  float lux = lightMeter.readLightLevel();
  Serial.println("");
  Serial.print("Light: ");
  Serial.print(lux);
  Serial.println(" lx");
  delay(1000);
}
