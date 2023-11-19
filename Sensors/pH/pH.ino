int pHPin = A0; // Broche pour le pH-mètre (Analogique)

// Coefficients de l'équation de la droite trouvés après calibration
// pH = a * tension + b
float a = -5.165; // Exemple de coefficient a
float b = 27.632; // Exemple de coefficient b

void setup() {
  Serial.begin(115200); // Vitesse de la communication série à 115200 bauds pour l'Arduino
}

void loop() {
  int rawPhValue = analogRead(pHPin); // Lecture de la valeur analogique pour le pH
  float voltagePh = rawPhValue * (5.0 / 1023.0); // Conversion en tension (5V comme tension de référence)
  float phValue = a * voltagePh + b; // Conversion de la tension en pH en utilisant l'équation de la droite
  
  // Serial.print("rawPhValue=");
  // Serial.print(rawPhValue); // Affiche la valeur brute lue par l'Arduino
  // Serial.print(", Voltage=");
  // Serial.print(voltagePh); // Affiche la tension calculée
  Serial.print("pH=");
  Serial.println(phValue); // Affiche la valeur de pH calculée
  
  delay(2000); // Délai de 2 secondes avant la prochaine lecture
}
