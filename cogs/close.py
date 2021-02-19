import constant
from discord.ext.commands import Bot, Cog, Context, command


class Close(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command()
    async def close(self, ctx: Context):
        """自分の作成した部屋/スレッドをアーカイブします。"""
        author = ctx.author
        if author.bot:
            return
        channel = ctx.channel
        if not channel.category.id in (constant.CAT_ROOM, constant.CAT_THREAD):
            await ctx.send("ここでは実行できません。")
            return
        data_ch = await self.bot.database.fetch_row(
            constant.TABLE_NAME, channel_id=channel.id
        )
        if data_ch is None:
            await ctx.send("データが存在しませんでした。")
            return
        elif not (
            author.id == data_ch["author_id"]
            or author.permissions_in(channel).administrator
        ):
            await ctx.send("権限がありません。")
            return

        if channel.category.id == constant.CAT_ROOM:
            goto_cat = self.bot.get_channel(constant.CAT_ROOM_ARCHIVE)
        elif channel.category.id == constant.CAT_THREAD:
            goto_cat = self.bot.get_channel(constant.CAT_THREAD_ARCHIVE)
            await channel.category.edit(
                name=f"THREAD ─ {len(channel.category.channels)}"
            )
            await goto_cat.edit(name=f"📜 THREAD ─ {len(goto_cat.channels)}")
        await channel.edit(category=goto_cat)
        await channel.edit(sync_permissions=True)


def setup(bot: Bot):
    bot.add_cog(Close(bot))
