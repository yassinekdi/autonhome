#include <DHT.h>
#include <WiFi.h>
#include <ArduinoJson.h>
#include <FirebaseESP32.h>
#include <time.h>

const char* WIFI_SSID = "";
const char* WIFI_PASSWORD = "";

String FIREBASE_HOST = "";
String FIREBASE_AUTH = "";

FirebaseData firebaseData;
DHT dht(33, DHT22);

void setup() {
  Serial.begin(115200);
  delay(1000);

  // Connexion WiFi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected");

  // Connexion à Firebase
  Firebase.begin(FIREBASE_HOST,FIREBASE_AUTH);

  // Starting DHT
  dht.begin();
  delay(2000); 

  // Configuring time
  configTime(0, 0, "pool.ntp.org");  // Configure NTP
  delay(1000);
}

void sendDataToFirebase(float temperature, float humidity){
  FirebaseJson jsonDoc;
  jsonDoc.set("temperature", temperature);
  jsonDoc.set("humidity", humidity);
  jsonDoc.set("timestamp", time(nullptr));  // Add current timestamp

  String path = "/air_monitoring/DHT22";
  if (Firebase.pushJSON(firebaseData, path, jsonDoc)) {
    Serial.println("Data sent to Firebase");
  } else {
    Serial.println("Failed to send data to Firebase");
    Serial.println(firebaseData.errorReason());
  }
}

void loop() {
  
  float temp = dht.readTemperature();
  float humidity = dht.readHumidity();

  Serial.println(" ");
  Serial.print("Temp: ");
  Serial.print(temp);
  Serial.println(" C ");

  Serial.print("Humidity : ");
  Serial.print(humidity);
  Serial.println(" % ");

  sendDataToFirebase(temp,humidity);

  delay(10000);
}
