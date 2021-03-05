from random import choice, sample

from discord import AllowedMentions
from discord.ext.commands import Bot, Cog, Context, command


class Entrust(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(aliases=["p", "random", "choice", "dice"])
    async def pick(self, ctx: Context, *args):
        result = choice(args)
        await ctx.send(result, allowed_mentions=AllowedMentions.none())

    @command(aliases=["o"])
    async def order(self, ctx: Context, *args):
        result = " ".join(sample(args, len(args)))
        await ctx.send(result, allowed_mentions=AllowedMentions.none())


def setup(bot: Bot):
    bot.add_cog(Entrust(bot))
