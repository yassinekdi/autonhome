#include <WiFi.h>
#include <ArduinoJson.h>
#include <FirebaseESP32.h>
#include <time.h>

// INO VARIABLES -------------------
const char* WIFI_SSID = "";
const char* WIFI_PASSWORD = "";
String FIREBASE_HOST = "";
String FIREBASE_AUTH = "";
String UserId = "";
// INO VARIABLES -------------------

FirebaseData firebaseData;

void sendDataToFirebase(float value, String measure_type, String section, String sensor) {
  FirebaseJson jsonDoc;
  jsonDoc.set(measure_type, value);
  jsonDoc.set("timestamp", time(nullptr));

  String path = "/" + UserId + "/" + section + "/" + sensor;
  if (Firebase.pushJSON(firebaseData, path, jsonDoc)) {
    Serial.println("Data sent to Firebase");
  } else {
    Serial.println("Failed to send data to Firebase");
    Serial.println(firebaseData.errorReason());
  }
}

void setup() {
  Serial.begin(115200);
  setupDHT();
  setupTDS();
  setupBH();
  
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected");

  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  configTime(0, 0, "pool.ntp.org");
  delay(1000);
}

void loop() {
  // For DHT ----------------------------
  float temp_dht, humidity_dht;
  loopDHT(temp_dht, humidity_dht);
  sendDataToFirebase(temp_dht, "temperature", "AIR", "DHT22");
  sendDataToFirebase(humidity_dht, "humidity", "AIR", "DHT22");

  // For TDS ----------------------------
  float tdsValue;
  loopTDS(tdsValue);
  sendDataToFirebase(tdsValue, "tds", "EAU", "TDS");

  // For BH ----------------------------
  float lux;
  loopBH(lux);
  Serial.println("");
  sendDataToFirebase(lux, "luminosity", "AIR", "BH1750");

  // For PH ----------------------------
  if(Serial.available() > 0) { // Vérifie si des données sont disponibles pour être lues depuis le port série
    String pH_data = Serial.readStringUntil('\n'); // Lit la ligne jusqu'à ce qu'un saut de ligne soit reçu

    // Ici, je pars le String pour obtenir uniquement la valeur numérique. Cela suppose que l'Arduino envoie "PH_Voltage=xxx"
    if (pH_data.startsWith("PH_Voltage=")) {
      float pH_voltage = pH_data.substring(11).toFloat();
      Serial.print("PH voltage ESP part : ");
      Serial.println(pH_voltage, 4);
      sendDataToFirebase(pH_voltage, "pH", "EAU", "pH");
    }
  }
  // delay(900000); // Wait for 15 minutes before taking another set of measurements
  delay(3000);
}
