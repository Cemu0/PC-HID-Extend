/**
 * This example turns the ESP32 into a Bluetooth LE mouse that continuously moves the mouse.
 */
#include <Arduino.h>
#include <BleCombo.h>
#include <EEPROM.h>
// #include <BleMouse.h>

BleCombo bleCombo;
// BleCombo bleCombo1("ESP32 Combo 1", "Espressif", 90);
// BleMouse bleCombo;

#define PACKAGE_MOUSE 'A'
#define PACKAGE_KEYBOARD 'B'
#define DEVICE_CHOSE 'C'
#define DEBUG_DATA 'D'
signed char inPackage[5]; //maximum package read each time

//support "unlimited" number of devices
uint8_t new_mac[][8] = {{0x34, 0xAF, 0xA4, 0x07, 0x0B, 0x66},
                        {0x32, 0xAE, 0xAA, 0x47, 0x0D, 0x61}, 
                        {0x38, 0xAE, 0xAC, 0x42, 0x0A, 0x31}, 
                        {0x36, 0x4b, 0xc7, 0xc2, 0xc5, 0x3f}, //... add as much as you want
                        };
int currentDevice = 0;

int keyboardCharacter;

void switchDevice(const int &Device){
  if(Device != currentDevice){
    // bleCombo.releaseAll();  
    // bleCombo.end(false);
    // auto address = &new_mac[Device][0];
    // Serial.print("switching ");
    // delay(100);
    // for(int i = 0; i < 6 ; ++i){
    //   Serial.print(address[i], HEX);
    //   Serial.print(":");
    // }
    // int deviceChose = EEPROM.read(0);
    currentDevice = Device;
    EEPROM.write(0,Device);
    EEPROM.commit();
    //lmao
    ESP.restart();
    // esp_sleep_enable_timer_wakeup(1);
    // esp_deep_sleep_start();  //back to setup :(( i found no other way 
    // Serial.println(esp_base_mac_addr_set(address));
    // bleCombo.begin();
    // bleCombo.releaseAll();  
  }
}

void setup() {
  Serial.begin(500000);
  EEPROM.begin(1);
  pinMode(2,OUTPUT);
  // switchDevice(0);
  currentDevice = EEPROM.read(0);
  Serial.println("device ");
  Serial.println(currentDevice);
  bleCombo.setDelay(2); //esp32
  esp_base_mac_addr_set(&new_mac[currentDevice][0]); //address 1
  bleCombo.begin();
  bleCombo.releaseAll();
  Serial.println("Ready !");
}

void loop() {
  if (Serial.available() > 0) {
    // char data = Serial.read();
    String data = Serial.readStringUntil('\n');
    // Serial.flush();

    //A 1 2_3_4^5\n
    //  x y h v Click  
    if(data[0] == PACKAGE_MOUSE){
      int index1 = data.indexOf(' ');
      int index2 = data.lastIndexOf(' '); 
      int index3 = data.indexOf('_');
      int index4 = data.lastIndexOf('_');
      int index5 = data.indexOf('^');
      // inPackage[0] = data.substring(0, index1).toInt();
      inPackage[0] = data.substring(index1+1, index2).toInt();
      inPackage[1] = data.substring(index2+1, index3).toInt();
      inPackage[2] = data.substring(index3+1, index4).toInt();
      inPackage[3] = data.substring(index4+1, index5).toInt();
      inPackage[4] = data.substring(index5+1, data.length()).toInt();

      bleCombo.move(inPackage[0],inPackage[1],inPackage[2],inPackage[3]);
      if(inPackage[4] > 0)
        // bleCombo.press(MOUSE_LEFT);
        bleCombo.mousePress(inPackage[4]);
      else if (inPackage[4] < 0)
        // bleCombo.release(MOUSE_LEFT);
        bleCombo.mouseRelease(-inPackage[4]);
    //B 1\n
    //  Button  
    }else if(data[0] == PACKAGE_KEYBOARD){
      int index1 = data.indexOf(' ');
      keyboardCharacter = data.substring(index1+1, data.length()).toInt();
      if(keyboardCharacter > 0)
        // bleCombo.press(MOUSE_LEFT);
        bleCombo.press((uint8_t)keyboardCharacter); //(uint8_t)keyboard
      else if (keyboardCharacter < 0){
        keyboardCharacter = -keyboardCharacter;
        bleCombo.release((uint8_t)keyboardCharacter);
    }
    //C 1\n
    //  Devices
    }else if(data[0] == DEVICE_CHOSE){
      int index1 = data.indexOf(' ');
      int device = data.substring(index1+1, data.length()).toInt();
      if(device >= 0)
        switchDevice(device);
    }else if(data[0] == DEBUG_DATA){
      int index1 = data.indexOf(' ');
      int request = data.substring(index1+1, data.length()).toInt();
      if(request >= 0)
        Serial.println("ok");
    }
    
    if(bleCombo.isConnected())
        Serial.print(1);
    else
        Serial.print(0);

    // Serial.println(inPackage[1]);
  }else{
    if(!bleCombo.isConnected())
        digitalWrite(2,millis() % 1000 > 500);
    else
        digitalWrite(2,bleCombo.getLedStatus(LED_CAPS_LOCK));
    
  }
}

