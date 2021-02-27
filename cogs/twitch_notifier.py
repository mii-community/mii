import constant
from discord import AllowedMentions, Embed, Member, Streaming
from discord.ext.commands import Bot, Cog


class TwitchNotifier(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_update(self, before: Member, after: Member):
        for before in before.activities:
            if isinstance(before, Streaming):
                return
        for after_activity in after.activities:
            if not isinstance(after_activity, Streaming):
                continue
            stream = after_activity
            if stream.platform != "Twitch":
                return
            embed = Embed(title=stream.name, url=stream.url)
            embed.add_field(name="Game:", value=stream.game, inline=True)
            embed.set_author(
                name=stream.twitch_name, url=stream.url, icon_url=after.avatar_url
            )
            embed.set_thumbnail(url=after.avatar_url)
            msg = f"{after.mention} が {stream.platform} で配信を始めました！"
            await self.bot.get_channel(constant.CH_TWITCH).send(
                msg, embed=embed, allowed_mentions=AllowedMentions.none()
            )


def setup(bot: Bot):
    bot.add_cog(TwitchNotifier(bot))
