
// Acceleration values recorded from the readAccelSensor() function
int ax = 0; int ay = 0; int az = 0;
int ppg = 0;        // PPG from readPhotoSensor() (in Photodetector tab)
int sampleTime = 0; // Time of last sample (in Sampling tab)
bool sending;
unsigned long previous_time = millis();
int action = 0;

void setup() {
  setupCommunication();
  sending = false;
}

void loop() {
  String command = receiveMessage();
  writeDisplay(command.c_str(), 0, false);  
}