#include <WiFi.h>
#include <WebServer.h>
#include <Arduino.h>
#include <Servo.h>

const char* ssid = "";
const char* password = "";


WebServer server(80); 
Servo yaw;
Servo pitch;

int pitchpin = 18; 
int yawpin = 4; 
int relaypin = 5; 

void firegobrrr(){ // get fire s
  server.send(200, "text/html", "Firing command OK");
  Serial.println("Firing rocket"); 
  digitalWrite(relaypin,HIGH);
  digitalWrite(2,HIGH);
}

void keepaliveCON(){
  server.send(200,"text/html", "ESP online");
}

void resetrelay(){
  digitalWrite(relaypin,LOW);
  server.send(200,"text/html","Relaypin reset successfully");
}

void movement(){
    if (server.hasArg("plain")) {
      server.send(200,"text/plain","OK");
      String mousecordinates = server.arg("plain");
      int comma = mousecordinates.indexOf(','); 
      String y = mousecordinates.substring(0, comma); 
      String x = mousecordinates.substring(comma + 1);
      yaw.write(y.toInt());
      pitch.write(x.toInt()); 
 
  }
}

void setup() {
  pinMode(2,OUTPUT);
  pinMode(relaypin,OUTPUT);
  yaw.attach(yawpin);
  digitalWrite(relaypin,LOW);

  pitch.attach(pitchpin);
  Serial.begin(9600);
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    digitalWrite(2,LOW);
    delay(500);
    Serial.println("Awaiting wifi connection . .  ");
    digitalWrite(2,HIGH);
  }
  Serial.println("WiFi connected.");
  digitalWrite(2,HIGH);
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP()); 
  server.begin(); 
  server.on("/firerocket/",firegobrrr); 
  server.on("/movpos/",HTTP_POST,movement); 
  server.on("/resetrelay/",resetrelay); 
  Serial.println("Server started");
}

void loop() {server.handleClient();}


