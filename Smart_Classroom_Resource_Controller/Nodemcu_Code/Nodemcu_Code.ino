#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <WebSocketsServer.h>
#include <SoftwareSerial.h>
SoftwareSerial ns (4,5); //rx tx

String ipString;

const char *ssid = "Dialog 4G 411";
const char *password = "3D80B4bF";


AsyncWebServer server(80);
WebSocketsServer websockets(81);



String status_sf1;
String status_sf2;
String read_sf1;
String read_sf2;
String before_delaysf1;
String after_delaysf1;
String before_delaysf2;
String after_delaysf2;
String ps_statesf1;
String ps_statesf2;
String sf1_sensorRest;
String sf2_sensorRest;
String sf1_timeslots;
String sf2_timeslots;

void notFound(AsyncWebServerRequest *request)
{
  request->send(404, "text/plain", "Page Not found");
}


void webSocketEvent(uint8_t num, WStype_t type, uint8_t * payload, size_t length) {

  switch (type) 
  {
    case WStype_DISCONNECTED:
      Serial.printf("[%u] Disconnected!\n", num);
      break;
    case WStype_CONNECTED: {
        IPAddress ip = websockets.remoteIP(num);
        Serial.printf("[%u] Connected from %d.%d.%d.%d url: %s\n", num, ip[0], ip[1], ip[2], ip[3], payload);

        // send message to client
        websockets.sendTXT(num, "Connected from server");
      }
      break;
    case WStype_TEXT:
     // Serial.printf("[%u] get Text: %s\n", num, payload);
      String message = String((char*)( payload));
      //Serial.println(message);
      //If any value recieves, they will be here
  }
}



String dynamicLabelValue = "Initial Label Value";

void handleRoot(AsyncWebServerRequest *request) {
    request->send(200, "text/html", R"(
<!DOCTYPE html>
<html lang="en">
<head> 
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Classroom Resource Management System</title>


    <script>

        var connection = new WebSocket('ws://'+location.hostname+':81/');

        connection.onmessage = function(event){
  
  var full_data = event.data;
  console.log(full_data);
  var data = JSON.parse(full_data);
  
  var sf1_status_data = data.sf1_status;
  var sf2_status_data = data.sf2_status;

  status(sf1_status_data,"sf1_status");
  status(sf2_status_data,"sf2_status");

  var sf1_sRead_data = data.sf1_read;
  var sf2_sRead_data = data.sf2_read;

  var sf1_sRest_data = data.sf1_sRest;
  var sf2_sRest_data = data.sf2_sRest;
  
  sensorReading(sf1_sRead_data,"sf1_sensor",sf1_sRest_data);
  sensorReading(sf2_sRead_data,"sf2_sensor",sf2_sRest_data);

  valueset("_label_sf1_beforeDelay",data.sf1_beforeDelay,"Before Delay : ");
  valueset("_label_sf1_afterDelay",data.sf1_afterDelay, "After Delay : ");
  ps_state("_label_sf1_ps",data.sf1_psState);
  
  
  valueset("_label_sf2_beforeDelay",data.sf2_beforeDelay,"Before Delay : ");
  valueset("_label_sf2_afterDelay",data.sf2_afterDelay,"After Delay : ");
  ps_state("_label_sf2_ps",data.sf2_psState);


  timeslots(data.sf1_timeslots,"sf1");
  timeslots(data.sf2_timeslots,"sf2");


  }
  
  function timeslots (dataset,lechall){

    if (lechall == "sf1"){

           var numb;
            for( numb = 0; numb < 4; numb++) {
                var label = "status"+numb;
                
                if (dataset[numb] > 0){
                    document.getElementById(label).innerHTML = "Occupied";
                    var myLabel = document.getElementById(label);
                    myLabel.style.backgroundColor = "red";
                }
                else{                    
                    document.getElementById(label).innerHTML = "Not Occupied";
                      var myLabel = document.getElementById(label);
                      myLabel.style.backgroundColor = "green";
                }
                
            }

    }

    if (lechall == "sf2"){

   var numb;
     for( numb = 0; numb < 4; numb++) {
         var temp = numb + 4
         var label = "status"+temp;
         
         if (dataset[numb] > 0){
             document.getElementById(label).innerHTML = "Occupied";
                         var myLabel = document.getElementById(label);
                          myLabel.style.backgroundColor = "red";
         }
         else{                    
             document.getElementById(label).innerHTML = "Not Occupied";
                         var myLabel = document.getElementById(label);
                          myLabel.style.backgroundColor = "green";
         }
         
     }

}
 
  }
  function sensorReading(sensordata,label,restTime){
    if (sensordata == 1){
        document.getElementById(label).innerHTML  = "Detected";
         var myLabel = document.getElementById(label);
         myLabel.style.backgroundColor = "green";
        
    }
    if (sensordata == 0){
        document.getElementById(label).innerHTML  = "Last detected "+restTime+" seconds ago!";
           var myLabel = document.getElementById(label);
         myLabel.style.backgroundColor = "red";
        
    }
  }

  function status(data,label){
    if (data == 0){
        document.getElementById(label).innerHTML  = "Inactive";
         var myLabel = document.getElementById(label);
         myLabel.style.backgroundColor = "red";
    }
    else if (data == 1){
        document.getElementById(label).innerHTML  = "Active";
        var myLabel = document.getElementById(label);
         myLabel.style.backgroundColor = "green";

    }

    else if (data == 2){
        document.getElementById(label).innerHTML  = "Pre Conditioning";
         var myLabel = document.getElementById(label);
         myLabel.style.backgroundColor = "Indigo";
    }

    else if (data == 3){
        document.getElementById(label).innerHTML  = "Post Active Delay";
        var myLabel = document.getElementById(label);
         myLabel.style.backgroundColor = "Indigo";
    }

    else if (data == 4){
        document.getElementById(label).innerHTML  = "Power Saving Off";
        var myLabel = document.getElementById(label);
         myLabel.style.backgroundColor = "MediumBlue";
    }
  }

  function valueset(label,data,msg){
    document.getElementById(label).innerHTML  = msg+data;
  }

  function ps_state(label,data){
    if (data == 0){
        document.getElementById(label).innerHTML  = "Power Saving Off";
         var myLabel = document.getElementById(label);
         myLabel.style.backgroundColor = "red";


    }
    if (data == 1){
        document.getElementById(label).innerHTML  = "Power Saving On"
         var myLabel = document.getElementById(label);
         myLabel.style.backgroundColor = "green";

    
  } 
 }
        
        </script>



</head>
<style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
  
    body {
      font-family: 'Arial', sans-serif;
      background-color: rgb(161, 161, 159);
      display: flex;
    }
  
    .container {
      border: solid 3px #333;
      margin: 5% auto;
      max-width: 90%;
      width: 66%;
      background-color: #f3f3f3;
      border-radius: 14px;
      box-shadow: 0 0 10px #000000;
    }
  
    .ctrlpnl {
        width: fit-content;
        margin-left: 35%;
        padding: 20px;
        background-color: #2b1130;
        color: #ffffff;
        border-radius: 10px;
    }
  
    .sflivstat {
      display: inline-flex;
      width: 45%;
      margin: 20px;
      background-color: rgb(161, 161, 159);
      border: solid 2px #000000;
      border-radius: 10px;
      box-sizing: border-box;
      box-shadow: 0 0 10px rgba(248, 247, 247, 0.5);
    }
    
    .sfhead{
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
        border-radius: 5px;
        padding-left: 10px;
        padding-right: 10px;
        margin-top: 5px;
        background-color: rgb(230, 228, 228);
        margin-left: 140px;
        color: #000000;
    }
    .delay {
        width: 100%;
        border-radius: 10px;
  margin-top: 50px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
  background: linear-gradient(to bottom , rgb(161, 161, 159),rgb(161, 161, 159));
}

/*   
    .timeslot label {
      margin-left: 40px;
    } */
.st{
    margin-left: 60px;
    margin-right: 20px;
    color: #000000;
    font-weight: 700;
   /* text-shadow: 1px 1px 1px #000000, -1px -1px 1px #000000, 1px -1px 1px #000000, -1px 1px 1px #000000;*/
}
  
    .slot {
      font-weight: 700;
      margin-left: 17%;
      color: #000000;
      
      
    }
  
    table {
      width: 100%;
    }
  
    td {
      padding: 10px;
    }
    
    .stat label{
      /*  margin-left: 10px;*/
        color: rgb(0, 0, 0);
        font-weight: 700;
        /*text-shadow: 1px 1px 1px #534e4e, -1px -1px 1px #524d4d, 1px -1px 1px #4e4a4a, -1px 1px 1px #4d4848;*/
    }
    .timeslot td{
        border: 2px solid #000000;
    }

    @media only screen and (max-width: 600px) {
      .container {
        width: 90%;
      }
    /*  .ctrlpnl {
        margin-left: 18%;
    }
  */
      .sflivstat {
        width: 90%;
        margin-top: 25px;
      }
      .sfhead{
        left: 10%;
      }
      .st{
            margin-left: 10px;
      }
      .delay {
        width: 100%;
      }
  
      td {
        padding-top: 10px;
      }
      .slot {

      margin-left: 7%;

    }
  
    }
  </style>
  

<body>
    <div class="container">
    <h1 class="ctrlpnl">Control Panel</h1>
    <div class="sflivstat" >
        <h1 class="sfhead" style="position: absolute;" >SF-1</h1>
        <div class="delay">
            <table class="timeslot">
                <tr>
                    <td>
                        <label class="slot" for="status">08.00 - 10.00  </label>
                        <label id="status0" class="st">Occupied</label>
                    </td>
                </tr>
                <tr>
                    <td>
                        <label class="slot"  for="status">10.00 - 12.00  </label>
                        <label  id="status1" class="st">Occupied</label>
                    </td>
                </tr>
                <tr>
                    <td>
                        <label class="slot"  for="status">13.00 - 15.00  </label>
                        <label  id="status2" class="st">Occupied</label>
                    </td>
                </tr>
                <tr>
                    <td>
                        <label class="slot"  for="status">15.00 - 17.00  </label>
                        <label id="status3" class="st">Occupied</label>
                    </td>
                </tr>
            </table>

            <div style="margin-left: 15%;">
                <table class="stat"  >

                    <tr>
                        <td ><label for="" id ="sf1_status">Inactive</label></td>
                        
                    </tr>

                    <tr>
                            <td><label for="" id = "sf1_sensor">Motion Detected</label></td>
                    </tr>
                    <tr>
                        <td>
                            <label for="stat" id = "_label_sf1_beforeDelay">Before Delay: </label>
                            <label style="margin-left: 27px;"  id="stat"></label>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <label  for="stat" id = "_label_sf1_afterDelay">After Delay: </label>
                            <label style="margin-left: 40px;"    id="stat"></label>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <label  for="stat" id = "_label_sf1_ps">Power Saving: </label>
                            <label style="margin-left: 20px;"   id="stat"></label>
                        </td>
                    </tr>

                </table>                
            </div>
        </div>    
    </div>
    
    <div class="sflivstat" >
        <h1 class="sfhead" style="position: absolute;" >SF-2</h1>
        <div class="delay">
            <table class="timeslot">
                <tr>
                    <td >
                        <label class="slot" for="status">08.00 - 10.00  </label>
                        <label id="status4" class="st">Occupied</label>
                    </td>
                </tr>
                <tr>
                    <td>
                        <label class="slot"  for="status">10.00 - 12.00  </label>
                        <label  id="status5" class="st">Occupied</label>
                    </td>
                </tr>
                <tr>
                    <td>
                        <label class="slot"  for="status">13.00 - 15.00  </label>
                        <label  id="status6" class="st">Occupied</label>
                    </td>
                </tr>
                <tr>
                    <td>
                        <label class="slot"  for="status">15.00 - 17.00  </label>
                        <label id="status7" class="st">Occupied</label>
                    </td>
                </tr>
            </table>

            <div style="margin-left: 15%;">
                <table class="stat"  >

                    <tr>
                        <td ><label  for="" id ="sf2_status">Inactive</label></td>
                        
                    </tr>

                    <tr>
                            <td><label  for="" id = "sf2_sensor">Motion Detected</label></td>
                    </tr>
                    <tr>
                        <td>
                            <label for="stat" id = "_label_sf2_beforeDelay">Before Delay: </label>
                            <label style="margin-left: 27px;"  id="stat"></label>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <label  for="stat" id = "_label_sf2_afterDelay">After Delay: </label>
                            <label style="margin-left: 40px;"    id="stat"></label>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <label  for="stat" id = "_label_sf2_ps">Power Saving: </label>
                            <label style="margin-left: 20px;"   id="stat"></label>
                        </td>
                    </tr>

                </table>                
            </div>
        </div>    
    </div>

            
</div>

</body>
</html>
    )");
}

void handleGetLabelValue(AsyncWebServerRequest *request) {
    request->send(200, "text/plain", dynamicLabelValue);
}

void setup() {
    Serial.begin(9600);
    ns.begin(9600);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
        
    }

    Serial.println("Connected to WiFi");
    Serial.println(WiFi.localIP());
    IPAddress ip = WiFi.localIP();
    ipString = ip.toString();

   
    server.on("/", HTTP_GET, handleRoot);
//    server.on("/getLabelValue", HTTP_GET, handleGetLabelValue);

    server.begin();
    websockets.begin();
    websockets.onEvent(webSocketEvent);

}

void loop() {
  websockets.loop();
         
  if (ns.available()>0){

status_sf1 = ns.readStringUntil(':');
//EEPROM.write(8,before_delaysf1.toInt());

status_sf2 = ns.readStringUntil(':');
//EEPROM.write(9,after_delaysf1.toInt());


read_sf1 = ns.readStringUntil(':');
//EEPROM.write(8,before_delaysf1.toInt());

read_sf2 = ns.readStringUntil(':');
//EEPROM.write(9,after_delaysf1.toInt());

//Delay Commands 
before_delaysf1 = ns.readStringUntil(':');
//EEPROM.write(8,before_delaysf1.toInt());

after_delaysf1 = ns.readStringUntil(':');
//EEPROM.write(9,after_delaysf1.toInt());

before_delaysf2 = ns.readStringUntil(':');
//EEPROM.write(10,before_delaysf2.toInt());

after_delaysf2 = ns.readStringUntil(':');
//EEPROM.write(11,after_delaysf2.toInt());

//Power Saving Status 
ps_statesf1 = ns.readStringUntil(':');
//EEPROM.write(12,ps_statesf1.toInt());

ps_statesf2 = ns.readStringUntil(':');
//EEPROM.write(13,ps_statesf2.toInt());

sf1_sensorRest = ns.readStringUntil(':');
//EEPROM.write(12,ps_statesf1.toInt());

sf2_sensorRest = ns.readStringUntil(':');

sf1_timeslots = ns.readStringUntil('/');

sf2_timeslots = ns.readStringUntil('\n');
//buffer[] = ns.readStringUntil('\n');


//Serial.print(status_sf1);
//Serial.print(status_sf2);
//Serial.print(read_sf1);
//Serial.print(read_sf2);
//Serial.print(before_delaysf1);
//Serial.print(after_delaysf1);
//Serial.print(before_delaysf2);
//Serial.print(after_delaysf2);
//Serial.print(ps_statesf1);
//Serial.print(ps_statesf2);
//Serial.print(sf1_timeslots);
//Serial.print(sf2_timeslots);
//Serial.print("\n");




   
  String JSON_Data = "{\"sf1_status\":";
         JSON_Data += status_sf1;
         JSON_Data += ",\"sf2_status\":";
         JSON_Data += status_sf2;
         JSON_Data += ",\"sf1_read\":";
         JSON_Data += read_sf1;
         JSON_Data += ",\"sf2_read\":";
         JSON_Data += read_sf2;
         JSON_Data += ",\"sf1_beforeDelay\":";
         JSON_Data += before_delaysf1;
         JSON_Data += ",\"sf1_afterDelay\":";
         JSON_Data += after_delaysf1;
         JSON_Data += ",\"sf2_beforeDelay\":";
         JSON_Data += before_delaysf2;
         JSON_Data += ",\"sf2_afterDelay\":";
         JSON_Data += after_delaysf2;
         JSON_Data += ",\"sf1_psState\":";
         JSON_Data += ps_statesf1;
         JSON_Data += ",\"sf2_psState\":";
         JSON_Data += ps_statesf2;
         JSON_Data += ",\"sf1_sRest\":";
         JSON_Data += sf1_sensorRest;
         JSON_Data += ",\"sf2_sRest\":";
         JSON_Data += sf2_sensorRest;
         JSON_Data += ",\"sf1_timeslots\":[";
         JSON_Data += String(sf1_timeslots);
         JSON_Data += "],\"sf2_timeslots\":[";
         JSON_Data += String(sf2_timeslots);
         JSON_Data += "]}";
 // Serial.println(JSON_Data);     
  websockets.broadcastTXT(JSON_Data);
  
  
      ns.print(ipString);
      ns.print("\n");
       Serial.println(ipString);
    
      
}


}
