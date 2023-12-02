
String mycmd;
String hall_1[4];
String hall_2[4];

void setup() {
Serial.begin(9600);
pinMode(3,OUTPUT);
pinMode(4,OUTPUT);
}

void loop() {
while(Serial.available()==0){ 
  if ((hall_1[0]=="1")||(hall_1[1]=="1")||(hall_1[2]=="1")||(hall_1[3]=="1")){
  digitalWrite(3,HIGH);
  
}
else{
  digitalWrite(3,LOW);
}

  if ((hall_2[0]=="1")||(hall_2[1]=="1")||(hall_2[2]=="1")||(hall_2[3]=="1")){
  digitalWrite(4,HIGH);
  
}
else{
  digitalWrite(4,LOW);
}
}
hall_1[0] =Serial.readStringUntil(':');
hall_1[1] =Serial.readStringUntil(':');
hall_1[2] =Serial.readStringUntil(':');
hall_1[3] =Serial.readStringUntil(':');
hall_2[0] =Serial.readStringUntil(':');
hall_2[1] =Serial.readStringUntil(':');
hall_2[2] =Serial.readStringUntil(':');
hall_2[3] =Serial.readStringUntil('\r');


  if ((hall_1[0]=="1")||(hall_1[1]=="1")||(hall_1[2]=="1")||(hall_1[3]=="1")){
  digitalWrite(3,HIGH);
  
}
else{
  digitalWrite(3,LOW);
}
}
