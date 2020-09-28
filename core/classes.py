import discord
from discord.ext import commands
import os

class Cog_Extension(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
