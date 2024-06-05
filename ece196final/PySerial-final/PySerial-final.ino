
String lineOne;
String lineTwo;
String lineThree;
String message;
//String lineFour;

int i;

void setup() {
  setupCommunication();
  setupDisplay();
  writeDisplay("No Connection", 0, true);
  //delay(10000);
  //writeDisplay("Connected", 0, true);
  //delay(3000);
  lineOne = "";
  lineTwo = "";
  lineThree = "";
  //lineFour = "";

  i=0;
}
 void loop() {
  String message = receiveMessage();
  if(message != "") {

    if (message == " "){
      //lineFour = lineThree;
      lineThree = lineTwo;
      lineTwo = lineOne;
      lineOne = "";
    }
    else{      
      lineOne = lineOne + message;
    }

    writeDisplay(lineOne.c_str(), 0, true);
    writeDisplay(lineTwo.c_str(), 1, true);
    writeDisplay(lineThree.c_str(), 2, true);
    sendMessage(message);
    i = i+1;
  }
  delay(750);
}