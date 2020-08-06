from discord.ext import commands
import discord
import os
import constant


class Room(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def open(self, ctx):
        """スレッドマスターで使うことであなたの部屋を作成します。"""
        if ctx.author.bot:
            return
        elif ctx.channel.id != constant.CH_ROOM_MASTER:
            await ctx.send("ここでは実行できません。")
            return

        ch_data = await self.bot.database.fetchrow(
            """
            SELECT *
              FROM mii_channels
             WHERE author_id = $1
               AND channel_type = $2
            """,
            ctx.author.id, "room"
        )

        creator = ctx.guild.get_member(ctx.author.id)
        cat_room = self.bot.get_channel(constant.CAT_ROOM)
        # ルームを持っていない場合
        if not ch_data:
            name = f"{ctx.author.display_name}の部屋"
            new_room = await cat_room.create_text_channel(name=name)
            await new_room.set_permissions(creator, manage_messages=True, manage_channels=True)
            await ctx.send(f"{ctx.author.mention} {new_room.mention} を作成しました。")
            await self.bot.database.execute(
                """
                INSERT INTO mii_channels (channel_id, author_id, channel_type)
                     VALUES ($1, $2, $3)
                  RETURNING *
                """,
                new_room.id, ctx.author.id, "room"
            )
            return

        ch_room = self.bot.get_channel(ch_data['channel_id'])
        cat_room_archive = self.bot.get_channel(constant.CAT_ROOM_ARCHIVE)
        # ルームカテゴリーにある場合
        if ch_room.category == cat_room:
            text = "あなたの部屋はもう作られています。"
        # アーカイブカテゴリーにある場合
        elif ch_room.category == cat_room_archive:
            text = "をアーカイブから戻しました。"
            role_member = ctx.guild.get_role(constant.ROLE_MEMBER)
            role_archive = ctx.guild.get_role(constant.ROLE_ARCHIVE)
            await ch_room.edit(category=cat_room)
            await ch_room.set_permissions(role_archive, overwrite=None)
            await ch_room.set_permissions(role_member, read_messages=True)
            await ch_room.set_permissions(creator, manage_messages=True, manage_channels=True)
        # おわりに
        await ctx.send(f"{ctx.author.mention} {ch_room.mention} {text}")


def setup(bot):
    bot.add_cog(Room(bot))
