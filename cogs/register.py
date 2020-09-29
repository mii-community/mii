from discord.ext import commands
import discord
import constant


class RegisterCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction_register):
        if reaction_register.channel_id != constant.CH_REGISTER:
            return

        member = reaction_register.member  # shorten
        guild = self.bot.get_guild(reaction_register.guild_id)  # for get_role()
        role = guild.get_role(constant.ROLE_MEMBER)  # for add_roles()
        channel = self.bot.get_channel(constant.CH_REGISTER)  # for fetch_message()
        message = await channel.fetch_message(
            reaction_register.message_id
        )  # for remove_reaction()

        if not role in member.roles:
            await member.add_roles(role)
            await self.bot.get_channel(constant.CH_JOIN).send(
                f"{reaction_register.member.mention}が参加しました。"
            )
        await message.remove_reaction(reaction_register.emoji, member)


def setup(bot):
    bot.add_cog(RegisterCog(bot))
