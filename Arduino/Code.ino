#include <WiFi.h>
#include <HTTPClient.h>
int Prevalue;
const char* ssid = "JARVIS";
const char* password = "12345678";
String id="e9c12f48-ba6c-4679-be86-c450e6f15aa7";
const int trigPin = 13;
const int echoPin = 12;
int Flow = 23;
volatile long pulse;
unsigned long lastTime;
float volume;
//define sound speed in cm/uS
#define SOUND_SPEED 0.034
#define CM_TO_INCH 0.393701

long duration;
float distanceCm;
int sensorPin=32;
int motor1Pin1 = 18; 
int motor1Pin2 = 19; 
int enable1Pin = 21; 
const unsigned long durationx = 3000;
const int numReadings = 300;
// Setting PWM properties
const int freq = 30000;
const int pwmChannel = 0;
const int resolution = 8;
int dutyCycle = 150;
float distanceInch;
int isFlow()
{
  pulse=0;
  delay(1000);
  volume = 2.663 * pulse;
  Serial.print(volume);
  Serial.println(" mL/s");
  if(volume!=0)
  {
    Serial.println("Flow Detected...");
    return 1;
  }
  else
  {
    Serial.println("No Flow Detected...");
    return 0; 
  }
}

int readSensorFor3Seconds() 
{
  unsigned long startTime = millis(); // record the start time
  unsigned long currentTime;
  int sensorReadings[numReadings];
  int index = 0;
  while (millis() - startTime <= durationx && index < numReadings) 
  {
    int sensorValue = digitalRead(sensorPin);
    sensorReadings[index] = sensorValue;
    index++;
    delay(10);
  }
  int m=0;
  int n=0;
  for (int i = 0; i < index; i++) 
  {
    if(sensorReadings[i]==1)
    {
      m++;
    }
    else if(sensorReadings[i]==0)
    {
      n++;
    }
  }
  Serial.println(String(m)+" "+String(n));
  if(m!=0 and n!=0)
  {
    return 1;
  }
  else
  {
    return 0;
  }
}
void increase()
{
  pulse++;
}
int ChangeinPetrol(int Prev)
{
  Serial.println("Previous : "+String(Prev));
  int Temp,Data=Prev;
  int C;
  do{
  delay(1000);
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distanceCm = duration * SOUND_SPEED/2;
  distanceInch = distanceCm * CM_TO_INCH;
  C=Temp-distanceCm;
  Serial.println("Change : "+String(C));
  Temp=C;
  }while(C>=1);
  Serial.println("Start : "+String(Data)+" End : "+String(distanceCm));
  return distanceCm;
}
void SendReq(String URL)
{
  Serial.println(URL);
  HTTPClient http;
  http.begin(URL);
  Serial.print("Sending GET request to: ");
  Serial.println(URL);
  int httpResponseCode = http.GET();
  if (httpResponseCode > 0) 
  {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);

    String payload = http.getString();
    Serial.println("Response: " + payload);
  } 
  else 
  {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }
  http.end();
}
void UpdateLevel()
{
  int Avg=0;
  for(int x=0;x<3;x++)
  {
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    duration = pulseIn(echoPin, HIGH);
    distanceCm = duration * SOUND_SPEED/2;
    distanceInch = distanceCm * CM_TO_INCH;
    Serial.print("Distance (cm): ");
    Serial.println(distanceCm);
    Avg+=distanceCm;
    delay(500);
  }
  String Level=String(Avg/3);
  Serial.println("Change in Level "+String(Prevalue-(Avg/3)));
  if(Prevalue-(Avg/3)>=2)
  {
    Serial.println("Alert Fuel Added");
    Prevalue=ChangeinPetrol((Avg/3));
    Level=Prevalue;
  }
  else
  {
    Prevalue=Avg/3;
  }
  String serverAddress="http://172.16.72.194:3247/fuellevel?vid="+id+"&h="+Level;
  SendReq(serverAddress);
}
void setup() 
{
  Serial.begin(115200); 
  pinMode(trigPin, OUTPUT); 
  pinMode(echoPin, INPUT);
   WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  Serial.println("SettingUpCurrent Value");
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distanceCm = duration * SOUND_SPEED/2;
  distanceInch = distanceCm * CM_TO_INCH;
  Serial.print("Distance (cm): ");
  Serial.println(distanceCm);
  Prevalue=distanceCm;
  attachInterrupt(digitalPinToInterrupt(Flow), increase, RISING);
  pinMode(sensorPin,INPUT);
  digitalWrite(motor1Pin1, HIGH);
  digitalWrite(motor1Pin2, LOW);
  pinMode(motor1Pin1, OUTPUT);
  pinMode(motor1Pin2, OUTPUT);
  pinMode(enable1Pin, OUTPUT);
  ledcSetup(pwmChannel, freq, resolution);
  ledcAttachPin(enable1Pin, pwmChannel);
  ledcWrite(pwmChannel, dutyCycle);
}
void loop() 
{
  UpdateLevel();
  //isFlow();
  if(readSensorFor3Seconds())
  {Serial.println("Engine is On");}
  else
  {
    Serial.println("Engine is Off");
    if(isFlow())
    {
      Serial.println("Fuel Theft....");
    }
    else
    {
      Serial.println("No issues");
    }
  }
  delay(2000);
}