import discord
import sys
import RPi.GPIO as GPIO
import Adafruit_DHT
from discord.ext import commands
sys.path.append("..")
from core.classes import Cog_Extension

class pi(Cog_Extension):
    
    @commands.command()
    async def read(self, ctx):
        """讀取腳位的值"""
        pinValue11 = GPIO.input(11)
        pinValue13 = GPIO.input(13)
        pinValue15 = GPIO.input(15)
        pinValue16 = GPIO.input(16)
        await ctx.send('Pin 11 = {:d}\nPin 13 = {:d}\nPin 15 = {:d}\nPin 16 = {:d}'.format(pinValue11,pinValue13,pinValue15,pinValue16))
    
    @commands.command()
    async def light(self, ctx, inStr : str):
        """控制電燈(on/off)"""
        if inStr == 'on':
            GPIO.output(12, 1)
            await ctx.send('已開啟電燈')
        elif inStr == 'off':
            GPIO.output(12, 0)
            await ctx.send('已關閉電燈')
    
    @commands.command()
    async def temp(self, ctx):
        """回應當前溫度"""
        h, t = Adafruit_DHT.read_retry(11, 4)
        if t is not None:
            await ctx.send('現在溫度為: {:0.1f} ℃'.format(t))
        else:
            await ctx.send('無法讀取數值')
    
    @commands.command()
    async def humi(self, ctx):
        """回應當前濕度"""
        h, t = Adafruit_DHT.read_retry(11, 4)
        if h is not None:
            await ctx.send('現在濕度為: {:0.1f} %'.format(h))
        else:
            await ctx.send('無法讀取數值')

    """@commands.command()
    async def lcd_print(self, ctx, str1 : str, str2 = ''):
        \"""顯示文字在lcd上\"""
        lcd_print(str1 , str2, 1, 0)"""

def setup(bot):
    bot.add_cog(pi(bot))