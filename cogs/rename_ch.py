from discord.ext import commands
import os
import launcher


class Rename_chCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rename(self, ctx, named):
        """あなたの部屋/スレッドをリネームします。"""
        if ctx.author.bot:
            return
        elif (ctx.channel.category.id != launcher.CAT_ROOM
                and ctx.channel.category.id != launcher.CAT_THREAD):
            await ctx.send("ここでは実行できません。")
            return

        user = await self.bot.datebase.fetchrow(
            """
            SELECT *
              FROM mii
             WHERE user_id = $1
               AND guild_id = $2
            """,
            ctx.author.id, ctx.guild.id
        )
        if not user:
            user = await self.bot.datebase.fetchrow(
                """
                INSERT INTO mii (user_id, guild_id)
                     VALUES ($1, $2)
                  RETURNING *
                """,
                ctx.author.id, ctx.guild.id
            )

        if (ctx.channel.id == user['room_id']
                or ctx.channel.topic == "thread-author: " + str(ctx.author.id)):
            await ctx.channel.edit(name=named)
            await ctx.send(f"{ctx.author.mention} チャンネル名を {named} に上書きしました。")
            return
        await ctx.send("権限がありません。")
        return


def setup(bot):
    bot.add_cog(Rename_chCog(bot))
