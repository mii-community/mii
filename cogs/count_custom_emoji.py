import re

import constant
import emoji
from discord import Message
from discord.ext.commands import Bot, Cog, Context, command

pattern = re.compile(r"<:(\w+):(\d+)>")


class CountCustomEmoji(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    def emoji_of_mii(self, emoji_id: int):
        return self.bot.get_emoji(emoji_id)

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

    @Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot:
            return

        response = pattern.finditer(message.content)
        for match_custom_emoji in response:
            if not self.emoji_of_mii(int(match_custom_emoji.group(2))):
                continue
            emoji_data = str(match_custom_emoji.group())
            data = await self.get_data_from_db(emoji_data)
            if data:
                await self.update_count_custom_emoji(data, emoji_data)
                continue
            await self.insert_count_custom_emoji(emoji_data)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction):
        emoji = reaction.emoji
        if emoji.name in emoji.UNICODE_EMOJI:
            return

        emoji_data = str(emoji)
        if not self.emoji_of_mii(int(pattern.match(emoji_data).group(2))):
            return

        data = await self.get_data_from_db(emoji_data)
        if data:
            await self.update_count_custom_emoji(data, emoji_data)
            return
        await self.insert_count_custom_emoji(emoji_data)

    @command(name="scce")
    async def show_count_custom_emoji(self, ctx: Context):
        """カスタム絵文字の使用回数を表示します。"""
        response = await self.bot.database.fetch_all(
            constant.COUNT_EMOJI, "ORDER BY count desc"
        )
        content = "カスタム絵文字のカウント\n"
        i = 1
        for data in response:
            emoji_data = data["data"]
            count = data["count"]
            if not self.bot.get_emoji(int(pattern.match(emoji_data).group(2))):
                await self.bot.database.delete_row(
                    constant.COUNT_EMOJI, data=emoji_data
                )
                continue
            if i % 4 == 0:
                content += f"{emoji_data}：**{count}**\n"
                if len(content) > 1500:
                    await ctx.send(content)
                    content = ""
                i += 1
                continue
            content += f"{emoji_data}：**{count}**　　"
            i += 1

        await ctx.send(content)


def setup(bot: Bot):
    bot.add_cog(CountCustomEmoji(bot))
