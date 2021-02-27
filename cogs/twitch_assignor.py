import constant
from discord import AllowedMentions, Embed, Member, Streaming
from discord.ext.commands import Bot, Cog


class TwitchAssignor(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.role_streaming = self.bot.get_guild(constant.GUILD_ID).get_role(
            constant.ROLE_STREAMING
        )

    @Cog.listener()
    async def on_member_update(self, before: Member, after: Member):
        for before_activity in before.activities:
            if isinstance(before_activity, Streaming):
                continue
            # 前が配信中でなくて
            for after_activity in after.activities:
                if not isinstance(after_activity, Streaming):
                    continue
                # 後が配信中であれば
                if after_activity.platform != "Twitch":
                    continue
                try:
                    # ロールをつける
                    await after.add_roles(self.role_streaming)
                    return
                except Exception:
                    pass

        for after_activity in after.activities:
            if isinstance(after_activity, Streaming):
                continue
            # 後が配信中でなくて
            for before_activity in before.activities:
                if not isinstance(before_activity, Streaming):
                    continue
                # 前が配信中であれば
                if before_activity.platform != "Twitch":
                    continue
                try:
                    # ロールを外す
                    await after.remove_roles(self.role_streaming)
                    return
                except Exception:
                    pass


def setup(bot: Bot):
    bot.add_cog(TwitchAssignor(bot))
