#include "AHTxx.h"

AHTxx aht10;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("Starting up...");
  while ( aht10.begin() != true) {
    Serial.println("Sensor not running.");
    delay(5000);
  }

  Serial.println("AHT10 running");
  aht10.setCycleMode();
}

void loop() {
  // put your main code here, to run repeatedly:

  // int measurements = 100, counter = 0;
  // bool tester = true;
  
  // float humArr[measurements], tempArr[measurements];

  // while (counter < measurements) { 
  float humidity = aht10.readHumidity(true);
  // humArr[counter] = humidity;
  float temperature = aht10.readTemperature(false);
  // tempArr[counter] = temperature;
  // Serial.println(humArr[counter]);
  // Serial.println(tempArr[counter]);
  // Serial.print("Humidity: ");
  Serial.println(humidity);
  // Serial.print("%  Temperature: ");
  Serial.println(temperature);
  // Serial.println(" C");
  // delay(1200000);
  delay(1000);
  // delay(100);
  // counter++;
  // }
  // Serial.println("Done!");
  

    // Serial.println(counter);
  // counter++;

  // This while loop stops data collection.
  // while (1) {}
}
