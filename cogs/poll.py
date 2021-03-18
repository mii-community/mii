from discord import Embed
from discord.ext.commands import Bot, Cog, Context, command


class Poll(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command()
    async def poll(self, ctx: Context, title: str, *args):
        """!poll <title> <任意の数の要素(21未満、指定しなければ さんせいorはんたい)> で投票を行います。"""
        if len(args) > 21:
            await ctx.send("引数が多すぎます。")
            return
        emoji = 0x0001F1E6
        num = 0
        content = ""
        emojis = []
        if len(args) == 0:
            emojis += [
                "<:___increment:739136647592935494>",
                "<:___decrement:739136716924911748>",
            ]
        else:
            for arg in args:
                reac = chr(emoji + num)
                content += f"{reac}：{arg}\n"
                num += 1
                emojis.append(reac)
        embed = Embed(title=title, description=content, color=0x3AEE67)
        msg = await ctx.send(embed=embed)
        [await msg.add_reaction(e) for e in emojis]


def setup(bot: Bot):
    bot.add_cog(Poll(bot))
