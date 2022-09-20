/**
 * This example turns the ESP32 into a Bluetooth LE mouse that continuously moves the mouse.
 */
#include <Arduino.h>
#include <BleCombo.h>
// #include <BleMouse.h>

BleCombo bleCombo;
// BleCombo bleCombo1("ESP32 Combo 1", "Espressif", 90);
// BleMouse bleCombo;

signed char inPackage[10];
int keyboard;
int pos = 0;
void setup() {
  Serial.begin(500000);
  bleCombo.begin();
  // bleCombo1.begin();
  bleCombo.releaseAll();
  // bleCombo1.releaseAll();
  pinMode(2,OUTPUT);
  Serial.println("Ready !");
}

void loop() {
  if(bleCombo.isConnected()) {
    if (Serial.available() > 0) {
        // char data = Serial.read();
        String data = Serial.readStringUntil('\n');

        // if(data == '\n'){
        // Serial.readBytesUntil('\n',(uint8_t *) inPackage, 4);
        
        //0 0 2_3_5\n

        Serial.flush();
        int index1 = data.indexOf(' ');
        int index2 = data.lastIndexOf(' '); 
        int index3 = data.indexOf('_');
        int index4 = data.lastIndexOf('_');
        inPackage[0] = data.substring(0, index1).toInt();
        inPackage[1] = data.substring(index1+1, index2).toInt();
        inPackage[2] = data.substring(index2+1, index3).toInt();
        inPackage[3] = data.substring(index3+1, index4).toInt();
        keyboard = data.substring(index4+1, data.length()).toInt();
        // strcpy((char *)inPackage, data.c_str());
        // bleCombo.move(inPackage[0],inPackage[1],inPackage[2]);
        bleCombo.move(inPackage[0],inPackage[1],inPackage[2]);

        if(inPackage[3] > 0)
          // bleCombo.press(MOUSE_LEFT);
          bleCombo.mousePress(inPackage[3]);
        else if (inPackage[3] < 0)
          // bleCombo.release(MOUSE_LEFT);
          bleCombo.mouseRelease(-inPackage[3]);

        if(keyboard > 0)
          // bleCombo.press(MOUSE_LEFT);
          bleCombo.press((uint8_t)keyboard); //(uint8_t)keyboard
        else if (keyboard < 0){
          keyboard = -keyboard;
          bleCombo.release((uint8_t)keyboard);
        }
        // bleCombo.release(MOUSE_LEFT);

        Serial.println(inPackage[1]);
        digitalWrite(2,!bleCombo.getLedStatus(LED_CAPS_LOCK));
        // Serial.print(" ");
        // Serial.println();
        // Serial.println((uint8_t)' ');
        // pos = 0;
        // }
        // else{
        //   inPackage[pos] = data;
        //   pos++;
        // }
    }else{
        // BLEDevice::

    }
  }


  // if(bleCombo1.isConnected()){
  //   bleCombo.print("this should work");
  //   delay(1000);
  // }


}

