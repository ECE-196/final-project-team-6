#include "OLED_Driver.h"
#include "GUI_paint.h"
#include "DEV_Config.h"
#include "Debug.h"
#include "ImageData.h"

void setup() {
  System_Init();                                                                                                                                                                                                                                                                                   
  Serial.print(F("OLED_Init()...\r\n"));
  OLED_2IN42_Init();
  Driver_Delay_ms(500); 
  OLED_2IN42_Clear(); 

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
  
  // Drawing on the image
  Serial.print("Drawing:page 2\r\n");     
  Paint_DrawString_EN(10, 0, "Initial bootup", &Font12, WHITE, WHITE);
  Paint_DrawString_EN(10, 17, "Testing line 2", &Font8, WHITE, WHITE);
  Paint_DrawNum(10, 30, "bootup test", &Font8, 4, WHITE, WHITE);
  Paint_DrawNum(10, 43, "bootup test", &Font12, 4, WHITE, WHITE);
  // Show image on page2
  OLED_2IN42_Display(BlackImage);
  Driver_Delay_ms(5000);  
  Paint_Clear(BLACK);   
  
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

  String command = "test line 0";

  //recieve string to print

  command = "test line 1";   
  Paint_DrawString_EN(10, 0, command.c_str(), &Font12, WHITE, WHITE);
  OLED_2IN42_Display(BlackImage);
  Driver_Delay_ms(2000);

  command = "test line 2";
  Paint_DrawString_EN(10, 15, command.c_str(), &Font12, WHITE, WHITE);
  OLED_2IN42_Display(BlackImage);
  Driver_Delay_ms(2000);

  command = "test line 3";
  Paint_DrawString_EN(10, 30, command.c_str(), &Font12, WHITE, WHITE);
  OLED_2IN42_Display(BlackImage);
  Driver_Delay_ms(2000);
  
  command = "test line 4";
  Paint_DrawString_EN(10, 45, command.c_str(), &Font12, WHITE, WHITE);
  OLED_2IN42_Display(BlackImage);
  Driver_Delay_ms(2000);

  // Show image on page
  //OLED_2IN42_Display(BlackImage);
  //Driver_Delay_ms(5000);  
  Paint_Clear(BLACK); 
  OLED_2IN42_Display(BlackImage);
  Driver_Delay_ms(3000);

}
