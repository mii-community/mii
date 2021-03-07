from discord import AllowedMentions
from discord.ext.commands import Bot, Cog, Context, command
from googletrans import Translator


class QuickTranslator(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command()
    async def tr(self, ctx: Context, dest: str, *, text: str):
        """!tr <翻訳先の言語コード> <翻訳するテキスト>"""
        translator = Translator()
        translated = translator.translate(text, dest=dest)
        reply_message = translated.text
        if translated.pronunciation is not None:
            reply_message += f"\n🗣 {translated.pronunciation}"
        await ctx.reply(reply_message, allowed_mentions=AllowedMentions.none())


def setup(bot: Bot):
    bot.add_cog(QuickTranslator(bot))
