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

def disp_load_screen(delay, cycles, file_num, file_path, file_name, file_ext):
    disp.clear()
    disp.display()
    count = 0
    og_file_num = file_num

    while(cycles > 0):
        file_path_final = file_path + file_name + str(count) + file_ext
        frame = Image.open(file_path_final).resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')
        count = count + 1
        file_num = file_num- 1
        disp.image(frame)
        disp.display()
        time.sleep(delay)
        cycles = cycles - 1
        if(file_num == 0 and cycles > 0):
            file_num = og_file_num
            count = 0
    disp.clear()
    disp.display()
# run at start:
# delay: cycles: f_num: f_path: f_name: f_ext:
disp_load_screen(0.1, 6, 6, "icons/icon_restart/", "icon_restart_frame_", ".png")


#file_num = 6 # number of files to load, starting with 0 ;)
    #file_path = "icons/icon_restart/"
    #file_name = "icon_restart_frame_" # does not contain interation number
    #file_ext = ".png"
