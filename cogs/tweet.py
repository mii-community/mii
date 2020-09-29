import os

import discord
from discord.ext import commands

import constant


class TweetCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # つぶやきchのログを、古いものから、指定件数分までだけが残るように削除
        if message.channel.id != constant.CH_TWEET:
            return

        messages = await message.channel.history().flatten()

        # 残すメッセージ数を指定
        limit = 15

        # 指定件数以下ならば無視
        delete_messages = messages[limit:]

        # BOT停止などで複数件更新されていた場合やerror:unknown messageなどの対策も含めてリスト化してから削除

        await self.bot.get_channel(constant.CH_TWEET).delete_messages(delete_messages)


def setup(bot):
    bot.add_cog(TweetCog(bot))
