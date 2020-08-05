from discord.ext import commands
import os
import traceback
import glob


class Load(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if not await ctx.bot.is_owner(ctx.author):
            await ctx.send("権限がありません。")
            return False
        return True

    @commands.command(name="load")
    async def load_cog(self, ctx, cog):
        try:
            self.bot.load_extension("cogs." + cog)
            await ctx.send(f"{cog}.pyは正常にロードされました。")
        except:
            await ctx.send(f"{cog}.pyはロードできませんでした。ログを確認してください。")
            traceback.print_exc()

    @commands.command(name="unload")
    async def unload_cog(self, ctx, cog):
        try:
            self.bot.unload_extension("cogs." + cog)
            await ctx.send(f"{cog}.pyは正常にアンロードされました。")
        except:
            await ctx.send(f"{cog}.pyはアンロードできませんでした。ログを確認してください。")
            traceback.print_exc()

    @commands.command(name="reload")
    async def reload_cog(self, ctx, cog):
        try:
            self.bot.reload_extension("cogs." + cog)
            await ctx.send(f"{cog}は正常にリロードされました。")
        except:
            await ctx.send(f"{cog}.pyはリロードできませんでした。ログを確認してください。")

    @commands.command(name="reloadall")
    async def reload_all_cogs(self, ctx):
        for cog in [cog.replace("/", ".").replace(".py", "") for cog in glob.glob("cogs/*.py")]:
            try:
                self.bot.reload_extension(cog)
                await ctx.send(f"{cog}は正常に読み込まれました。")
            except:
                traceback.print_exc()
        await ctx.send("すべて終わりました。")


def setup(bot):
    bot.add_cog(Load(bot))
