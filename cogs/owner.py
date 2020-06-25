from discord.ext import commands
import os
import traceback



class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Owner(bot))
