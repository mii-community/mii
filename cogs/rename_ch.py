from discord.ext import commands
import os
import launcher


class Rename_chCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rename(self, ctx, named):
        if (ctx.channel.category.id != launcher.CAT_ROOM
                and ctx.channel.category.id != launcher.CAT_THREAD):
            await ctx.send("ここでは実行できません。")
            return
        elif (ctx.channel.topic != "room-author: " + str(ctx.author.id)
                and ctx.channel.topic != "thread-author: " + str(ctx.author.id)
                and (not ctx.author.guild_permissions.administrator)):
            await ctx.send("権限がありません。")
            return
        await ctx.channel.edit(name=named)
        await ctx.send(f"{ctx.author.mention} チャンネル名を {named} に上書きしました。")


def setup(bot):
    bot.add_cog(Rename_chCog(bot))
