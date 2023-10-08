#include <WiFi.h>
#include <ArduinoJson.h>
#include <FirebaseESP32.h>
#include <time.h>

unsigned long startTime;

// INO VARIABLES -------------------
const char* WIFI_SSID = "";
const char* WIFI_PASSWORD = "";
String FIREBASE_HOST = "";
String FIREBASE_AUTH = "";
String UserId = "";
// INO VARIABLES -------------------

FirebaseData firebaseData;

void sendDataToFirebase(float value, String measure_type, String section, String sensor){
  FirebaseJson jsonDoc;
  jsonDoc.set(measure_type, value);
  jsonDoc.set("timestamp", time(nullptr));  // Add current timestamp

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
    startTime = millis();
    setupCMS();
    setupDHT();
    delay(1000);
    Serial.println(" ");

    // Connexion WiFi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected");

  // Connexion à Firebase
  Firebase.begin(FIREBASE_HOST,FIREBASE_AUTH);
  // Configuring time
  configTime(0, 0, "pool.ntp.org");  // Configure NTP
  delay(1000);
}

void loop() {
    float humidity_CMS4, humidity_CMS1;
    loopCMS(humidity_CMS4, humidity_CMS1);

    // unsigned long currentTime = (millis() - startTime) / 1000;
    // Serial.print("Temps (sec) : ");
    // Serial.print(currentTime);
    // Serial.print(", Valeur CMS 4 : ");
    // Serial.println(humidity_CMS4);
    sendDataToFirebase(humidity_CMS4, "humidity", "POT1", "CMS4");
    // Serial.print(", Valeur CMS 1 : "); 
    // Serial.println(humidity_CMS1);
    sendDataToFirebase(humidity_CMS1, "humidity", "POT2", "CMS5");

    float temp_dht, humidity_dht;
    loopDHT(temp_dht, humidity_dht);

    // Serial.println(" ");
    // Serial.print("Temp DHT22: ");
    // Serial.print(temp_dht);
    // Serial.println(" C ");
    sendDataToFirebase(temp_dht, "temperature", "AIR", "DHT22");

    // Serial.print("Humidity DHT22 : ");
    // Serial.print(humidity_dht);
    // Serial.println(" % ");
    sendDataToFirebase(humidity_dht, "humidity", "AIR", "DHT22");

    delay(900000);
}
