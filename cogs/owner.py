from discord.ext import commands
import os
import traceback
import discord


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="set")
    @commands.is_owner()
    async def db_set_room_id(self, ctx, member: discord.Member):
        await self.bot.datebase.execute(
            """
            UPDATE mii
            SET room_id = $1
            WHERE user_id = $2
            AND guild_id = $3
            """,
            ctx.channel.id, member.id, ctx.guild.id
        )
        await ctx.send(f"このチャンネルの所有者は{member.display_name}にセットされました。")
        await ctx.channel.set_permissions(member, manage_messages=True, manage_channels=True)


def setup(bot):
    bot.add_cog(Owner(bot))
