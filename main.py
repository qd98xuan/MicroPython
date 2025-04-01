# main.py -- put your code here!
from machine import Pin,SPI
import ssd1306
import network

def displayOnScreen(display,title,text1="",text2="",text3=""):
    display.fill(0)
    display.show()
    display.text(title,0,0)
    display.text(text1,0,20)
    display.text(text2,0,40)
    display.text(text3,0,60)
    display.show()


hspi = SPI(1)
display = ssd1306.SSD1306_SPI(128,64,hspi,Pin(5),Pin(4),Pin(16))
displayOnScreen(display,"log...")

waln = network.WLAN(network.STA_IF)
if not waln.isconnected():
    displayOnScreen(display,"log...","net","connecting...")
    waln.active(True)
    waln.connect("BAIYYYAP","baiyyy06")
    while(not waln.isconnected()):
        pass
    print("config:",waln.ifconfig()[0])
    displayOnScreen(display,"now ip",waln.ifconfig()[0],0,20)

