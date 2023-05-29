#define AOUT_PIN 33
unsigned long startTime;


const char* WIFI_SSID = "";
const char* WIFI_PASSWORD = "";

String FIREBASE_HOST = "";
String FIREBASE_AUTH = "";
String UserId = "";

void setup() {
  Serial.begin(115200);
  startTime = millis();
  delay(1000);
  Serial.println(" ");
}

void loop() {
  int value= analogRead(AOUT_PIN);
  float humidity = ((value - 3490) / (1584.7 - 3490)) * 100;
  humidity = constrain(humidity, 0, 100);
  unsigned long currentTime = (millis() - startTime) / 1000;
  Serial.print("Temps (sec) : ");
  Serial.print(currentTime);
  // Serial.print(", Humidité: ");
  // Serial.print(humidity);
  // Serial.print(" %");
  Serial.print(", Valeur: ");
  Serial.println(value);

  delay(1000);
}
