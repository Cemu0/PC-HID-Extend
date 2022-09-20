import serial
import time
from pynput import mouse, keyboard
import pyautogui
from threading import Timer

from pynput.mouse import Button, Controller
mouseController = Controller()

screen_w, screen_h = pyautogui.size()

MOUSE_LEFT = 1
MOUSE_RIGHT = 2
MOUSE_MIDDLE = 4
MOUSE_BACK = 8
MOUSE_FORWARD = 16

KEY_LEFT_CTRL = 0x80
KEY_LEFT_SHIFT = 0x81
KEY_LEFT_ALT = 0x82
KEY_LEFT_GUI = 0x83
KEY_RIGHT_CTRL = 0x84
KEY_RIGHT_SHIFT = 0x85
KEY_RIGHT_ALT = 0x86
KEY_RIGHT_GUI = 0x87

KEY_UP_ARROW = 0xDA
KEY_DOWN_ARROW = 0xD9
KEY_LEFT_ARROW = 0xD8
KEY_RIGHT_ARROW = 0xD7
KEY_BACKSPACE = 0xB2
KEY_TAB = 0xB3
KEY_RETURN = 0xB0
KEY_ESC = 0xB1
KEY_INSERT = 0xD1
KEY_PRTSC = 0xCE
KEY_DELETE = 0xD4
KEY_PAGE_UP = 0xD3
KEY_PAGE_DOWN = 0xD6
KEY_HOME = 0xD2
KEY_END = 0xD5
KEY_CAPS_LOCK = 0xC1
KEY_SCROLL_LOCK = 0xCF
KEY_F1 = 0xC2
KEY_F2 = 0xC3
KEY_F3 = 0xC4
KEY_F4 = 0xC5
KEY_F5 = 0xC6
KEY_F6 = 0xC7
KEY_F7 = 0xC8
KEY_F8 = 0xC9
KEY_F9 = 0xCA
KEY_F10 = 0xCB
KEY_F11 = 0xCC
KEY_F12 = 0xCD
KEY_F13 = 0xF0
KEY_F14 = 0xF1
KEY_F15 = 0xF2
KEY_F16 = 0xF3
KEY_F17 = 0xF4
KEY_F18 = 0xF5
KEY_F19 = 0xF6
KEY_F20 = 0xF7
KEY_F21 = 0xF8
KEY_F22 = 0xF9
KEY_F23 = 0xFA
KEY_F24 = 0xFB

KEY_NUM_LOCK = 0xDB
KEY_NUM_0 = 0xEA
KEY_NUM_1 = 0xE1
KEY_NUM_2 = 0xE2
KEY_NUM_3 = 0xE3
KEY_NUM_4 = 0xE4
KEY_NUM_5 = 0xE5
KEY_NUM_6 = 0xE6
KEY_NUM_7 = 0xE7
KEY_NUM_8 = 0xE8
KEY_NUM_9 = 0xE9
KEY_NUM_SLASH = 0xDC
KEY_NUM_ASTERISK = 0xDD
KEY_NUM_MINUS = 0xDE
KEY_NUM_PLUS = 0xDF
KEY_NUM_ENTER = 0xE0
KEY_NUM_PERIOD = 0xEB

buttonToID={
    keyboard.Key.alt: KEY_LEFT_ALT, #??
    keyboard.Key.alt_l: KEY_LEFT_ALT,
    keyboard.Key.alt_r: KEY_RIGHT_ALT, 
    keyboard.Key.alt_gr: KEY_RIGHT_ALT,
    keyboard.Key.backspace: KEY_BACKSPACE,
    keyboard.Key.caps_lock: KEY_CAPS_LOCK,
    keyboard.Key.cmd: KEY_LEFT_GUI,
    keyboard.Key.cmd_l: KEY_LEFT_GUI,
    keyboard.Key.cmd_r: KEY_RIGHT_GUI,
    keyboard.Key.ctrl: KEY_LEFT_CTRL,
    keyboard.Key.ctrl_l: KEY_LEFT_CTRL,
    keyboard.Key.ctrl_r: KEY_RIGHT_CTRL,
    keyboard.Key.delete : KEY_DELETE,
    keyboard.Key.down : KEY_DOWN_ARROW,
    keyboard.Key.end : KEY_END,
    keyboard.Key.enter : KEY_RETURN,
    keyboard.Key.esc : KEY_ESC,
    keyboard.Key.f1 : KEY_F1 ,
    keyboard.Key.f2 : KEY_F2 ,
    keyboard.Key.f3 : KEY_F3 ,
    keyboard.Key.f4 : KEY_F4 ,
    keyboard.Key.f5 : KEY_F5 ,
    keyboard.Key.f6 : KEY_F6 ,
    keyboard.Key.f7 : KEY_F7 ,
    keyboard.Key.f8 : KEY_F8 ,
    keyboard.Key.f9 : KEY_F9 ,
    keyboard.Key.f10 :KEY_F10,
    keyboard.Key.f11 :KEY_F11,
    keyboard.Key.f12 :KEY_F12,
    keyboard.Key.f13 :KEY_F13,
    keyboard.Key.f14 :KEY_F14,
    keyboard.Key.f15 :KEY_F15 ,
    keyboard.Key.f16 :KEY_F16 ,
    keyboard.Key.f17 :KEY_F17 ,
    keyboard.Key.f18 :KEY_F18 ,
    keyboard.Key.f19 :KEY_F19 ,
    keyboard.Key.f20 :KEY_F20 ,
    keyboard.Key.home : KEY_HOME,
    keyboard.Key.left : KEY_LEFT_ARROW,
    keyboard.Key.page_down :KEY_PAGE_DOWN,
    keyboard.Key.page_up : KEY_PAGE_UP,
    keyboard.Key.right : KEY_RIGHT_ARROW,
    keyboard.Key.shift :KEY_LEFT_SHIFT,
    keyboard.Key.shift_l :KEY_RIGHT_SHIFT,
    keyboard.Key.shift_r :KEY_RIGHT_SHIFT,
    keyboard.Key.space : ord(' '),
    keyboard.Key.tab : KEY_TAB,
    keyboard.Key.up : KEY_UP_ARROW,
    # keyboard.Key.media_play_pause : 
    # keyboard.Key.media_volume_mute :
    # keyboard.Key.media_volume_down :
    # keyboard.Key.media_volume_up :
    # keyboard.Key.media_previous :
    # keyboard.Key.media_next :
    keyboard.Key.insert : KEY_INSERT,
    # keyboard.Key.menu : 
    keyboard.Key.num_lock : KEY_NUM_LOCK,
    # keyboard.Key.pause :
    keyboard.Key.print_screen : KEY_PRTSC,
    keyboard.Key.scroll_lock : KEY_SCROLL_LOCK
}

def typeConvert(x):
    if x < 0:
        return x + 256
    return x


class SerialCommunicate():
    """
    Class that control the LED
    """

    def __init__(self):
        """
            initial serial port 
        """

        self.serial = serial.Serial(
            # port = 'COM16', \
            port = 'COM13', \
            baudrate=500000,\
            parity=serial.PARITY_NONE,\
            stopbits=serial.STOPBITS_ONE,\
            bytesize=serial.EIGHTBITS,\
            timeout=0.1)

        
        # print('[sys] init serial ', self.serial.open())
        print('[sys] init serial ', self.serial)

        # time.sleep(5)
        data = self.serial.readline()
        if data == b'Ready !\r\n':
            print("[sys] init success !")
        else:
            print("[sys] init failed !!!")

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


test = SerialCommunicate()

# for i in range(100, 255):
#     print(i)
#     test.sendData(keyboard=i)
#     test.sendData(keyboard=-i)
#     time.sleep(1)

# exit()

# not smaller than 0.007 pls 

# 0.021  125
# 0.001  125
# 0.0009  1000
device = 0

###test refresh speed
lastEnter = time.time() 
minTime = 10
minTimeAllow = 0.007

def resetVal():
    global device
    global last_position_x
    global last_position_y
    global mx
    global my
    global virtual_x
    global virtual_y
    last_position_x = None
    last_position_y = None
    mx = 0
    my = 0
    virtual_x = 0
    virtual_y = 0

def on_move_normal(x, y):
    # global minTime
    global device
    # if time.time() - lastEnter < minTime:
    #     minTime = time.time() - lastEnter 
    #     lastEnter = time.time()
    #     print(minTime)
    if x > 1919 and y > 100 and y < 1800:
        test.sendData(device=0)
        if device != 0:
            device = 0
            resetVal()
        print("device 0")
        return False

    if x == 0 and y > 100 and y < 1800:
        test.sendData(device=1)
        if device != 1:
            device = 1
            resetVal()
        resetVal()
        print("device 1")
        return False
    
last_position_x = None
last_position_y = None
mx = 0
my = 0
virtual_x = 0
virtual_y = 0
exiting = False
def on_move(x, y):
    global last_position_x
    global last_position_y
    global mx
    global my
    global virtual_x
    global virtual_y
    global lastEnter
    global device

    if time.time() - lastEnter < minTimeAllow:
        minTime = time.time() - lastEnter 
        # print(minTime)
        # time.sleep(minTimeAllow - minTime) #wait for ESP to finish send package

    # print('Pointer moved to {0}'.format(
    #     (x, y)))
    # test.sendData(x,y)

    if last_position_x is not None and last_position_y is not None:
        mx = x - last_position_x
        my = y - last_position_y
        # print(mx, my)
        test.sendData(mx,my)
        # mouseController.position = (x, y) #create bug
        # listener.wait
        virtual_x += mx
        virtual_y += my
        if device == 0:
            if virtual_x < -50:
                return False  

        if device == 1:
            if virtual_x > 1000:
                print("exit")
                return False  
        # print(virtual_x)
    else:
        if device == 0:
            test.sendData(-120,0)
        if device == 1:
            test.sendData(120,0)


    # else:
    #     last_position_x = x
    #     last_position_y = y

    last_position_x, last_position_y = mouseController.position

    # print(device, virtual_x, virtual_y)

    # listener.suppress_event() #still call back 
    # listener.
    # listener.position = (0, 0)
    
    lastEnter = time.time()

def on_click(x, y, button, pressed):
    # print(int(button))
    # print('{0} at {1}'.format(
    #     'Pressed' if pressed else 'Released',
    #     (x, y)))
    if button == Button.right:
        test.sendData(0,0, click = MOUSE_RIGHT if pressed else -MOUSE_RIGHT)
    if button == Button.left:
        test.sendData(0,0, click = MOUSE_LEFT if pressed else -MOUSE_LEFT)
    if button == Button.middle:
        test.sendData(0,0, click = MOUSE_MIDDLE if pressed else -MOUSE_MIDDLE)
    if button == Button.x2:
        # print(MOUSE_FORWARD)
        test.sendData(0,0, click = MOUSE_FORWARD if pressed else -MOUSE_FORWARD)
    if button == Button.x1:
        test.sendData(0,0, click = MOUSE_BACK if pressed else -MOUSE_BACK)
    
    # if not pressed:
    #     # Stop listener
    #     return False

def on_scroll(x, y, dx, dy):
    global lastEnter

    if time.time() - lastEnter < minTimeAllow:
        minTime = time.time() - lastEnter 
        # print(minTime)
        time.sleep(minTimeAllow - minTime)
    # print('Scrolled {0} at {1}'.format(
    #     'down' if dy < 0 else 'up',
    #     (x, y)))
    test.sendData(0,0, dy)
    # return False
    lastEnter = time.time()


def on_press(key):
    
    if key == keyboard.Key.f4:
        global exiting
        exiting = True
        listener.stop()
        exit()

    # print(key)
    # print(key, buttonToID.get(key,'Invalided'))
    id = buttonToID.get(key, None)
    if id == None:
        id = ord(key.char)
    test.sendData(keyboard=id)

    # print('pressed',id)

    # try:
    #     print('alphanumeric key {0} pressed'.format(
    #         key.char))
    # except AttributeError:
    #     print('special key {0} pressed'.format(
    #         key))

def on_release(key):
    # print(key, buttonToID.get(key,'Invalided'))
    id = buttonToID.get(key, None)
    if id == None:
        id = ord(key.char)
    # print('released',id)
    test.sendData(keyboard=-id)

    # try:
    #     print('alphanumeric key {0} released'.format(
    #         key.char))
    # except AttributeError:
    #     print('special key {0} released'.format(
    #         key))

    # if key == keyboard.Key.esc:
    #     # Stop listener
    #     return False 

# Collect events until released
while(1):
    with mouse.Listener(
            on_move=on_move_normal) as listener:
        listener.join()

    virtual_x = 0
    virtual_y = 0

    print('entered')

    # https://developer.apple.com/forums/thread/119022

    keyboardListener = keyboard.Listener(on_press=on_press, 
                           on_release=on_release, suppress = True)
    keyboardListener.start()

    with mouse.Listener(
            on_move=on_move,
            on_click=on_click,
            on_scroll=on_scroll, suppress = True) as listener:
        listener.join()
    keyboardListener.stop()

    if exiting:
        exit()
    


# listener = mouse.Listener(
#     on_move=on_move,
#     on_click=on_click,
#     on_scroll=on_scroll,
#     suppress = True)
# listener.start()

# while 1:
#     if last_position_x and last_position_y:
#         # mouseController.position = (last_position_x, last_position_y)
#         mouseController.move(mx,my)
    # mouseController.position = (0, 0)
        # time.sleep(5)


"""
if __name__ == '__main__':
    #define test unit and run
    import unittest

    test = LedControl()
    # test.start() 
    # test.Led1()
    # test.Led2()
    # test.stop()
    
    repeat = 1000

    class IntegerArithmeticTestCase(unittest.TestCase):
        
        def testLed1(self):  # test method names begin with 'test'
            self.assertEqual(test.Led1(), True)
            self.assertEqual(test.stop(), True)

        def testLed2(self):
            self.assertEqual(test.Led2(), True)
            self.assertEqual(test.stop(), True)

        def testFull(self):
            for _ in range(repeat):
                self.assertEqual(test.Led1(), True)
                self.assertEqual(test.stop(), True)
                self.assertEqual(test.Led2(), True)
                self.assertEqual(test.stop(), True)

    unittest.main()
"""

