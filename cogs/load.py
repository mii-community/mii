from discord.ext import commands
import os
import traceback

class Load(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Load(bot))
