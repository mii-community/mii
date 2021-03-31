import constant
from discord import Message
from discord.ext.commands import Bot, Cog


class Tweet(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message):
        if message.channel.id != constant.CH_TWEET:
            return
        messages = await message.channel.history().flatten()
        await message.channel.delete_messages(messages[25:])


def setup(bot: Bot):
    bot.add_cog(Tweet(bot))
