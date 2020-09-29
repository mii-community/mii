import os

import discord
from discord.ext import commands

import constant


class ThreadCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def set_admin(self, author_id, channel_id):
        await self.bot.database.execute(
            """
            INSERT INTO mii_channels (channel_id, author_id, channel_type)
                 VALUES ($1, $2, $3)
              RETURNING *
            """,
            channel_id,
            author_id,
            "thread",
        )
        return

    async def update_admin(self, author_id, channel_id):
        await self.bot.database.execute(
            """
            UPDATE mii_channels
               SET author_id = $1
             WHERE channel_id = $2
               AND channel_type = $3
            """,
            author_id,
            channel_id,
            "thread",
        )
        return

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.channel.category.id != constant.CAT_THREAD:
            return

        elif message.channel.id != constant.CH_THREAD_MASTER:
            position = self.bot.get_channel(constant.CH_THREAD_MASTER).position + 1
            await message.channel.edit(position=position)
            return

        # 簡易的なCH名の重複チェック
        name = message.content
        ch_thread = discord.utils.get(message.guild.channels, name=name)
        cat_thread = self.bot.get_channel(constant.CAT_THREAD)
        # 同名CHがない場合
        if not ch_thread:
            new_thread = await cat_thread.create_text_channel(name=name)
            await message.channel.send(
                f"{message.author.mention} {new_thread.mention} を作成しました。"
            )
            await self.set_admin(message.author.id, new_thread.id)
            return

        # 同名CHがスレッドカテゴリーにある場合
        if ch_thread.category.id == constant.CAT_THREAD:
            text = "はもう作られています。"
        # 同名CHがアーカイブカテゴリーにある場合
        elif ch_thread.category.id == constant.CAT_THREAD_ARCHIVE:
            text = "をアーカイブから戻しました。"
            role_archive = message.guild.get_role(constant.ROLE_ARCHIVE)
            role_member = message.guild.get_role(constant.ROLE_MEMBER)
            await ch_thread.edit(category=cat_thread)
            await ch_thread.set_permissions(role_archive, overwrite=None)
            await ch_thread.set_permissions(role_member, read_messages=True)
            await self.update_admin(message.author.id, ch_thread.id)
        # おわりに
        await message.channel.send(
            f"{message.author.mention} {ch_thread.mention} {text}"
        )


def setup(bot):
    bot.add_cog(ThreadCog(bot))
