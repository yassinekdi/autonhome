#include <DHT.h>

#define DHT_PIN 27
DHT dht(DHT_PIN, DHT22);

void setupDHT() {
    dht.begin();
}

void loopDHT(float &temp_dht, float &humidity_dht) {
    temp_dht = dht.readTemperature();
    humidity_dht = dht.readHumidity();

    // Serial.print("temp dht : ");
    // Serial.println(temp_dht);
    // Serial.print("humidity dht : ");
    // Serial.println(humidity_dht);
}
