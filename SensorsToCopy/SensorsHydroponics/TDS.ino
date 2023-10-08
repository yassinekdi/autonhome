const int TDS_PIN = 33;  // Connect the TDS sensor to IO33

void setupTDS() {
  analogReadResolution(12); // Set the analog read resolution to 12 bits
}

void loopTDS(float &tdsValue) {
  int tdsRawValue = analogRead(TDS_PIN);  // Read the raw value from the TDS sensor
  tdsValue = (tdsRawValue / 4095.0) * 3.3; // Convert the raw value to voltage
  
  // Serial.print("TDS Raw Value: ");
  // Serial.print(tdsRawValue);
  // Serial.print("\tTDS Value in Voltage: ");
  // Serial.println(tdsValue, 4); // Print with 4 decimal places
}
