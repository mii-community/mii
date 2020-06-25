from discord.ext import commands
import os
import traceback


async def reload_cog(self, ctx, cog):
    try:
        cog = cog.replace('.py', '')
        self.bot.reload_extension("cogs." + cog)
        await ctx.send(f"{cog}.pyは正常にリロードされました。")
    except:
        await ctx.send("リロードできませんでした。ログを確認してください。")
        traceback.print_exc()


class Load(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, cog):
        try:
            self.bot.load_extension("cogs." + cog)
            await ctx.send(f"{cog}.pyは正常にリロードされました。")
        except:
            await ctx.send("リロードできませんでした。ログを確認してください。")
            traceback.print_exc()

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, cog):
        if cog == "all":
            for cog in [cogs for cogs in os.listdir("./cogs") if cogs.endswith(".py")]:
                await reload_cog(self, ctx, cog)
            await ctx.send("全て終わりました。")
            return
        await reload_cog(self, ctx, cog)


def setup(bot):
    bot.add_cog(Load(bot))
