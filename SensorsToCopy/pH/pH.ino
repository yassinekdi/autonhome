int pHPin = A0; // Broche pour le pH-mètre (Analogique)
// int tempPin = A1; // Broche pour le capteur de température (Analogique)

float a = -5.165; // Exemple de coefficient a
float b = 27.632; // Exemple de coefficient b

void setup() {
  Serial.begin(115200); // Vitesse de la communication série à 115200 bauds pour l'Arduino
}

void loop() {
  int rawPhValue = analogRead(pHPin); // Lecture de la valeur analogique pour le pH
  float voltagePh = rawPhValue * (5.0 / 1023.0); // Conversion en tension (5V comme tension de référence)
  float phValue = a * voltagePh + b; // Conversion de la tension en pH en utilisant l'équation de la droite
  
  Serial.print("PH_Voltage=");
  Serial.println(phValue);

  // Serial.print("Voltage de la température: ");
  // Serial.println(voltageTemp, 2); // Affiche la tension de la température avec 2 chiffres après la virgule
  
  Serial.println("------------------------");
  Serial.println(" ");
  delay(3000); // Délai de 2 secondes avant la prochaine lecture
}

