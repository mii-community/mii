from discord.ext import commands
import os

# consts
CAT_ROOM = int(os.getenv("CAT_ROOM", "702044270609170443"))
CAT_THREAD = int(os.getenv("CAT_THREAD", "662856289151615025"))


class Rename_chCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rename(self, ctx, named):
        """!rename <named> で自分の作成した部屋/スレッドをリネームします。"""
        if (ctx.channel.category.id != CAT_ROOM
                and ctx.channel.category.id != CAT_THREAD):
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
