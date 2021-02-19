import constant
from discord.ext.commands import Bot, Cog


# とりあえずスレッドだけ。
# こちらも 10 分間に 2 回ずつ更新されるみたい。
class ShowNumberChannels(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.category_ids = (constant.CAT_THREAD, constant.CAT_THREAD_ARCHIVE)

    async def update_category_name(self, channel):
        if channel.category.id == constant.CAT_THREAD:
            await channel.category.edit(
                name=f"THREAD ─ {len(channel.category.channels)}"
            )
            return
        if channel.category.id == constant.CAT_THREAD_ARCHIVE:
            await channel.category.edit(
                name=f"📜 THREAD ─ {len(channel.category.channels)}"
            )
            return

    @Cog.listener()
    async def on_guild_channel_create(self, channel):
        if channel.category is None or not channel.category.id in self.category_ids:
            return
        await self.update_category_name(channel)

    @Cog.listener()
    async def on_guild_channel_delete(self, channel):
        if channel.category is None or not channel.category.id in self.category_ids:
            return
        await self.update_category_name(channel)


def setup(bot: Bot):
    bot.add_cog(ShowNumberChannels(bot))
