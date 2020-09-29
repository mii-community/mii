import os

import discord
from discord.ext import commands

import constant


class RegisterCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction_event):
        if reaction_event.channel_id == constant.CH_REGISTER:
            channel = self.bot.get_channel(constant.CH_REGISTER)
            guild = self.bot.get_guild(reaction_event.guild_id)
            message = await channel.fetch_message(reaction_event.message_id)
            member = reaction_event.member
            role = guild.get_role(constant.ROLE_MEMBER)
            if role in member.roles:
                await message.remove_reaction(reaction_event.emoji, member)
                return
            await message.remove_reaction(reaction_event.emoji, member)
            await member.add_roles(role)
            await self.bot.get_channel(constant.CH_JOIN).send(
                f"{reaction_event.member.mention}が参加しました。"
            )


def setup(bot):
    bot.add_cog(RegisterCog(bot))
