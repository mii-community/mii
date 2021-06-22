from time import monotonic

from discord.ext.commands import Bot, Cog, Context, command


class Ping(Cog):
    __slots__ = "bot"

    def __init__(self, bot: Bot):
        self.bot = bot

    @command()
    async def ping(self, ctx: Context):
        tmp = monotonic()
        reply = await ctx.reply("計算中...")
        latency = (monotonic() - tmp) * 1000
        await reply.edit(content=f"Pong! 応答時間は **{int(latency)}** ms です。")


def setup(bot: Bot):
    bot.add_cog(Ping(bot))
