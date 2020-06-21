from discord.ext import commands
import discord
import os

# consts
CH_ROOM_MASTER = int(os.getenv("CH_ROOM_MASTER", "702042912338346114"))
CAT_ROOM = int(os.getenv("CAT_ROOM", "702044270609170443"))
CAT_ROOM_ARCHIVE = int(os.getenv("CAT_THREAD_ARCHIVE", "711058666387800135"))

MEMBER_ROLE_NAME = str(os.getenv("MEMBER_ROLE_NAME", "member"))
ARCHIVE_ROLE_NAME = str(os.getenv("ARCHIVE_ROLE_NAME", "view archive"))


class RoomCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def open(self, ctx):
        """スレッドマスターで使うことであなたの部屋を作成します。"""
        if ctx.author.bot:
            return
        elif ctx.channel.id != CH_ROOM_MASTER:
            await ctx.send("ここでは実行できません。")
            return
        category = self.bot.get_channel(CAT_ROOM_ARCHIVE)
        for channel in category.channels:
            if channel.topic == "room-author: " + str(ctx.author.id):
                await channel.edit(category=self.bot.get_channel(CAT_ROOM))
                role = discord.utils.get(
                    ctx.guild.roles, name=ARCHIVE_ROLE_NAME)
                await channel.set_permissions(role, overwrite=None)
                role = discord.utils.get(
                    ctx.guild.roles, name=MEMBER_ROLE_NAME)
                await channel.set_permissions(role, read_messages=True)
                creator = channel.guild.get_member(ctx.author.id)
                await channel.set_permissions(creator, manage_messages=True)
                await ctx.send(
                    f"{ctx.author.mention} {channel.mention} をアーカイブから戻しました。"
                )
                return
        category = self.bot.get_channel(CAT_ROOM)
        for channel in category.channels:
            if channel.topic == "room-author: " + str(ctx.author.id):
                await ctx.send(
                    f"{ctx.author.mention} {channel.mention} あなたの部屋はもう作られています。"
                )
                return
        named = ctx.author.display_name + "の部屋"
        new_channel = await category.create_text_channel(name=named)
        creator = new_channel.guild.get_member(ctx.author.id)
        await new_channel.edit(topic="room-author: " + str(ctx.author.id))
        await new_channel.set_permissions(creator, manage_messages=True)
        await ctx.send(
            f"{ctx.author.mention} {new_channel.mention} を作成しました。"
        )


def setup(bot):
    bot.add_cog(RoomCog(bot))
