#include <DHT.h>

#include <WiFi.h>
#include <ArduinoJson.h>
#include <FirebaseESP32.h>

const char* WIFI_SSID = "Bbox-32BE8614";
const char* WIFI_PASSWORD = "PcPQPfmPXTqVShDF6F";

String FIREBASE_HOST = "https://autonhome-af7ba-default-rtdb.europe-west1.firebasedatabase.app/";
String FIREBASE_AUTH = "idCrjvKYAhGFV56Yfnx8FbGtEzBDOzDGuvA40v7L";

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

  // Startint DHT
  dht.begin();
  delay(2000); 
}

void sendDataToFirebase(float temperature, float humidity){
  FirebaseJson jsonDoc;
  jsonDoc.set("temperature", temperature);
  jsonDoc.set("humidity", humidity);

  String path = "/air_monitoring";
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
