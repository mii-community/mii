from discord import Message
from discord.ext.commands import Bot, Cog


class Nuoh(Cog):
    nuoh = ("ぬおー", "ヌオー", "nuoh", "nuo-")
    nuoh_king = ("ぬ王", "ヌ王", "ぬ・王", "ヌ・王")

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot:
            return
        if any(map(message.content.__contains__, self.nuoh)):
            await message.channel.send(
                "https://cdn.discordapp.com/attachments/752286472383758416/807988458290806854/unknown.png"
            )
            return
        elif any(map(message.content.__contains__, self.nuoh_king)):
            await message.channel.send(
                "https://cdn.discordapp.com/attachments/752286472383758416/811338296151638016/image0.png"
            )
            return


def setup(bot: Bot):
    bot.add_cog(Nuoh(bot))
