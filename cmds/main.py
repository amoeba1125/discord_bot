import discord
import sys
import time
from discord.ext import commands
sys.path.append("..")
from core.classes import Cog_Extension
sys.path.append("..")
from core.lcd import lcd_print

class main(Cog_Extension):

    @commands.command()
    async def add(self, ctx, left : float, right : float):
        """相加兩個數字"""
        subResult = left + right
        result : int = int(subResult)
        if(result == subResult):
            await ctx.send(int(subResult))
        else:
            await ctx.send(subResult)

    @commands.command()
    async def sub(self, ctx, left : float, right : float):
        """將左邊數字減去右邊數字"""
        subResult = left - right
        result : int = int(subResult)
        if(result == subResult):
            await ctx.send(int(subResult))
        else:
            await ctx.send(subResult)

    @commands.command()
    async def echo(self, ctx, *inStr : str):
        """回應輸入的內容"""
        outStr = ''
        for n in range(len(inStr)):
            outStr = outStr + inStr[n] + ' '
        await ctx.send(outStr)
        
    @commands.command()
    async def date(self, ctx):
        """回應當前日期"""
        await ctx.send("{}".format(time.strftime("%Y 年 %m 月 %d 日")))
        
    @commands.command()
    async def time(self, ctx):
        """回應當前時間"""
        await ctx.send("{}".format(time.strftime("%H 點 %M 分 %S 秒")))
    
    @commands.command()
    async def debug(self, ctx, str1 ,str2 = ''):
        """用於debug"""
        self.channel = self.bot.get_channel(660656251843379243)
        lcd_print(str1 , str2, 1, 0)
        await self.channel.send(self)
        
def setup(bot):
    bot.add_cog(main(bot))