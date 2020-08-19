from discord.ext import commands
import discord
import os
import launcher


class TweetCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.category.id != launcher.CH_TWEET:
            return


def setup(bot):
    bot.add_cog(TweetCog(bot))
