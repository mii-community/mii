from discord.ext import commands


class PurgeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def purge(self, ctx, limit):
        """!purge <number> で指定された数のメッセージを一括削除します。"""
        channel = ctx.channel
        if not ctx.author.permissions_in(channel).manage_messages:
            await channel.send("メッセージ管理の権限がありません。")
            return
        if limit == "all":
            await channel.purge(limit=None)
            await ctx.send("✅")
            return
        try:
            limit = int(limit)
        except:
            await channel.send("不正な引数です。削除するメッセージ数か、全て削除する場合はallを入力してください。")
            return
        await channel.purge(limit=limit)
        await ctx.send("✅")


def setup(bot):
    bot.add_cog(PurgeCog(bot))
