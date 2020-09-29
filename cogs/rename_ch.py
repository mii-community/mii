from discord.ext import commands
import constant


class Rename_chCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rename(self, ctx, *, name: str):
        """あなたの部屋/スレッドをリネームします。"""
        if ctx.author.bot:
            return

        elif ctx.channel.category.id not in (constant.CAT_ROOM, constant.CAT_THREAD):
            await ctx.send("ここでは実行できません。")
            return

        user = await self.bot.database.fetch_row(
            constant.TABLE_NAME, channel_id=ctx.channel.id
        )
        if not user:
            user = await self.bot.database.fetchrow(
                """
                INSERT INTO mii (user_id, guild_id)
                     VALUES ($1, $2)
                  RETURNING *
                """,
                ctx.author.id,
                ctx.guild.id,
            )

        if not (
            ctx.channel.id == user["room_id"]
            and ctx.channel.topic == f"thread-author: {ctx.author.id}"
        ):
            await ctx.send("権限がありません。")
            return
        await ctx.channel.edit(name=name)
        await ctx.send(f"{ctx.author.mention} チャンネル名を {name} に上書きしました。")


def setup(bot):
    bot.add_cog(Rename_chCog(bot))
