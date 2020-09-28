import discord
from discord.ext import commands
import asyncio
import sys
import os
import time
import Adafruit_DHT
import RPi.GPIO as GPIO
import core.global_variables
from core.lcd import lcd_print, lcd_clear

bot = core.global_variables.get_value('bot')
char = ['0','1','2','3','4','5','6','7','8','9',
        'a','b','c','d','e','f','g','h','i','j','k','l','m',
        'n','o','p','q','r','s','t','u','v','w','x','y','z',
        ' ',',','.','?','!','+','-','*','/','=','>','<','_','(',')','\'','\"'
        ,'\\',':',';','@','#','$','%','^','&','`','~','[',']','{','}','|',
        'A','B','C','D','E','F','G','H','I','J','K','L','M',
        'N','O','P','Q','R','S','T','U','V','W','X','Y','Z']  # 傳送訊息的字元表
nowMenu = 1     # 正在首頁
menuList = 0    # 0=顯示日期時間 1=顯示溫度 2=傳送訊息
nowDate = 0     # 正在顯示日期時間
nowTemp = 0     # 正在顯示溫度
nowMessage = 0  # 正在傳送訊息
nowLight = 0    # 正在控制電燈
messageStr = '' # 傳送訊息的字串
charPos = 0     # 傳送訊息的字串 目前選擇的字元(0~94)
timectl = 0.0   # 控制時間
timectl = time.time()
cursorBlink = 0 # cursor的閃爍 0=cursor 1=character
light = 0       # 選擇電燈開關 0=off 1=on

def btn_push(btn : int):
    global nowMenu  # 使用全域變數
    global menuList
    global nowDate
    global nowTemp
    global nowMessage
    global nowLight
    if (nowMenu == 1):       # menu中控制
        inMenu(btn)
    elif (nowDate == 1):     # date中控制
        inDate(btn)
    elif (nowTemp == 1):     # temp中控制
        inTemp(btn)
    elif (nowMessage == 1):  # message中控制
        inMessage(btn)
    elif (nowLight == 1):    # light中控制
        inLight(btn)

def inMenu(btn : int):  # 在menu中的按鈕控制
    global nowMenu  # 使用全域變數
    global menuList
    global nowDate
    global nowTemp
    global nowMessage
    global nowLight
    global messageStr
    if (btn == 2):
        menuList -= 1
        if (menuList%4 == 0):
            lcd_print('display date', '& time')
        if (menuList%4 == 1):
            lcd_print('display temp', '& humi')
        if (menuList%4 == 2):
            lcd_print('send message', 'to discord')
        if (menuList%4 == 3):
            lcd_print('turn on/off', 'the light')
    elif (btn == 3):
        menuList += 1
        if (menuList%4 == 0):
            lcd_print('display date', '& time')
        if (menuList%4 == 1):
            lcd_print('display temp', '& humi')
        if (menuList%4 == 2):
            lcd_print('send message', 'to discord')
        if (menuList%4 == 3):
            lcd_print('turn on/off', 'the light')
    elif (btn == 4):
        if (menuList%4 == 0):
            nowMenu = 0
            nowDate = 1
            lcd_print("Date: {}".format(time.strftime("%Y/%m/%d")),
                "Time: {}".format(time.strftime("%H:%M:%S")))
            inDate(0)
        if (menuList%4 == 1):
            nowMenu = 0
            nowTemp =1
            inTemp(0)
        if (menuList%4 == 2):
            nowMenu = 0
            nowMessage = 1
            lcd_clear()
            messageStr = ''
            inMessage(0)
        if (menuList%4 == 3):
            nowMenu = 0
            nowLight = 1
            inLight(0)

def inDate(btn = 0):  # 在date中的按鈕控制
    global nowMenu  # 使用全域變數
    global menuList
    global nowDate
    global nowTemp
    global nowMessage
    if (btn == 0):
        lcd_print("Date: {}".format(time.strftime("%Y/%m/%d")),
                  "Time: {}".format(time.strftime("%H:%M:%S")), 0)
        time.sleep(0.1)
    elif (btn == 1) or (btn == 4):
        toMenu()
    
def inTemp(btn = 0):  # 在temp中的按鈕控制
    global nowMenu  # 使用全域變數
    global menuList
    global nowDate
    global nowTemp
    global nowMessage
    humi, temp = Adafruit_DHT.read_retry(11, 4)
    if (btn == 0):
        lcd_print('Temp: {:0.1f} deg C'.format(temp),
                  'Humi: {:0.1f} %'.format(humi))
        time.sleep(0.1)
    elif (btn == 1) or (btn == 4):
        toMenu()
    
def inMessage(btn = 0):  # 在message中的按鈕控制
    global char  # 使用全域變數
    global nowMenu
    global menuList
    global nowDate
    global nowTemp
    global nowMessage
    global messageStr
    global charPos
    global timectl
    global cursorBlink
    if (time.time() - timectl >= 0.25):  # cursor閃爍
        if (cursorBlink == 0):  # 有cursor
            lcd_print(messageStr[:16:], messageStr[16::], True, 1)
            cursorBlink = (cursorBlink + 1) % 2
        else:  # 無cursor
            if (len(messageStr) <= 16):
                lcd_print(messageStr[:16:] + char[charPos], messageStr[16::], True, 0)
            else:
                lcd_print(messageStr[:16:], messageStr[16::] + char[charPos], True, 0)
            cursorBlink = (cursorBlink + 1) % 2
        timectl = time.time()
    if (GPIO.input(13) == 1) and (GPIO.input(15) == 1):  # 發送message
        asyncio.ensure_future(send(messageStr))
        charPos = 0 
        toMenu()
    elif (btn == 1):  # 退出message 刪除一個字元
        if (len(messageStr) == 0):
            messageStr = ''
            charPos = 0 
            toMenu()
        else:
            messageStr = messageStr[:-1:]
            charPos = 0
    elif (btn == 2):  # 切換上一個字元
        charPos -= 1
        if (charPos < 0):
            charPos = 94
    elif (btn == 3):  # 切換下一個字元
        charPos += 1
        if (charPos > 94):
            charPos = 0
    elif (btn == 4):  # 確定一個字元
        messageStr += char[charPos]
        charPos = 0
    time.sleep(0.02)
    
async def send(sendStr : str):
    global bot
    channel = bot.get_channel(660656251843379243)
    await channel.send(sendStr)
    
def inLight(btn = 0):
    global light
    if (btn == 0):
        if (light == 0):
            lcd_print('turn the light:', '  *off*    on ', False)
        elif (light == 1):
            lcd_print('turn the light:', '   off    *on*', False)
    elif (btn == 1):
        toMenu()
    elif (btn == 2):
        light = 0
        inLight(0)
    elif (btn == 3):
        light = 1
        inLight(0)
    elif (btn == 4):
        if (light == 0):
            GPIO.output(12, 0)
            asyncio.ensure_future(send('已關閉電燈'))
        else:
            GPIO.output(12, 1)
            asyncio.ensure_future(send('已開啟電燈'))
        toMenu()
    
def toMenu():  # 初始化至首頁
    global nowMenu  # 使用全域變數
    global menuList
    global nowDate
    global nowTemp
    global nowMessage
    nowMenu = 1
    nowDate = 0
    nowTemp = 0
    nowMessage = 0
    if (menuList%4 == 0):
        lcd_print('display date', '& time')
    if (menuList%4 == 1):
        lcd_print('display temp', '& humi')
    if (menuList%4 == 2):
        lcd_print('send message', 'to discord')
    if (menuList%4 == 3):
        lcd_print('turn on/off', 'the light')