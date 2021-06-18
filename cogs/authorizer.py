import constant
from discord import AllowedMentions
from discord.ext.commands import Bot, Cog


class Register(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_raw_reaction_add(self, reaction):
        if reaction.channel_id != constant.CH_REGISTER:
            return

        user = reaction.member
        guild = self.bot.get_guild(reaction.guild_id)
        role_member = guild.get_role(constant.ROLE_MEMBER)
        ch_register = self.bot.get_channel(constant.CH_REGISTER)
        message = await ch_register.fetch_message(reaction.message_id)
        if role_member in user.roles:
            return
        await user.add_roles(role_member)
        ch_notify = self.bot.get_channel(constant.CH_JOIN)
        await ch_notify.send(
            f"{user.mention}が参加しました。",
            allowed_mentions=AllowedMentions.none(),
        )
        await message.remove_reaction(reaction.emoji, user)


def setup(bot: Bot):
    bot.add_cog(Register(bot))
