
String lineOne;
String lineTwo;
String lineThree;
String message;
//String lineFour;
//char test[26] = {"You really should learn ASL"};
//char test[31] = {'Y', 'o', 'u', ' ', 'r', 'e', 'a', 'l', 'l', 'y', ' ', 
//'s', 'h', 'o', 'u', 'l', 'd', ' ', 'l', 'e', 'a', 'r', 'n', ' ', 'A', 'S', 'L', ' ', ' ', ' ', ' '};
char test[5] = {'A', 'B', 'C', 'D', 'E'};
int i;

void setup() {
  //setupCommunication();
  setupDisplay();
  writeDisplay("No Connection", 0, true);
  delay(10000);
  writeDisplay("Connected", 0, true);
  delay(3000);
  lineOne = "";
  lineTwo = "";
  lineThree = "";
  //lineFour = "";

  i=0;
}
 void loop() {
  message = test[i];
  //String message = receiveMessage();
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