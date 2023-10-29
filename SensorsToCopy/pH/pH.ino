int pHPin = A0; // Broche pour le pH-mètre (Analogique)
// int tempPin = A1; // Broche pour le capteur de température (Analogique)

void setup() {
  Serial.begin(115200); // Vitesse de la communication série à 115200 bauds pour l'Arduino
}

void loop() {
  int rawPhValue = analogRead(pHPin); // Lecture de la valeur analogique pour le pH
  float voltagePh = rawPhValue * (5.0 / 1023.0); // Conversion en tension (5V comme tension de référence)

  // int rawTempValue = analogRead(tempPin); // Lecture de la valeur analogique pour la température
  // float voltageTemp = rawTempValue * (5.0 / 1023.0); // Conversion en tension (5V comme tension de référence)

  Serial.print("PH_Voltage=");
  Serial.println(voltagePh, 4); // Envoie la tension avec 4 décimales à l'ESP via Serial

  // Serial.print("Voltage de la température: ");
  // Serial.println(voltageTemp, 2); // Affiche la tension de la température avec 2 chiffres après la virgule
  
  Serial.println("------------------------");
  Serial.println(" ");
  delay(3000); // Délai de 2 secondes avant la prochaine lecture
}

