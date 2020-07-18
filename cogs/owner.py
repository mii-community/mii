from discord.ext import commands
import os
import traceback
import discord


class Owner(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="set")
    @commands.is_owner()
    async def db_set_room_id(self, ctx, member: discord.Member):
        
        user = await self.bot.datebase.fetchrow(
            """
            SELECT *
              FROM mii
             WHERE user_id = $1
               AND guild_id = $2
            """,
            member.id, ctx.guild.id
        )
        if not user:
            user = await self.bot.datebase.fetchrow(
                """
                INSERT INTO mii (user_id, guild_id)
                     VALUES ($1, $2)
                  RETURNING *
                """,
                member.id, ctx.guild.id
            )

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
