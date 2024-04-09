'''
#include <WiFi.h>
#include <HTTPClient.h>


#include <DHT.h>
#define DHTPIN 15
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);



const char* ssid = "Wokwi-GUEST"; // Your WiFi SSID
const char* password = ""; // Your WiFi password

String baseURL = "https://api.thingspeak.com/update?api_key=87JIILFZ88HY6E9D&field1=";
String field2 = "&field2=";
String tempData = "0";
String humData = "0";

float tempdataval = 0;
float humdataval = 0;


void connectToWiFi() {
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting...");
  }
  Serial.println("Connected to WiFi");
}

void makeGETRequest() {
  tempData = String(tempdataval);
  humData  = String(humdataval);

  String url = baseURL + tempData + field2 + humData;

  Serial.print("Sending GET request to: ");Serial.println(url);


  HTTPClient http;
  http.begin(url); // Specify the URL here

  int httpCode = http.GET();
  
  if (httpCode > 0) {
    Serial.printf("[HTTP] GET... code: %d\n", httpCode);
    if (httpCode == HTTP_CODE_OK) {
      String payload = http.getString();
      Serial.println(payload);
    }
  } else {
    Serial.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
  }

  http.end();
}

void setup() {
  Serial.begin(115200);
  delay(500);

  Serial.println("Upload the DHT22 Data on the Thingspeak Server !!!");
  dht.begin();
  delay(1000);
  
  connectToWiFi();
}

void loop() {

  tempdataval = dht.readTemperature();
  humdataval  = dht.readHumidity();
  
  if (isnan(tempdataval) || isnan(humdataval)) {Serial.println("Failed to read from DHT sensor!");return;}

  String message = "Weather   temp:  " + String(tempdataval) + "    humidity:  " + String(humdataval);
  Serial.println(message);
  delay(500);







  // Make the URL request
  makeGETRequest();
  
  // Wait for some time before making the next request
  delay(20000);         // 1 minute delay (60000)
}


'''