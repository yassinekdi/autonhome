int pHPin = 34; // Broche pour le pH-mètre
int temperaturePin = 35; // Broche pour le capteur de température

void setup() {
  Serial.begin(115200);
  analogReadResolution(12); // 12 bits de résolution pour l'ESP32
}

void loop() {
  int rawPhValue = analogRead(pHPin);
  float voltage = rawPhValue * (3.3 / 4095.0); // Conversion en tension
  Serial.print("Voltage du pH: ");
  Serial.println(voltage, 2);

  // int rawTempValue = analogRead(temperaturePin);
  // float tempVoltage = rawTempValue * (3.3 / 4095.0); // Conversion en tension
  // Serial.print("Voltage de la température: ");
  // Serial.println(tempVoltage, 2);

  Serial.println("------------------------");
  delay(2000);
}
