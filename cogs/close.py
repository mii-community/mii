from discord.ext import commands
import constant


class CloseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def close(self, ctx):
        """自分の作成した部屋/スレッドをアーカイブします。"""
        if ctx.author.bot:
            return
        elif not (ctx.channel.category.id == constant.CAT_ROOM
                  or ctx.channel.category.id == constant.CAT_THREAD):
            await ctx.send("ここでは実行できません。")
            return
        elif not (ctx.channel.topic == f"room-author: {ctx.author.id}"
                  or ctx.channel.topic == f"thread-author: + {ctx.author.id}"
                  or ctx.author.guild_permissions.administrator):
            await ctx.send("権限がありません。")
            return

        if ctx.channel.category.id == constant.CAT_ROOM:
            goto_cat = self.bot.get_channel(constant.CAT_ROOM_ARCHIVE)
        elif ctx.channel.category.id == constant.CAT_THREAD:
            goto_cat = self.bot.get_channel(constant.CAT_THREAD_ARCHIVE)
        await ctx.channel.edit(category=goto_cat)
        role_member = ctx.guild.get_role(constant.ROLE_MEMBER)
        role_archive = ctx.guild.get_role(constant.ROLE_ARCHIVE)
        await ctx.channel.set_permissions(role_member, overwrite=None)
        await ctx.channel.set_permissions(role_archive, read_messages=True, send_messages=False)


def setup(bot):
    bot.add_cog(CloseCog(bot))
