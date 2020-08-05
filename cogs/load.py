from discord.ext import commands
import os
import traceback


class Load(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if not await ctx.bot.is_owner(ctx.author):
            ctx.send("権限がありません。")
            return False
        return True

    @commands.command()
    async def load(self, ctx, cog):
        try:
            self.bot.load_extension("cogs." + cog)
            await ctx.send(f"{cog}.pyは正常にロードされました。")
        except:
            await ctx.send(f"{cog}.pyはロードできませんでした。ログを確認してください。")
            traceback.print_exc()

    @commands.command()
    async def unload(self, ctx, cog):
        try:
            self.bot.unload_extension("cogs." + cog)
            await ctx.send(f"{cog}.pyは正常にアンロードされました。")
        except:
            await ctx.send(f"{cog}.pyはアンロードできませんでした。ログを確認してください。")
            traceback.print_exc()

    async def reload_cog(self, ctx, cog):
        try:
            cog = cog.replace('.py', '')
            self.bot.reload_extension("cogs." + cog)
            await ctx.send(f"{cog}.pyは正常にリロードされました。")
        except:
            await ctx.send(f"{cog}.pyはリロードできませんでした。ログを確認してください。")
            traceback.print_exc()

    @commands.command()
    async def reload(self, ctx, cog):
        if cog == "all":
            for cog in [cogs for cogs in os.listdir("./cogs") if cogs.endswith(".py")]:
                await self.reload_cog(ctx, cog)
            await ctx.send("全て終わりました。")
            return
        await self.reload_cog(ctx, cog)


def setup(bot):
    bot.add_cog(Load(bot))
