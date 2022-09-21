import serial

class SerialCommunicate():
    """
    Class that control the LED
    """

    def __init__(self, COMPort):
        """
            initial serial port 
        """

        self.serial = serial.Serial(
            # port = 'COM16', \
            # port = 'COM13', \
            port = COMPort, \
            baudrate=500000,\
            parity=serial.PARITY_NONE,\
            stopbits=serial.STOPBITS_ONE,\
            bytesize=serial.EIGHTBITS,\
            timeout=0.1)

        
        # print('[sys] init serial ', self.serial.open())
        print('[sys] init serial ', self.serial)

        # time.sleep(5)
        # data = self.serial.readline()
        # if data == b'Ready !\r\n':
        #     print("[sys] init success !")
        # else:
        #     print("[sys] init failed !!!")

    def sendData(self, x = 0, y = 0, horizontalScroll = 0, verticalScroll = 0, click = 0, keyboard = 0, device = -1):
        if device != -1:
            sendData = bytearray(("C" + " " + str(device) + '\n').encode()) #A 0 1_2_3^4\n
            self.serial.write(sendData)
        elif keyboard != 0:
            sendData = bytearray(("B" + " " + str(keyboard) + '\n').encode()) #A 0 1_2_3^4\n
            self.serial.write(sendData)
        else:
            sendData = bytearray(("A" + " " + str(x) + " " + str(y) + "_" + str((horizontalScroll)) 
                                    + "_" + str(verticalScroll)+  "^"  + str(click) 
                                    + '\n').encode()) #A 0 1_2_3^4\n
            # print(sendData)
            self.serial.write(sendData)

        data = self.serial.read(1)
        if(data == ord('0')):
            return False
        return True

    def __del__(self):
        self.serial.close()             # close port
        print("Self stop serial")

