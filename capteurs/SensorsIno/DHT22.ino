#include <DHT.h>

#define DHT_PIN 25
DHT dht(DHT_PIN, DHT22);

void setupDHT() {
    dht.begin();
}

void loopDHT(float &temp_dht, float &humidity_dht) {
    temp_dht = dht.readTemperature();
    humidity_dht = dht.readHumidity();
}
