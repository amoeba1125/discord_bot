import discord
from discord.ext import commands
import RPi.GPIO as GPIO
import os
import core.global_variables

TOKEN = '*********************************'
description = '''Discord bot in Python'''

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(12, GPIO.OUT) #LED腳位
GPIO.setup(11, GPIO.IN) #按鈕腳位
GPIO.setup(13, GPIO.IN) #按鈕腳位
GPIO.setup(15, GPIO.IN) #按鈕腳位
GPIO.setup(16, GPIO.IN) #按鈕腳位

core.global_variables._init()
bot = commands.Bot(command_prefix='.', description=description)
core.global_variables.set_value('bot', bot)

@bot.event
async def on_ready():
    print('Logged in as:', end='')
    print(bot.user.name)
    print('User id:', end='')
    print(bot.user.id)
    print('------')

@bot.command()
async def load(ctx, extension):
    """載入 extension"""
    bot.load_extension(F'cmds.{extension}')
    await ctx.send(F'已載入{extension}')
    
@bot.command()
async def unload(ctx, extension):
    """卸除 extension"""
    bot.unload_extension(F'cmds.{extension}')
    await ctx.send(F'已卸除{extension}')
    
@bot.command()
async def reload(ctx, extension):
    """重載 extension"""
    bot.reload_extension(F'cmds.{extension}')
    await ctx.send(F'已重載{extension}')
    
for filename in os.listdir('./cmds'):
    if filename.endswith('.py') and not(filename.startswith('__')):
        bot.load_extension(F'cmds.{filename[:-3]}')
        
if __name__ == "__main__":
    bot.run(TOKEN)
