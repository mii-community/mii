import os
import traceback
import pathlib

from discord.ext import commands


class Load(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, cog):
        try:
            self.bot.load_extension("cogs." + cog)
            await ctx.send(f"{cog}.pyは正常にロードされました。")
        except:
            await ctx.send(f"{cog}.pyはロードできませんでした。ログを確認してください。")
            traceback.print_exc()

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, cog):
        try:
            self.bot.unload_extension("cogs." + cog)
            await ctx.send(f"{cog}.pyは正常にアンロードされました。")
        except:
            await ctx.send(f"{cog}.pyはアンロードできませんでした。ログを確認してください。")
            traceback.print_exc()

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, cog):
        async def reload_cog(cog):
            try:
                self.bot.reload_extension("cogs." + cog)
                await ctx.send(f"{cog}.pyは正常にリロードされました。")
            except:
                await ctx.send(f"{cog}.pyはリロードできませんでした。ログを確認してください。")
                traceback.print_exc()
            return

        if cog == "all":
            for cog in pathlib.Path("cogs/").glob("*.py"):
                await reload_cog(cog.stem)
            await ctx.send("全て終わりました。")
            return
        await reload_cog(cog)


def setup(bot):
    bot.add_cog(Load(bot))
