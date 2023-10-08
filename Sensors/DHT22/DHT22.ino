#include <DHT.h>

DHT dht(27, DHT22);

void setup() {
  Serial.begin(115200);
  delay(1000);

  // Startint DHT
  dht.begin();
  delay(2000); 
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

  delay(1000);
}