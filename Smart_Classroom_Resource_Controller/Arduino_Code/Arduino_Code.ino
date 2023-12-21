#include <EEPROM.h>
#include <DS3231.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd (0x27,16,2);
DS3231 rtc(SDA, SCL);

#include <SoftwareSerial.h> // Serial for nodemcu
SoftwareSerial ns(5,6);
String ip_recieved;

String mycmd;

String hall_1[4];
String hall_2[4];

String sf1_status = "0";
String sf2_status = "0";

String sf_2_read = "0";
String sf_1_read = "0";


int sf1_sensorRest = 0;
int sf2_sensorRest = 0;

int ps_time = 60;

unsigned long prevTime = millis();

Time t;

int timecal = 0;
void setup() {
  
 //rx tx
rtc.begin();

//Pin Configuration RTC Module
//A5 - SCL
//A4 - SDA

//Set Date and Time
//rtc.setDOW(TUESDAY);
//rtc.setDate(12, 12, 2023);
rtc.setTime(7, 50, 30);

Serial.begin(9600);
ns.begin(9600);
pinMode(3,OUTPUT);// SF1 Output
pinMode(4,OUTPUT);// SF2 Output

pinMode(9,INPUT); // SF1 Sensor
pinMode(7,INPUT); // SF2 Sensor


//Initial Print LCD 
 lcd.init();
 lcd.backlight();
 lcd.print("SMART LEC");
 lcd.setCursor(0,1);
 lcd.print("HALL MANAGEMENT");
 delay(1000);
 lcd.clear();

 
 
}



void loop() {


while(Serial.available()==0){ 

////SENSOR READINGS////

  if (digitalRead(9)== HIGH){
    sf_1_read ="1";
    sf1_sensorRest = 0;    
  }
  else{
    sf_1_read ="0";
  }

  if (digitalRead(7)== HIGH){
  sf_2_read ="1";
  sf2_sensorRest = 0;
  }
  
  else{
    sf_2_read ="0";
}

//Getting current time from RTC
  t = rtc.getTime();

  int h = t.hour;
  int m = t.min;
  int s = t.sec;

 
 if (ns.available()>0){
  ip_recieved = ns.readStringUntil("\n");
  //Serial.println(ip_recieved);
  
} 
//Creating pulse once in 0.1 second
 
 unsigned long currentTime = millis();
if (currentTime - prevTime >1000){

 // timecal++;
 // if (timecal == 10){
    sf1_sensorRest++;
    sf2_sensorRest++;
 //   timecal = 0;
 // }
    
  //Serial Prints 
  Serial.print(sf1_status);
  Serial.print(",");
  Serial.print(sf2_status);
  Serial.print(",");
  Serial.print(sf_1_read);
  Serial.print(",");
  Serial.print(sf_2_read);
  Serial.print(",");
  Serial.print(EEPROM.read(8));
  Serial.print(",");
  Serial.print(EEPROM.read(9));
  Serial.print(",");
  Serial.print(EEPROM.read(10));
  Serial.print(",");
  Serial.print(EEPROM.read(11));
  Serial.print(",");
  Serial.print(EEPROM.read(12));
  Serial.print(",");
  Serial.print(EEPROM.read(13));
  Serial.print(",");
  Serial.print(h);
  Serial.print(",");
  Serial.print(m);
  Serial.print(",");
  Serial.print(s);
  
 
  
  //False values for avoid data loose 
  Serial.print(",");
  Serial.print("0");
  Serial.print(",");
  Serial.print("0");
  Serial.print(",");
  Serial.print("0");
  Serial.print(",");
  Serial.print("0");
  Serial.print("\n");
  
 //Serial Prints for NodeMCU 
  ns.print(sf1_status);
  ns.print(":");
  ns.print(sf2_status);
  ns.print(":");
  ns.print(sf_1_read);
  ns.print(":");
  ns.print(sf_2_read);
  ns.print(":");
  ns.print(EEPROM.read(8));
  ns.print(":");
  ns.print(EEPROM.read(9));
  ns.print(":");
  ns.print(EEPROM.read(10));
  ns.print(":");  
  ns.print(EEPROM.read(11));
  ns.print(":");
  ns.print(EEPROM.read(12));
  ns.print(":");
  ns.print(EEPROM.read(13));
  ns.print(":");
  ns.print(sf1_sensorRest);
  ns.print(":");
  ns.print(sf2_sensorRest);
  ns.print(":");


  
 //Timeslots
  ns.print(EEPROM.read(0));
  ns.print(",");
  ns.print(EEPROM.read(1));
  ns.print(",");
  ns.print(EEPROM.read(2));
  ns.print(",");  
  ns.print(EEPROM.read(3));
  ns.print("/");
  ns.print(EEPROM.read(4));
  ns.print(",");
  ns.print(EEPROM.read(5));
  ns.print(",");
  ns.print(EEPROM.read(6));
  ns.print(",");
  ns.print(EEPROM.read(7));
  ns.print("\n");

 //LCD Prints
  lcd.clear();
  lcd.setCursor(4,1);
  lcd.print(h);
  lcd.setCursor(6,1);
  lcd.print(":");
  lcd.setCursor(7,1);
  lcd.print(m);
  lcd.setCursor(9,1);
  lcd.print(":");
  lcd.setCursor(10,1);
  lcd.print(s);
  lcd.setCursor(1,0);
  lcd.print(ip_recieved);

  prevTime = currentTime;
}
  

//--------------- Controlling Outputs ----------------

// status == 0 -> Not active 
// status == 1 -> Active (Lecture Ongoing) 
// status == 2 -> Before Delay (Pre condition)
// status == 3 -> After Delay (Time before automatically switch off)
// status == 4 ->Power saving off



//SF 1 On Time  
  if ( ((EEPROM.read(0)==8)&&((h==8)||(h==9))) || ((EEPROM.read(1)==10)&&((h==10)||(h==11))) || ((EEPROM.read(2)==13)&&((h==13)||(h==14))) ||((EEPROM.read(3)==15)&&((h==15)||(h==16)))   ){

//SF 1 Power Saving 
    if ((EEPROM.read(12) == 1)&&(sf1_sensorRest > ps_time )){

         digitalWrite(3,LOW);
         sf1_status = "4";
         }

    else{
          digitalWrite(3,HIGH);
          sf1_status = "1";
      
         }
   }

else{

  //SF 1 Before Delay
  
  if ( (((h+1) == EEPROM.read(0)) || ((h+1) == EEPROM.read(1)) || ((h+1) == EEPROM.read(2)) || ((h+1) == EEPROM.read(3))) && ((60 - EEPROM.read(8)) <= m ) ){
    digitalWrite(3,HIGH);
    sf1_status = "2";
    }

  //SF 1 After Delay
  else if ( (((h-2) == EEPROM.read(0)) || ((h-2) == EEPROM.read(1)) || ((h-2) == EEPROM.read(2)) || ((h-2) == EEPROM.read(3))) && (EEPROM.read(9) >=  m ) ){
    digitalWrite(3,HIGH);
    sf1_status = "3";
}

//SF 1 No Command
else{
  digitalWrite(3,LOW);
  sf1_status = "0";

}    
}


//Sf 2 On Time 
  if (((EEPROM.read(4)==8)&&((h==8)||(h==9))) || ((EEPROM.read(5)==10)&&((h==10)||(h==11))) || ((EEPROM.read(6)==13)&&((h==13)||(h==14))) ||((EEPROM.read(7)==15)&&((h==15)||(h==16)))){

//Sf 2 Power Saving
    if ((EEPROM.read(13) == 1)&&(sf2_sensorRest > ps_time )){
      digitalWrite(4,LOW);
      sf2_status = "4";
    }

    else{
       digitalWrite(4,HIGH);
       sf2_status = "1";
    }
}


else{

  //Sf 2 Before Delay
  if ( (((h+1) == EEPROM.read(4)) || ((h+1) == EEPROM.read(5)) || ((h+1) == EEPROM.read(6)) || ((h+1) == EEPROM.read(7))) && ((60 - EEPROM.read(10)) <= m ) ){
    digitalWrite(4,HIGH);
    sf2_status = "2";
      
  }

  //Sf 2 After Delay
  else if ( (((h-2) == EEPROM.read(4)) || ((h-2) == EEPROM.read(5)) || ((h-2) == EEPROM.read(6)) || ((h-2) == EEPROM.read(7))) && (EEPROM.read(11) >=  m ) ){
    digitalWrite(4,HIGH);
    sf2_status = "3";
    
  }


  //Sf 2 No Command
else{
  digitalWrite(4,LOW);
  sf2_status = "0";

}
  
}

}

  
 

// If Serial is available (Read Data)

//SF 1 Time Details

hall_1[0] =Serial.readStringUntil(':');
EEPROM.write(0,hall_1[0].toInt());

hall_1[1] =Serial.readStringUntil(':');
EEPROM.write(1,hall_1[1].toInt());

hall_1[2] =Serial.readStringUntil(':');
EEPROM.write(2,hall_1[2].toInt());

hall_1[3] =Serial.readStringUntil(':');
EEPROM.write(3,hall_1[3].toInt());



//Sf 2 Time Details 
hall_2[0] =Serial.readStringUntil(':');
EEPROM.write(4,hall_2[0].toInt());

hall_2[1] =Serial.readStringUntil(':');
EEPROM.write(5,hall_2[1].toInt());

hall_2[2] =Serial.readStringUntil(':');
EEPROM.write(6,hall_2[2].toInt());

hall_2[3] =Serial.readStringUntil(':');
EEPROM.write(7,hall_2[3].toInt());



//Delay Commands 
String before_delaysf1 = Serial.readStringUntil(':');
EEPROM.write(8,before_delaysf1.toInt());

String after_delaysf1 = Serial.readStringUntil(':');
EEPROM.write(9,after_delaysf1.toInt());

String before_delaysf2 = Serial.readStringUntil(':');
EEPROM.write(10,before_delaysf2.toInt());

String after_delaysf2 = Serial.readStringUntil(':');
EEPROM.write(11,after_delaysf2.toInt());

//Power Saving Status 
String ps_statesf1 = Serial.readStringUntil(':');
EEPROM.write(12,ps_statesf1.toInt());

String ps_statesf2 = Serial.readStringUntil('\n');
EEPROM.write(13,ps_statesf2.toInt());

}
