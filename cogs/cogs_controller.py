from discord.ext.commands import Bot, Cog, Context, command


class CogsController(Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def cog_check(self, ctx: Context):
        if await ctx.bot.is_owner(ctx.author):
            return True
        await ctx.send("You cannot run this command.")
        return False

    @command(name="load")
    async def load_cog(self, ctx: Context, cog: str):
        self.bot.load_extension("cogs." + cog)
        await ctx.send(f"Loaded Extension: {cog}.py")

    @command(name="unload")
    async def unload_cog(self, ctx: Context, cog: str):
        self.bot.unload_extension("cogs." + cog)
        await ctx.send(f"Unloaded Extension: {cog}.py")

    @command(name="reload")
    async def reload_cog(self, ctx: Context, cog: str):
        self.bot.reload_extension("cogs." + cog)
        await ctx.send(f"Reloaded Extension: {cog}.py")


def setup(bot: Bot):
    bot.add_cog(CogsController(bot))
