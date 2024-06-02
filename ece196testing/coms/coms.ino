#include "OLED_Driver.h"
#include "GUI_paint.h"
#include "DEV_Config.h"
#include "Debug.h"
#include "ImageData.h"

int i;
bool sending;


void setup() {
  i = 0;
  setupCommunication();
  System_Init();                                                                                                                                                                                                                                                                                   
  Serial.print(F("OLED_Init()...\r\n"));
  OLED_2IN42_Init();
  Driver_Delay_ms(500); 
  OLED_2IN42_Clear(); 
}

void loop() {

  //0.Create a new image cache
  UBYTE *BlackImage;
  UWORD Imagesize = ((OLED_2IN42_WIDTH%8==0)? (OLED_2IN42_WIDTH/8): (OLED_2IN42_WIDTH/8+1)) * OLED_2IN42_HEIGHT;
  Paint_NewImage(BlackImage, OLED_2IN42_WIDTH, OLED_2IN42_HEIGHT, 270, BLACK);  

  //1.Select Image
  Paint_SelectImage(BlackImage);
  Paint_Clear(BLACK);

  //declare strings
  String command = "";

  int recieved = 0;
  while (command != "Z"){

    String message = receiveMessage();
    while (recieved == 0){
      if(message != ""){
        command = message;
        recieved = 1;
        Paint_Clear(BLACK); 
        Paint_DrawString_EN(10, 0, message.c_str(), &Font12, WHITE, WHITE);
        OLED_2IN42_Display(BlackImage);
        sendMessage(message);
      }
    }
    recieved = 0;
  }

}

