import os
import traceback

import constant
import discord
from discord.ext import commands


class Owner(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="room")
    @commands.is_owner()
    async def db_set_room_id(
        self, ctx, member: discord.Member, channel: discord.TextChannel = None
    ):
        if channel is None:
            channel = ctx.channel
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
        await ctx.channel.edit(sync_permissions=True)
        await ctx.channel.set_permissions(
            member, manage_messages=True, manage_channels=True
        )

    @commands.command(name="thread")
    @commands.is_owner()
    async def db_set_thread_id(
        self, ctx, member: discord.Member, channel: discord.TextChannel = None
    ):
        if channel is None:
            channel = ctx.channel
        # データベースからデータをもらう
        ch_data = await self.bot.database.fetch_row(
            constant.TABLE_NAME, channel_id=channel.id
        )

        # データがなければ新規作成
        if not ch_data:
            await self.bot.database.insert(
                constant.TABLE_NAME,
                channel_id=channel.id,
                author_id=member.id,
                channel_type="thread",
            )

        # データの上書き
        else:
            await self.bot.database.update(
                constant.TABLE_NAME,
                {"author_id": member.id},
                channel_id=channel.id,
                channel_type="thread",
            )
        await ctx.send(f"{channel.mention}の所有者は{member.display_name}にセットされました。")

    @commands.command(name="rcce")
    @commands.is_owner()
    async def reset_count_custom_emoji(self, ctx):
        await self.bot.database.delete_all(constant.COUNT_EMOJI)
        await ctx.send("カスタム絵文字のカウントをリセットしました。")


def setup(bot):
    bot.add_cog(Owner(bot))
