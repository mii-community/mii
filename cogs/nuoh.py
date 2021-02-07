from discord import Message
from discord.ext.commands import Bot, Cog


class Nuoh(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message):
        nuoh = ("ぬおー", "ヌオー", "nuoh", "nuo-")
        if not any(map(message.content.__contains__, nuoh)):
            return
        await message.channel.send(
            "https://cdn.discordapp.com/attachments/752286472383758416/807988458290806854/unknown.png"
        )


def setup(bot: Bot):
    bot.add_cog(Nuoh(bot))
