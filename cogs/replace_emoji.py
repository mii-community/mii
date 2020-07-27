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


def get_replaced_char(message, replace_char):
    if replace_char in constant.HIRAGANA_EMOJI:
        emoji_alias = constant.HIRAGANA_EMOJI[replace_char]
        emoji_id = get_emoji_id(message, emoji_alias)
        replaced_char = "<:" + emoji_alias + ":" + str(emoji_id) + ">"
        return replaced_char
    elif replace_char in constant.DAKUTEN_EMOJI:
        emoji_alias = constant.DAKUTEN_EMOJI[replace_char]
        emoji_id = get_emoji_id(message, emoji_alias)
        replaced_char = "<:" + emoji_alias + ":" + str(emoji_id) + ">" + "ﾞ "
        return replaced_char
    elif replace_char in constant.HANDAKUTEN_EMOJI:
        emoji_alias = constant.HANDAKUTEN_EMOJI[replace_char]
        emoji_id = get_emoji_id(message, emoji_alias)
        replaced_char = "<:" + emoji_alias + ":" + str(emoji_id) + ">" + "ﾟ "
        return replaced_char
    else:
        replaced_char = replace_char
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
