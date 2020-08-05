from discord.ext import commands
import discord


# consts
emojis_main = {
    "あ": "99_aa", "い": "98_ii", "う": "97_uu", "え": "96_ee", "お": "95_oo",
    "か": "94_ka", "き": "93_ki", "く": "92_ku", "け": "91_ke", "こ": "90_ko",
    "さ": "89_sa", "し": "88_si", "す": "87_su", "せ": "86_se", "そ": "85_so",
    "た": "84_ta", "ち": "83_ti", "つ": "82_tu", "て": "81_te", "と": "80_to",
    "な": "79_na", "に": "78_ni", "ぬ": "77_nu", "ね": "76_ne", "の": "75_no",
    "は": "74_ha", "ひ": "73_hi", "ふ": "72_hu", "へ": "71_he", "ほ": "70_ho",
    "ま": "69_ma", "み": "68_mi", "む": "67_mu", "め": "66_me", "も": "65_mo",
    "や": "64_ya", "ゆ": "63_yu", "よ": "62_yo",
    "ら": "61_ra", "り": "60_ri", "る": "59_ru", "れ": "58_re", "ろ": "57_ro",
    "わ": "56_wa", "を": "55_wo",
    "ん": "54_nn",
    "ぁ": "53_la", "ぃ": "52_li", "ぅ": "51_lu", "ぇ": "50_le", "ぉ": "49_lo",
    "っ": "48_ltu",
    "ゃ": "47_lya", "ゅ": "46_lyu", "ょ": "45_lyo",
    "〜": "44_nobasi", "ー": "44_nobasi",
    "！": "43_exclamation", "!": "43_exclamation",
    "？": "42_question", "?": "42_question",
    "、": "41_touten", ",": "41_touten",
    "。": "40_kuten", ".": "40_kuten"
}

emojis_sub1 = {
    "が": "94_ka", "ぎ": "93_ki", "ぐ": "92_ku", "げ": "91_ke", "ご": "90_ko",
    "ざ": "89_sa", "じ": "88_si", "ず": "87_su", "ぜ": "86_se", "ぞ": "85_so",
    "だ": "84_ta", "ぢ": "83_ti", "づ": "82_tu", "で": "81_te", "ど": "80_to",
    "ば": "74_ha", "び": "73_hi", "ぶ": "72_hu", "べ": "71_he", "ぼ": "70_ho",
}

emojis_sub2 = {
    "ぱ": "74_ha", "ぴ": "73_hi", "ぷ": "72_hu", "ぺ": "71_he", "ぽ": "70_ho",
}


async def get_webhook(message):
    webhooks = await message.channel.webhooks()
    for webhook in webhooks:
        if webhook.name == "mii":
            return webhook
    return await message.channel.create_webhook(name="mii")


def get_emoji_id(message, emoji_alias):
    get_emoji = discord.utils.get(message.guild.emojis, name=emoji_alias)
    emoji_id = get_emoji.id
    return emoji_id


def get_replaced_char(message, replace_char):
    if replace_char in emojis_main:
        emoji_alias = emojis_main[replace_char]
        emoji_id = get_emoji_id(message, emoji_alias)
        replaced_char = "<:" + emoji_alias + ":" + str(emoji_id) + ">"
        return replaced_char
    elif replace_char in emojis_sub1:
        emoji_alias = emojis_sub1[replace_char]
        emoji_id = get_emoji_id(message, emoji_alias)
        replaced_char = "<:" + emoji_alias + ":" + str(emoji_id) + ">" + "ﾞ "
        return replaced_char
    elif replace_char in emojis_sub2:
        emoji_alias = emojis_sub2[replace_char]
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
        webhook = await get_webhook(ctx)
        replaced_string = []
        for replace_char in replace_string:
            replaced_char = get_replaced_char(ctx, replace_char)
            replaced_string.append(replaced_char)
        content = ">>> " + "".join(replaced_string)
        await ctx.message.delete()
        await webhook.send(
            avatar_url=ctx.author.avatar_url,
            username=ctx.author.display_name,
            content=content
        )


def setup(bot):
    bot.add_cog(Replace_emojiCog(bot))
