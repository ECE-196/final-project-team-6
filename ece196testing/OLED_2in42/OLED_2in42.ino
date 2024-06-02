#include "OLED_Driver.h"
#include "GUI_paint.h"
#include "DEV_Config.h"
#include "Debug.h"
#include "ImageData.h"

int i;
bool sending;


void setup() {
  i = 0;

  System_Init();                                                                                                                                                                                                                                                                                   
  Serial.print(F("OLED_Init()...\r\n"));
  OLED_2IN42_Init();
  Driver_Delay_ms(500); 
  OLED_2IN42_Clear(); 
  setupCommunication();

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
  Paint_DrawString_EN(10, 0, "Team 6 Project", &Font12, WHITE, WHITE);
  Paint_DrawString_EN(10, 17, "Sign Language CC", &Font8, WHITE, WHITE);
  Paint_DrawString_EN(10, 30, "Initial Bootup", &Font8, WHITE, WHITE);
  Paint_DrawNum(10, 43, "5292024", &Font12, 4, WHITE, WHITE);
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

  //declare strings
  char comms[18] = {'a', 'r', 'd', 'u', 'i', 'n', 'o', ' ', 't', 'e', 's', 't', ' ', 't', 'r', 'y', '2', 'Z'};
  String command = " ";
  String lineOne = "EMPTY";
  String lineTwo = "EMPTY";
  String lineThree = "EMPTY";
  String lineFour = "EMPTY";
  int recieved = 0;
  i = 0;
  while (command != "Z"){
    //receive command
    //command = comms[i]; //receive command input

    String message = receiveMessage();
    while (recieved == 0){
      if(message != ""){
        command = message;
        recieved = 1;
        //sendMessage(message);
      }
    }
    recieved = 0;

    Paint_Clear(BLACK); 

    Paint_DrawString_EN(10, 0, lineOne.c_str(), &Font12, WHITE, WHITE);

    Paint_DrawString_EN(10, 15, lineTwo.c_str(), &Font12, WHITE, WHITE);

    Paint_DrawString_EN(10, 30, lineThree.c_str(), &Font12, WHITE, WHITE);
    
    Paint_DrawString_EN(10, 45, lineFour.c_str(), &Font12, WHITE, WHITE);

    OLED_2IN42_Display(BlackImage);
    Driver_Delay_ms(1000);

    //shift all valus down
    if (command == " "){
      lineFour = lineThree;
      lineThree = lineTwo;
      lineTwo = lineOne;
      lineOne = command;
    } 
    else if (command != ""){      
      lineOne = lineOne + command;
    }
    

    i = i+1;
  }
  // Show image on page
  //OLED_2IN42_Display(BlackImage);
  //Driver_Delay_ms(5000);  
  Paint_Clear(BLACK); 
  OLED_2IN42_Display(BlackImage);
  Driver_Delay_ms(3000);

}
