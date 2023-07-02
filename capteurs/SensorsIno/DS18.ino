#include <OneWire.h>
#include <DallasTemperature.h>

#define ONE_WIRE_BUS 27 

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

void setupDS18() {
    sensors.begin();
}

void loopDS18(float &temp_DS18B20) {
    sensors.requestTemperatures();
    temp_DS18B20 = sensors.getTempCByIndex(0);
}
