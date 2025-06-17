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

def get_network_time():
    try:
        resp = urequests.get("http://worldtimeapi.org/api/timezone/Asia/Shanghai")
        data = json.loads(resp.text)
        datetime_str = data["datetime"]  # 例如 "2025-06-17T15:30:45.123456+08:00"
        time_part = datetime_str.split("T")[1].split(".")[0]  # "15:30:45"
        hour, minute, second = map(int, time_part.split(":"))
        return hour, minute, second
    except Exception as e:
        print("获取网络时间失败:", e)
        return None, None, None


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
    refreshTime = 18000
    nowMode = 1 # 1-天气信息 0-时间信息
    weatherPinin1 = ""
    weatherPinin2 = ""
    reportDate = ""
    reportTime = ""
    temp = ""
    needRefreshScreen = False

    while True:
        if nowMode == 0:
            # 获取当前时间
            hour,minute,second = get_network_time()
            # 格式化时间字符串
            time_str = "{:02}:{:02}:{:02}".format(hour, minute, second)
            displayOnScreen(display,"QingDao ^_^",time_str)
        else:
            if(refreshTime ==18000):
                resp = urequests.get("https://restapi.amap.com/v3/weather/weatherInfo?key=d146bc3bf8eb1c1e1faa3f035e1a864b&city=370200")
                resp_json = json.loads(resp.text)
                print(resp_json)
                # print(resp_json.get('status'))
                # print(resp_json.get('lives')[0].get('weather'))
                # print(resp_json.get('lives')[0].get('reporttime'))
                netWeather = resp_json.get('lives')[0].get('weather')
                weathers = weather_data.get('weathers')
                
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
                refreshTime = 0
                needRefreshScreen = True
        if needRefreshScreen==True:
            needRefreshScreen = False
            displayOnScreen(display,"QingDao ^_^","temp:"+temp,"date:"+reportDate,"time:"+reportTime,weatherPinin1,weatherPinin2)
                
        # 监听按下按钮
         # 监听按下Flash按钮
        flash_button = Pin(0, Pin.IN, Pin.PULL_UP)
        if flash_button.value() == 0:
            if nowMode == 0:
                nowMode = 1
                displayOnScreen(display,"QingDao ^_^","temp:"+temp,"date:"+reportDate,"time:"+reportTime,weatherPinin1,weatherPinin2)
            else:
                nowMode = 0    
        refreshTime += 1
        # 延迟1秒
        time.sleep(1)
       

