from discord.ext import commands
import discord
import constant

class CloseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def close(self, ctx):
        """自分の作成した部屋/スレッドをアーカイブします。"""
        if ctx.author.bot:
            return
        elif (ctx.channel.category.id != constant.CAT_ROOM
                and ctx.channel.category.id != constant.CAT_THREAD):
            await ctx.send("ここでは実行できません。")
            return
        elif (ctx.channel.topic != "room-author: " + str(ctx.author.id)
                and ctx.channel.topic != "thread-author: " + str(ctx.author.id)
                and (not ctx.author.guild_permissions.administrator)):
            await ctx.send("権限がありません。")
            return

        cat_room = self.bot.get_channel(constant.CAT_ROOM)
        cat_room_archive = self.bot.get_channel(constant.CAT_ROOM_ARCHIVE)
        cat_thread = self.bot.get_channel(constant.CAT_THREAD)
        cat_thread_archive = self.bot.get_channel(constant.CAT_THREAD_ARCHIVE)
        role_member = ctx.guild.get_role(constant.ROLE_MEMBER)
        role_archive = ctx.guild.get_role(constant.ROLE_ARCHIVE)

        if ctx.channel.category == cat_room:
            await ctx.channel.edit(category=cat_room_archive)
        elif ctx.channel.category == cat_thread:
            await ctx.channel.edit(category=cat_thread_archive)
        await ctx.channel.set_permissions(role_member, overwrite=None)
        await ctx.channel.set_permissions(role_archive, read_messages=True, send_messages=False)


def setup(bot):
    bot.add_cog(CloseCog(bot))
