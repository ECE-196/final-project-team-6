#include "OLED_Driver.h"
#include "GUI_paint.h"
#include "DEV_Config.h"
#include "Debug.h"
#include "ImageData.h"

String lineOne;
String lineTwo;
String lineThree;
//String lineFour;

void setup() {
  setupCommunication();
  setupDisplay();
  writeDisplay("No Connection", 0, true);
  lineOne = "";
  lineTwo = "";
  lineThree = "";
  //lineFour = "";



  //waveshare functions
  System_Init();                                                                                                                                                                                                                                                                                   
  OLED_2IN42_Init();
  Driver_Delay_ms(500); 
  OLED_2IN42_Clear(); 

  

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
  }
}