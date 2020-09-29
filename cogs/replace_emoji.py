import unicodedata

import discord
from discord.ext import commands

import constant


async def check_webhook(message):
    webhooks = await message.channel.webhooks()
    if not webhooks:
        webhook = await message.channel.create_webhook(name=constant.WEBHOOK_NAME)
        return webhook
    for webhook in webhooks:
        if webhook.name == constant.WEBHOOK_NAME:
            return webhook
    webhook = await message.channel.create_webhook(name=constant.WEBHOOK_NAME)
    return webhook


def get_emoji_id(message, emoji_alias):
    get_emoji = discord.utils.get(message.guild.emojis, name=emoji_alias)
    emoji_id = get_emoji.id
    return emoji_id


def get_replaced_char(message, char):
    other_dict = {"309A": "ﾟ ", "3099": "ﾞ "}

    if ligature := unicodedata.decomposition(char):
        seion, other = ligature.split()
        if other not in other_dict:
            return char
        pure_char = (r"\u" + seion).encode().decode("unicode-escape")
        emoji_alias = constant.HIRAGANA_EMOJI.get(pure_char)
    elif emoji_alias := constant.HIRAGANA_EMOJI.get(char):
        other = None
    else:
        return char

    emoji_id = get_emoji_id(message, emoji_alias)
    replaced_char = "<:" + emoji_alias + ":" + str(emoji_id) + ">"
    replaced_char += other_dict[other] if other else ""
    return replaced_char


class Replace_emojiCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def emoji(self, ctx, replace_string):
        """!emoji <text> でテキストをサポート済みの絵文字に置き換えます。"""
        webhook = await check_webhook(ctx)
        replaced_string = []
        for replace_char in replace_string:
            replaced_char = get_replaced_char(ctx, replace_char)
            replaced_string.append(replaced_char)
        content = ">>> " + "".join(replaced_string)
        await ctx.message.delete()
        await webhook.send(
            avatar_url=ctx.author.avatar_url,
            username=ctx.author.display_name,
            content=content,
        )


def setup(bot):
    bot.add_cog(Replace_emojiCog(bot))
