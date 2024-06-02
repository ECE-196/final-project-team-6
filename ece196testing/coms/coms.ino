#include "OLED_Driver.h"
#include "GUI_paint.h"
#include "DEV_Config.h"
#include "Debug.h"
#include "ImageData.h"

int i;
bool sending;
String command;

void setup() {
  System_Init();                                                                                                                                                                                                                                                                                   
  Serial.print(F("OLED_Init()...\r\n"));
  OLED_2IN42_Init();
  Driver_Delay_ms(500); 
  OLED_2IN42_Clear(); 
  setupCommunication();
  //setupDisplay();
}

void loop() {

  //0.Create a new image cache
  UBYTE *BlackImage;
  UWORD Imagesize = ((OLED_2IN42_WIDTH%8==0)? (OLED_2IN42_WIDTH/8): (OLED_2IN42_WIDTH/8+1)) * OLED_2IN42_HEIGHT;
  if((BlackImage = (UBYTE *)malloc(Imagesize)) == NULL) { 
      Serial.print("Failed to apply for black memory...\r\n");
      //return -1;
  }
  Serial.print("Paint_NewImage\r\n");
  Paint_NewImage(BlackImage, OLED_2IN42_WIDTH, OLED_2IN42_HEIGHT, 270, BLACK);  

  //1.Select Image
  Paint_SelectImage(BlackImage);
  Paint_Clear(BLACK);

  //declare strings
  char comms[18] = {'a', 'r', 'd', 'u', 'i', 'n', 'o', ' ', 't', 'e', 's', 't', ' ', 't', 'r', 'y', '2', 'Z'};

  while (command != "Z"){
    //receive command
    command = comms[i]; //receive command input

    String message = receiveMessage();   
    if(message != "") { 
      //write display
      Paint_Clear(BLACK); 
      Paint_DrawString_EN(10, 0, message.c_str(), &Font12, WHITE, WHITE);
      Paint_DrawString_EN(10, 15, command.c_str(), &Font12, WHITE, WHITE);
      OLED_2IN42_Display(BlackImage);
      Driver_Delay_ms(1000);
    }
    i = i+1;
  }

}
