#define AOUT_PIN 33
unsigned long startTime;


const char* WIFI_SSID = "Bbox-32BE8614";
const char* WIFI_PASSWORD = "PcPQPfmPXTqVShDF6F";

String FIREBASE_HOST = "https://autonhome-af7ba-default-rtdb.europe-west1.firebasedatabase.app/";
String FIREBASE_AUTH = "idCrjvKYAhGFV56Yfnx8FbGtEzBDOzDGuvA40v7L";
String UserId = "8";

void setup() {
  Serial.begin(115200);
  startTime = millis();
  delay(1000);
  Serial.println(" ");
}

void loop() {
  int value= analogRead(AOUT_PIN);
  float humidity = ((value - 3413.4) / (1584.7 - 3413.4)) * 100;
  humidity = constrain(humidity, 0, 100);
  unsigned long currentTime = (millis() - startTime) / 1000;
  Serial.print("Temps (sec) : ");
  Serial.print(currentTime);
  Serial.print(", Humidité: ");
  Serial.print(humidity);
  Serial.println(" %");
  // Serial.print(", Valeur: ");
  // Serial.println(value);

  delay(1000);
}
