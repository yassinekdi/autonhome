#include <BH1750.h>
#include <Wire.h>

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
