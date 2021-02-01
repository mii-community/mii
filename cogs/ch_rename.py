import constant
from discord.ext.commands import Bot, Cog, Context, command


class CHRename(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command()
    async def rename(self, ctx: Context, *, name: str):
        """あなたの部屋/スレッドをリネームします。"""
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
        if data_ch["author_id"] != author.id:
            await ctx.send("自分のチャンネルでのみ使えます。")
            return
        await channel.edit(name=name)
        await ctx.send(f"{author.mention} チャンネル名を {name} に上書きしました。")


def setup(bot: Bot):
    bot.add_cog(CHRename(bot))
