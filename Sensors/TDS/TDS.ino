// Pin Configuration
const int TDS_PIN = 33;  // Connect the TDS sensor to IO34

void setup() {
  // Initialize Serial Monitor
  Serial.begin(115200);
  
  // Configure the ADC
  analogReadResolution(12); // Set the analog read resolution to 12 bits
}

void loop() {
  int tdsRawValue = analogRead(TDS_PIN);  // Read the raw value from the TDS sensor
  float tdsValue = (tdsRawValue / 4095.0) * 3.3; // Convert the raw value to voltage
  
  // Print the values to Serial Monitor
  Serial.print("TDS Raw Value: ");
  Serial.print(tdsRawValue);
  Serial.print("\tTDS Value in Voltage: ");
  Serial.println(tdsValue, 4); // Print with 4 decimal places
  
  delay(2000); // Wait for 2 seconds before reading again
}
