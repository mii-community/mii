from discord.ext import commands
import discord
import os
import constant


class TweetCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # つぶやきchのログを、古いものから、指定件数分までだけが残るように削除
        if message.channel.id != constant.CH_TWEET:
            return

        # メッセージ数(num)を取得
        num = 0
        async for msg in message.channel.history():
            num += 1

        # 残すメッセージ数を指定
        log = 15

        # 指定件数以下ならば無視
        if num < log:
            return

        # BOT停止などで複数件更新されていた場合やerror:unknown messageなどの対策も含めてリスト化してから削除
        arrayMsg = []
        async for msg in message.channel.history(limit=num - log, oldest_first=True):
            arrayMsg.append(msg)
        await self.bot.get_channel(constant.CH_TWEET).delete_messages(arrayMsg)


def setup(bot):
    bot.add_cog(TweetCog(bot))
