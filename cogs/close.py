from discord.ext import commands
import discord
import os

# consts
CH_ROOM_MASTER = int(os.getenv("CH_ROOM_MASTER", "702042912338346114"))
CAT_ROOM = int(os.getenv("CAT_ROOM", "702044270609170443"))
CAT_ROOM_ARCHIVE = int(os.getenv("CAT_THREAD_ARCHIVE", "711058666387800135"))
CH_THREAD_MASTER = int(os.getenv("CH_THREAD_MASTER", "702030388033224714"))
CAT_THREAD = int(os.getenv("CAT_THREAD", "662856289151615025"))
CAT_THREAD_ARCHIVE = int(os.getenv("CAT_THREAD_ARCHIVE", "702074011772911656"))
MEMBER_ROLE_NAME = str(os.getenv("MEMBER_ROLE_NAME", "member"))
ARCHIVE_ROLE_NAME = str(os.getenv("ARCHIVE_ROLE_NAME", "view archive"))


class CloseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def close(self, ctx):
        if ctx.author.bot:
            return
        elif (ctx.channel.category.id != CAT_ROOM
                and ctx.channel.category.id != CAT_THREAD):
            await ctx.send("ここでは実行できません。")
            return
        elif (ctx.channel.topic != "room-author: " + str(ctx.author.id)
                and ctx.channel.topic != "thread-author: " + str(ctx.author.id)
                and (not ctx.author.guild_permissions.administrator)):
            await ctx.send("権限がありません。")
            return
        elif ctx.channel.category.id == CAT_ROOM:
            await ctx.channel.edit(category=self.bot.get_channel(CAT_ROOM_ARCHIVE))
        elif ctx.channel.category.id == CAT_THREAD:
            await ctx.channel.edit(category=self.bot.get_channel(CAT_THREAD_ARCHIVE))
        role = discord.utils.get(ctx.guild.roles, name=MEMBER_ROLE_NAME)
        await ctx.channel.set_permissions(role, overwrite=None)
        role = discord.utils.get(ctx.guild.roles, name=ARCHIVE_ROLE_NAME)
        await ctx.channel.set_permissions(role, read_messages=True, send_messages=False)


def setup(bot):
    bot.add_cog(CloseCog(bot))
