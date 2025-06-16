# main.py -- put your code here!
from machine import Pin,SPI
import ssd1306
import network
import urequests
import json
import time

def displayOnScreen(display,title,text1="",text2="",text3="",text4="",text5=""):
    display.fill(0)
    display.show()
    display.text(title,0,5)
    display.text(text1,0,17)
    display.text(text2,0,27)
    display.text(text3,0,37)
    display.text(text4,0,47)
    display.text(text5,0,57)
    display.show()


hspi = SPI(1)
display = ssd1306.SSD1306_SPI(128,64,hspi,Pin(5),Pin(4),Pin(16))
displayOnScreen(display,"log...")

waln = network.WLAN(network.STA_IF)
if not waln.isconnected():
    displayOnScreen(display,"log...","net","connecting...")
    waln.active(True)
    waln.connect("瑜阳体育","neixiao666")
    # waln.connect("HXPhone","1472583690")
    # 解析weather.json，转成对象
    weather_data = {}
    with open('weather.json', 'r') as f:
        weather_data = json.load(f)
    while(not waln.isconnected()):
        pass
    print("config:",waln.ifconfig()[0])
    displayOnScreen(display,"now ip",waln.ifconfig()[0])

    while True:
        displayOnScreen(display,"QingDao ^_^","temp:--","date:--","time:--","XXXXXX","XXXXXX")
        # 延迟1000毫秒
        time.sleep(1)
        resp = urequests.get("https://restapi.amap.com/v3/weather/weatherInfo?key=d146bc3bf8eb1c1e1faa3f035e1a864b&city=370200")
        resp_json = json.loads(resp.text)
        print(resp_json)
        # print(resp_json.get('status'))
        # print(resp_json.get('lives')[0].get('weather'))
        # print(resp_json.get('lives')[0].get('reporttime'))
        netWeather = resp_json.get('lives')[0].get('weather')
        weathers = weather_data.get('weathers')
        weatherPinin1 = ""
        weatherPinin2 = ""
        for weather in weathers:
            if netWeather == weather.get('name'):
                pinin = weather.get('pinin')
                if len(pinin) >=16:
                    weatherPinin1 = pinin[:16]
                    weatherPinin2 = pinin[16:]
                else:
                    weatherPinin1 = pinin
                break
        
        reportDate = resp_json.get('lives')[0].get('reporttime').split(" ")[0]
        reportTime = resp_json.get('lives')[0].get('reporttime').split(" ")[1]
        temp = resp_json.get('lives')[0].get('temperature')
        displayOnScreen(display,"QingDao ^_^","temp:"+temp,"date:"+reportDate,"time:"+reportTime,weatherPinin1,weatherPinin2)
        # 延迟1000毫秒
        time.sleep(1800)


