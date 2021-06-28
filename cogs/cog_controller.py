from discord.ext.commands import Bot, Cog, Context, command


class CogController(Cog, command_attrs=dict(hidden=True)):
    __slots__ = "bot"

    def __init__(self, bot: Bot):
        self.bot = bot

    async def cog_check(self, ctx: Context) -> bool:
        has_permission = await ctx.bot.is_owner(ctx.author)
        if not has_permission:
            await ctx.reply("You cannot run this command.")
        return has_permission

    @command(name="load")
    async def load_cog(self, ctx: Context, cog: str) -> None:
        self.bot.load_extension("cogs." + cog)
        await ctx.reply(f"Loaded Extension: {cog}")

    @command(name="unload")
    async def unload_cog(self, ctx: Context, cog: str) -> None:
        self.bot.unload_extension("cogs." + cog)
        await ctx.reply(f"Unloaded Extension: {cog}")

    @command(name="reload")
    async def reload_cog(self, ctx: Context, cog: str) -> None:
        self.bot.reload_extension("cogs." + cog)
        await ctx.reply(f"Reloaded Extension: {cog}")


def setup(bot: Bot):
    bot.add_cog(CogController(bot))
