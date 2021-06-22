from typing import List

from discord import Embed
from discord.ext.commands import Bot, Cog, Context, command


class Poll(Cog):
    __slots__ = "bot"

    def __init__(self, bot: Bot):
        self.bot = bot

    @command()
    async def poll(self, ctx: Context, title: str, *args: str) -> None:
        """!poll <title> <任意の数の要素(20以下、指定しなければ +1 / -1 )> で投票を行います。"""
        # メッセージへのリアクションは20種類までしかできない
        if len(args) > 20:
            await ctx.reply("Too Many Arguments. Maximum number of reactions reached (20)")
            return

        # 絵文字 A の定数。インクリメントすると B, C, D ... となる
        const_emoji_large_a = 0x1f1e6
        elements: List[str] = []
        emojis: List[str] = []

        if len(args) == 0:
            emojis.extend(["<:___increment:739136647592935494>", "<:___decrement:739136716924911748>"])
        else:
            for i, element in enumerate(args):
                emoji = chr(const_emoji_large_a + i)
                elements.append(f"{emoji}：{element}")
                emojis.append(emoji)

        poll_board = Embed(title=title, description="\n".join(elements), color=0xffff00)
        message = await ctx.send(embed=poll_board)
        [await message.add_reaction(emoji) for emoji in emojis]


def setup(bot: Bot):
    bot.add_cog(Poll(bot))
