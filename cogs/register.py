from discord.ext import commands
import discord
import os

CH_REGISTER = int(os.getenv("CH_REGISTER", "608656664601690142"))
CH_JOIN = int(os.getenv("CH_JOIN", "653923742245978129"))
MEMBER_ROLE_NAME = str(os.getenv("MEMBER_ROLE_NAME", "member"))


class RegisterCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction_event):
        if reaction_event.channel_id == CH_REGISTER:
            channel = self.bot.get_channel(CH_REGISTER)
            message = await channel.fetch_message(reaction_event.message_id)
            guild = discord.utils.find(
                lambda g: g.id == reaction_event.guild_id, self.bot.guilds)
            member = discord.utils.find(
                lambda m: m.id == reaction_event.user_id, guild.members)
            role = discord.utils.get(guild.roles, name=MEMBER_ROLE_NAME)
            if role in member.roles:
                await message.remove_reaction(reaction_event.emoji, member)
                return
            await message.remove_reaction(reaction_event.emoji, member)
            await member.add_roles(role)
            await self.bot.get_channel(CH_JOIN).send(
                f"{reaction_event.member.mention}が参加しました。"
            )


def setup(bot):
    bot.add_cog(RegisterCog(bot))
