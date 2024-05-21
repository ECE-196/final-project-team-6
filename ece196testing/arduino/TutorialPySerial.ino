
void setup() {
   setupCommunication();
   setupDisplay();
   writeDisplay("No Connection", 0, true);
}
 void loop() {
   String message = receiveMessage();
   if(message != "") {
     writeDisplay(message.c_str(), 0, true);
     sendMessage(message);
   }
}