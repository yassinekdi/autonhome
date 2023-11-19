const int TDS_PIN = 33;  // Connect the TDS sensor to IO33

void setupTDS() {
  analogReadResolution(12); // Set the analog read resolution to 12 bits
}

void loopTDS(float &tdsValue) {
  float calibration_factor = 0.895;
  tdsValue = analogRead(TDS_PIN)*calibration_factor;  // Read the raw value from the TDS sensor

  Serial.print("TDS Value: ");
  Serial.println(tdsValue); 
}
