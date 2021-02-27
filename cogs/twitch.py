import constant
from discord import AllowedMentions, Embed, Member, Streaming
from discord.ext.commands import Bot, Cog


class Twitch(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    def to_embed(self, stream, streamer):
        embed = Embed(title=stream.name, url=stream.url)
        embed.add_field(name="Category:", value=stream.game, inline=True)
        embed.set_author(name=stream.twitch_name, url=stream.url)
        embed.set_thumbnail(url=streamer.avatar_url)
        return embed

    @Cog.listener()
    async def on_member_update(self, before: Member, after: Member):
        if after.activities is None:
            after.activities = ("dummy",)
        if before.activities is None:
            before.activities = ("dummy",)
        guild = self.bot.get_guild(constant.GUILD_ID)
        role_streaming = guild.get_role(constant.ROLE_STREAMING)
        ch_twitch = self.bot.get_channel(constant.CH_TWITCH)
        # 後が配信中
        if any(
            [
                isinstance(after_activity, Streaming)
                for after_activity in after.activities
            ]
        ):
            if any(
                [
                    isinstance(before_activity, Streaming)
                    for before_activity in before.activities
                ]
            ):
                return
            # 前が配信中でない
            for after_activity in after.activities:
                if not isinstance(after_activity, Streaming):
                    continue

                await ch_twitch.send(
                    f"{after.mention} が配信を始めました！",
                    embed=self.to_embed(after_activity, after),
                    allowed_mentions=AllowedMentions.none(),
                )
                await after.add_roles(role_streaming)
                return

        # 後が配信中じゃない
        else:
            if not any(
                [
                    isinstance(before_activity, Streaming)
                    for before_activity in before.activities
                ]
            ):
                return
            # 前が配信中
            await after.remove_roles(role_streaming)
            return


def setup(bot: Bot):
    bot.add_cog(Twitch(bot))
