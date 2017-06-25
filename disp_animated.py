import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image

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

def disp_load_screen(speed, cycles):
    file_num = 6 # number of files to load, starting with 0 ;)
    file_path = "icons/icon_restart/"
    file_name = "icon_restart_frame_" # does not contain interation number
    file_ext = ".png"
    count = 0

    while(file_num != 0):
        file_path_final = file_path + file_name + str(count) + file_ext
        frame = Image.open(file_path_final).resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')
        count = count + 1
        file_num = file_num- 1
        if(cycles > 0):
            disp.image(frame)
            disp.display()
            time.sleep(speed)
            cycles = cycles - 1
    disp.clear()
    disp.display()
# run at start:
disp_load_screen(0.1, 6)
