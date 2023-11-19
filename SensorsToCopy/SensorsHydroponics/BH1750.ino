#include <Wire.h>
#include <BH1750.h>

BH1750 lightMeter;

void setupBH() {
  // Serial.begin(115200);

  Wire.begin(); // Initialise la bibliothèque Wire
  lightMeter.begin(BH1750::CONTINUOUS_HIGH_RES_MODE); // Initialise le capteur BH1750
  
  Serial.println(F("BH1750 Test"));
}

void loopBH(float &lux) {
  lux = lightMeter.readLightLevel(); // Lit le niveau de luminosité en lux
  Serial.print("Light: ");
  Serial.print(lux);
  Serial.println(" lx");
}