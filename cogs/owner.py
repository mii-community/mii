import os
import traceback

import discord
from discord.ext import commands

import constant


class Owner(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="set")
    @commands.is_owner()
    async def db_set_room_id(
        self, ctx, channel: discord.TextChannel, member: discord.Member
    ):

        # データベースからデータをもらう
        ch_data = await self.bot.database.fetch_row(
            constant.TABLE_NAME, author_id=member.id, channel_type="room"
        )

        # データがなければ新規作成
        if not ch_data:
            await self.bot.database.insert(
                constant.TABLE_NAME,
                channel_id=channel.id,
                author_id=member.id,
                channel_type="room",
            )

        # データの上書き
        else:
            await self.bot.database.update(
                constant.TABLE_NAME,
                {"author_id": member.id},
                channel_id=channel.id,
                channel_type="room",
            )
        await ctx.send(f"{channel.mention}の所有者は{member.display_name}にセットされました。")
        await ctx.channel.set_permissions(
            member, manage_messages=True, manage_channels=True
        )


def setup(bot):
    bot.add_cog(Owner(bot))
