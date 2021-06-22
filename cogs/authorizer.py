from discord import AllowedMentions, Guild, Member, Message, RawReactionActionEvent, Role, TextChannel
from discord.ext.commands import Bot, Cog

import constant


class Authorizer(Cog):
    __slots__ = "bot"

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_raw_reaction_add(self, reaction: RawReactionActionEvent):
        if (reaction.channel_id != constant.CH_AUTHORIZE) or reaction.member.bot:
            return

        # 新規参加の頻度 > 再起動の頻度 になったら毎回取得するのはやめると良さそう。
        new_member: Member = reaction.member
        target_guild: Guild = new_member.guild
        members_role: Role = target_guild.get_role(constant.ROLE_MEMBER)
        auth_channel: TextChannel = target_guild.get_channel(constant.CH_AUTHORIZE)
        auth_message: Message = await auth_channel.fetch_message(reaction.message_id)
        join_log_channel: TextChannel = target_guild.get_channel(constant.CH_JOIN_LOG)

        if members_role in new_member.roles:
            return
        await new_member.add_roles(members_role)
        await auth_message.remove_reaction(reaction.emoji, new_member)
        await join_log_channel.send(
            f"{new_member.mention} が参加しました。",
            allowed_mentions=AllowedMentions.none(),
        )


def setup(bot: Bot):
    bot.add_cog(Authorizer(bot))
