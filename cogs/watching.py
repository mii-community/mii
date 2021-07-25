from discord import Message
from discord.ext.commands import Bot, Cog

from constant import EMOJI_MII_PEEKING


class Watching(Cog):
    __slots__ = "bot"

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message):
        if "みぃ様" not in message.content:
            return
        await message.add_reaction(EMOJI_MII_PEEKING)


def setup(bot: Bot):
    bot.add_cog(Watching(bot))
