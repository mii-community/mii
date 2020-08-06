from discord.ext import commands
import os
import traceback
import discord


class Owner(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="set")
    @commands.is_owner()
    async def db_set_room_id(self, ctx, channel: discord.TextChannel, member: discord.Member):

        # データベースからデータをもらう
        ch_data = await self.bot.database.fetchrow(
            """
            SELECT *
              FROM mii_channels
             WHERE author_id = $1
               AND channel_type = $2
            """,
            member.id, "room"
        )

        # データがなければ新規作成
        if not ch_data:
            ch_data = await self.bot.database.execute(
                """
                INSERT INTO mii_channels (channel_id, author_id, channel_type)
                     VALUES ($1, $2, $3)
                  RETURNING *
                """,
                channel.id, member.id, "room"
            )

        # データの上書き
        elif ch_data:
            await self.bot.database.execute(
                """
                UPDATE mii
                   SET author_id = $1
                 WHERE channel_id = $2
                   AND channel_type = $3
                """,
                member.id, channel.id, "room"
            )
        await ctx.send(f"{channel.mention}の所有者は{member.display_name}にセットされました。")
        await ctx.channel.set_permissions(member, manage_messages=True, manage_channels=True)


def setup(bot):
    bot.add_cog(Owner(bot))
