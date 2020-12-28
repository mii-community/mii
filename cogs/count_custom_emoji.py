import re

import constant
import emoji
from discord.ext import commands

pattern = re.compile(r"<:(\w+):(\d+)>")


class CountCustomEmojiCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_data_from_db(self, emoji_data):
        return await self.bot.database.fetch_row(constant.COUNT_EMOJI, data=emoji_data)

    async def update_count_custom_emoji(self, data, emoji_data):
        await self.bot.database.update(
            constant.COUNT_EMOJI,
            {"count": data["count"] + 1},
            data=emoji_data,
        )

    async def insert_count_custom_emoji(self, emoji_data):
        await self.bot.database.insert(
            constant.COUNT_EMOJI,
            data=emoji_data,
            count=1,
        )

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        response = pattern.finditer(message.content)
        for match_custom_emoji in response:
            emoji_data = str(match_custom_emoji.group())
            data = await self.get_data_from_db(emoji_data)
            if data:
                await self.update_count_custom_emoji(data, emoji_data)
                continue
            await self.insert_count_custom_emoji(emoji_data)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction):
        if reaction.emoji.name in emoji.UNICODE_EMOJI:
            return

        emoji_data = str(reaction.emoji)
        data = await self.get_data_from_db(emoji_data)
        if data:
            await self.update_count_custom_emoji(data, emoji_data)
            return
        await self.insert_count_custom_emoji(emoji_data)

    @commands.command(name="scce")
    async def show_count_custom_emoji(self, ctx):
        """カスタム絵文字の使用回数を表示します。"""
        response = await self.bot.database.fetch_all(constant.COUNT_EMOJI, "ORDER BY count desc")
        content = "カスタム絵文字のカウント\n"
        for i, data in enumerate(response):
            emoji_data = data["data"]
            count = data["count"]
            if not self.bot.get_emoji(int(pattern.match(emoji_data).group(2))):
                continue
            if (i + 1) % 4 == 0:
                content += f"{emoji_data}：**{count}**\n"
                continue
            content += f"{emoji_data}：**{count}**　　"
        await ctx.send(content)


def setup(bot):
    bot.add_cog(CountCustomEmojiCog(bot))
