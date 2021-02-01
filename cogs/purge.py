from discord.ext.commands import Bot, Cog, Context, command


class Purge(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def purging(self, ctx: Context, limit):
        if not ctx.author.permissions_in(ctx.channel).manage_messages:
            await ctx.send("メッセージ管理の権限がありません。")
            return
        await ctx.channel.purge(limit=limit)
        await ctx.send("✅", delete_after=10)

    @command(name="purge")
    async def purge_messages(self, ctx: Context, num):
        """!purge <num> で指定された数のメッセージを一括削除します。"""
        if not num.isdecimal():
            await ctx.send("数値を入力してください。")
            return
        await self.purging(ctx, int(num) + 1)

    @command(name="purgeall")
    async def purge_all_messages(self, ctx: Context):
        """全てのメッセージを一括削除します。"""
        await self.purging(ctx, None)


def setup(bot: Bot):
    bot.add_cog(Purge(bot))
