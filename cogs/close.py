from discord.ext import commands
import discord
import launcher

class CloseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def close(self, ctx):
        if ctx.author.bot:
            return
        elif (ctx.channel.category.id != launcher.CAT_ROOM
                and ctx.channel.category.id != launcher.CAT_THREAD):
            await ctx.send("ここでは実行できません。")
            return
        elif (ctx.channel.topic != "room-author: " + str(ctx.author.id)
                and ctx.channel.topic != "thread-author: " + str(ctx.author.id)
                and (not ctx.author.guild_permissions.administrator)):
            await ctx.send("権限がありません。")
            return
        elif ctx.channel.category.id == launcher.CAT_ROOM:
            await ctx.channel.edit(category=self.bot.get_channel(launcher.CAT_ROOM_ARCHIVE))
        elif ctx.channel.category.id == launcher.CAT_THREAD:
            await ctx.channel.edit(category=self.bot.get_channel(launcher.CAT_THREAD_ARCHIVE))
        role = ctx.guild.get_role(launcher.ROLE_MEMBER)
        await ctx.channel.set_permissions(role, overwrite=None)
        role = ctx.guild.get_role(launcher.ROLE_ARCHIVE)
        await ctx.channel.set_permissions(role, read_messages=True, send_messages=False)


def setup(bot):
    bot.add_cog(CloseCog(bot))
