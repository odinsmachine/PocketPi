import  RPi.GPIO as GPIO
import time
import os, sys
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
import subprocess
from multiprocessing import Process

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(11, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(12, GPIO.IN,pull_up_down=GPIO.PUD_UP)

print("::")


# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

right_arrow = Image.open('icon_right.png').resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')
left_arrow = Image.open('icon_left.png').resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')

icon_shutdown = Image.open('/home/pi/Adafruit_Python_SSD1306/examples/icons/icon_io/icon_io_frame_0.png').resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')
icon_restart = Image.open('/home/pi/Adafruit_Python_SSD1306/examples/icons/icon_restart/icon_restart_frame_0.png').resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')
icon_reset = Image.open('/home/pi/Adafruit_Python_SSD1306/examples/icons/icon_reset/icon_reset_frame_0.png').resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')
icon_back = Image.open('/home/pi/Adafruit_Python_SSD1306/examples/icons/icon_back/icon_back_frame_0.png').resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')


def disp_reset():
    disp.clear()
    disp.display()
    time.sleep(0.1)

def arrow_left():
    disp.image(left_arrow)
    disp.display()

def arrow_right():
    disp.image(right_arrow)
    disp.display()

def pid_kill():
    shell_cmd = "sudo kill "
    fo = open("/home/pi/Adafruit_Python_SSD1306/examples/pid.txt", "r+")
    str = fo.read(10);
    print "full_reset : ", str
    fo.close()

    shell_cmd = shell_cmd + str
    os.system(shell_cmd)
    print("pid_kill: "),str

def disp_full_reset():
    disp_reset()
    pid_kill()
    print "full_reset : display clear"

def disp_load_screen(speed, cycles):
    while(cycles > 0):
        disp.image(icon_logo)
        disp.display()
        time.sleep(speed)
        disp.image(icon_logo_turn)
        disp.display()
        time.sleep(speed)
        cycles = cycles - 1

    disp_reset()

disp_load_screen(.2, 6)

i = 0

def menu_check(i):
    if(i == 0):
        print("> shutdown: selected:"),i
        disp.image(icon_shutdown)
        disp.display()
    elif(i == 1):
        print("> restart: selected:"),i
        disp.image(icon_restart)
        disp.display()
    elif(i == 2):
        print("> reset: selected"),i
        disp.image(icon_reset)
        disp.display()
    elif(i == 3):
        print("> back: selected"),i
        disp.image(icon_back)
        disp.display()

while True:
    center_input = GPIO.input(23) #button: center:
    right_input = GPIO.input(12) #button: right
    left_input = GPIO.input(11) #button: left:
    if (left_input == False):
        if(i > 0):
            i = i - 1
            print("left button:"),i
            disp_full_reset()
            arrow_left()
            time.sleep(0.3)
            disp_reset()
            menu_check(i)
        else:
            print("left button: max:"),i
            time.sleep(0.3)
    if (right_input == False):
        if(i != 5):
            i = i + 1
            print("right button:"),i
            disp_full_reset()
            arrow_right()
            time.sleep(0.3)
            disp_reset()
            menu_check(i)
        else:
            print("right button: max:"),i
            time.sleep(0.3)

    if (center_input == False):
        if(i == 0):
            print("> shutdown")
            disp_load_screen(.2, 5)
            #os.system("sudo shutdown -h now")
            time.sleep(0.3)
        elif(i == 1):
            print("> restart")
            disp_load_screen(.2, 5)
            #os.system("sudo reboot")
            time.sleep(0.3)
        elif(i == 2):
            print("> reset")
            
            time.sleep(0.3)
        elif(i == 3):
            print("> back")
            #os.system("sudo python /home/pi/Adafruit_Python_SSD1306/examples/mainmenu_7.py")
            time.sleep(0.3)
   
        






# end of file::
