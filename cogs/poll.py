from discord.ext import commands
import discord


class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def poll(self, ctx, title, *args):
        """!poll <title> <任意の数の要素(22未満、指定しなければ さんせいorはんたい)> で投票を行います。"""
        if len(args) > 21:
            return
        emoji = 0x0001f1e6
        num = 0
        content = ""
        emojis = []
        if len(args) == 0:
            emojis += [
                "<:__sansei:703788213919023104>", "<:__hantai:703788248362647594>"]
        else:
            for arg in args:
                reac = chr(emoji + num)
                content += f"{reac}：{arg}\n"
                num += 1
                emojis.append(reac)
        embed = discord.Embed(
            title=title,
            description=content,
            color=0x3aee67
        )
        msg = await ctx.send(embed=embed)
        [await msg.add_reaction(e) for e in emojis]


def setup(bot):
    bot.add_cog(Poll(bot))
