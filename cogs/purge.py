from discord.ext import commands


class PurgeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def purging(self, ctx, limit):
        if not ctx.author.permissions_in(ctx.channel).manage_messages:
            await ctx.send("メッセージ管理の権限がありません。")
            return
        await ctx.channel.purge(limit=limit)
        await ctx.send("✅")

    @commands.command(name="purge")
    async def purge_messages(self, ctx, num):
        """!purge <number> で指定された数のメッセージを一括削除します。"""
        if not num.isdecimal():
            await ctx.send("数値を入力してください。")
            return
        num = int(num)
        await self.purging(ctx, num + 1)

    @commands.command(name="purgeall")
    async def purge_all_messages(self, ctx):
        """全てのメッセージを一括削除します。"""
        await self.purging(ctx, None)


def setup(bot):
    bot.add_cog(PurgeCog(bot))
