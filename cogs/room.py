import os

import discord
from discord.ext import commands

import constant


class Room(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def open(self, ctx):
        """ルームマスターで使うことであなたの部屋を作成します。"""
        if ctx.author.bot:
            return
        elif ctx.channel.id != constant.CH_ROOM_MASTER:
            await ctx.send("ここでは実行できません。")
            return

        ch_data = await self.bot.database.fetch_row(
            constant.TABLE_NAME, author_id=ctx.author.id, channel_type="room"
        )

        creator = ctx.guild.get_member(ctx.author.id)
        cat_room = self.bot.get_channel(constant.CAT_ROOM)
        # ルームを持っていない場合
        if not ch_data:
            name = f"{ctx.author.display_name}の部屋"
            new_room = await cat_room.create_text_channel(name=name)
            await new_room.set_permissions(
                creator, manage_messages=True, manage_channels=True
            )
            await ctx.send(f"{ctx.author.mention} {new_room.mention} を作成しました。")
            await self.bot.database.insert(
                constant.TABLE_NAME,
                channel_id=new_room.id,
                author_id=ctx.author.id,
                channel_type="room",
            )
            return

        ch_room = self.bot.get_channel(ch_data["channel_id"])
        cat_room_archive = self.bot.get_channel(constant.CAT_ROOM_ARCHIVE)
        # ルームカテゴリーにある場合
        if ch_room.category == cat_room:
            text = "あなたの部屋はもう作られています。"
        # アーカイブカテゴリーにある場合
        elif ch_room.category == cat_room_archive:
            text = "をアーカイブから戻しました。"
            role_member = ctx.guild.get_role(constant.ROLE_MEMBER)
            await ch_room.edit(category=cat_room)
            await ch_room.edit(sync_permissions=True)
            await ch_room.set_permissions(
                creator, manage_messages=True, manage_channels=True
            )
        # おわりに
        await ctx.send(f"{ctx.author.mention} {ch_room.mention} {text}")


def setup(bot):
    bot.add_cog(Room(bot))
