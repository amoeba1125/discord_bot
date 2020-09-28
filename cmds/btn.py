import discord
import sys
import RPi.GPIO as GPIO
import json, asyncio, datetime
from discord.ext import commands
sys.path.append("..")
from core.classes import Cog_Extension
from core.lcd_contents import btn_push, toMenu

GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.IN) #按鈕腳位
GPIO.setup(13, GPIO.IN) #按鈕腳位
GPIO.setup(15, GPIO.IN) #按鈕腳位
GPIO.setup(16, GPIO.IN) #按鈕腳位

lastPinValue11 = 0
lastPinValue13 = 0
lastPinValue15 = 0
lastPinValue16 = 0

class btn(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        toMenu()
        
        async def interval():  # 持續運作
            global lastPinValue11  # 使用全域變數
            global lastPinValue13
            global lastPinValue15
            global lastPinValue16
            await self.bot.wait_until_ready()
            self.channel = self.bot.get_channel(660656251843379243)
            while not self.bot.is_closed():
                pinValue11 = GPIO.input(11)
                pinValue13 = GPIO.input(13)
                pinValue15 = GPIO.input(15)
                pinValue16 = GPIO.input(16)
                
                if (pinValue11 == 1) and (lastPinValue11 == 0):  # 按下按鈕
                    btn_push(4)
                if (pinValue13 == 1) and (lastPinValue13 == 0):
                    btn_push(3)
                if (pinValue15 == 1) and (lastPinValue15 == 0):
                    btn_push(2)
                if (pinValue16 == 1) and (lastPinValue16 == 0):
                    btn_push(1)
                if (pinValue11 == 0) and (pinValue13 == 0) and (pinValue15 == 0) and (pinValue16 == 0):
                    btn_push(0)
                    
                lastPinValue11 = pinValue11
                lastPinValue13 = pinValue13
                lastPinValue15 = pinValue15
                lastPinValue16 = pinValue16
                await asyncio.sleep(0.02)
        
        self.bg_task = self.bot.loop.create_task(interval())
    
def setup(bot):
    bot.add_cog(btn(bot))