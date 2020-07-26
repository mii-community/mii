import os

import discord
from discord.ext import commands

import launcher


class Room(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def open(self, ctx):
        """スレッドマスターで使うことであなたの部屋を作成します。"""
        if ctx.author.bot:
            return
        elif ctx.channel.id != launcher.CH_ROOM_MASTER:
            await ctx.send("ここでは実行できません。")
            return

        user = await self.bot.datebase.fetchrow(
            """
            SELECT *
              FROM mii
             WHERE user_id = $1
               AND guild_id = $2
            """,
            ctx.author.id,
            ctx.guild.id,
        )
        if not user:
            user = await self.bot.datebase.fetchrow(
                """
                INSERT INTO mii (user_id, guild_id)
                     VALUES ($1, $2)
                  RETURNING *
                """,
                ctx.author.id,
                ctx.guild.id,
            )

        cat_room = self.bot.get_channel(launcher.CAT_ROOM)
        cat_room_archive = self.bot.get_channel(launcher.CAT_ROOM_ARCHIVE)
        role_member = ctx.guild.get_role(launcher.ROLE_MEMBER)
        role_archive = ctx.guild.get_role(launcher.ROLE_ARCHIVE)
        creator = ctx.guild.get_member(ctx.author.id)
        except_flag = True

        async def new_room():
            named = f"{ctx.author.display_name}の部屋"
            new_room = await cat_room.create_text_channel(name=named)
            await new_room.set_permissions(
                creator, manage_messages=True, manage_channels=True
            )
            await ctx.send(f"{ctx.author.mention} {new_room.mention} を作成しました。")
            await self.bot.datebase.execute(
                """
                UPDATE mii
                   SET room_id = $1
                 WHERE user_id = $2
                   AND guild_id = $3
                """,
                new_room.id,
                ctx.author.id,
                ctx.guild.id,
            )
            return

        # ルームを持っていない場合: 新規作成
        if not user["room_id"]:
            await new_room()

        for channel in ctx.guild.channels:
            if (
                channel.category != cat_room and channel.category != cat_room_archive
            ) or (channel.id != user["room_id"]):
                continue

            # ルームカテゴリーにある場合
            if channel.category == cat_room:
                await ctx.send(
                    f"{ctx.author.mention} {channel.mention} あなたの部屋はもう作られています。"
                )
                except_flag = False
                return

            # アーカイブカテゴリーにある場合
            elif channel.category == cat_room_archive:
                await channel.edit(category=cat_room)
                await channel.set_permissions(role_archive, overwrite=None)
                await channel.set_permissions(role_member, read_messages=True)
                await channel.set_permissions(
                    creator, manage_messages=True, manage_channels=True
                )
                await ctx.send(f"{ctx.author.mention} {channel.mention} をアーカイブから戻しました。")
                except_flag = False
                return

        # 例外: 新規作成
        if except_flag:
            await new_room()


def setup(bot):
    bot.add_cog(Room(bot))
