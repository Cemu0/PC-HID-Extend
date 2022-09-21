# PC HID Extend
Extent your **PC keyboard and mouse (HID)** to your **mobile devices** using a BLE hub such as ESP32. ESP will simulate BLE keyboard and Bluetooth to control other device that support BLE, this mean you *don't have to install any software or hack your phone at all*, just connect the phone with the ESP32 via Bluetooth setting.  
This come with a script that will track your mouse movement if you move your mouse to the right edge of the screen, the script will hook and capture all mouse and keyboard movement, then push it to the ESP32, then you can control your phone/table/etc by your PC mouse and keyboard.

![WOW](img/IMG_0162.GIF)

# Usage 
Current I don't have any hex file for the ESP32 so to upload the code you need to download this repo and build it.
1. Clone this repo
2. Open in VSCode that already install PlatformIO extension
3. Hookup your ESP32 and press upload (->).
4. Connect your mobile device via Bluetooth setting with `ESP32 Combo`
5. Then using the [PCcontrol/control.py script](/PCcontrol/control.py) you can request ESP32 to move the mouse and keyboard when move mouse to the right. This require you have python (3.7) and all package require to run. For convener I also prebuilt the software with pyinstaller [here](https://github.com/Cemu0/PC-HID-Extend/releases). 


# Peripheral  
BLE peripheral can only be connected to one central device (a mobile phone, etc.) at a time!

So in order to connect with multiple device ... the ESP need to reset to change MAC address.

In theory you can connect as much device as you want but current I only write up to 2 device, the right and left of screen, you need to pass the augment `python control.py -d 2` to the software to enable more than 1 device ! but this will come with a delay around 2s when switching between devices.


