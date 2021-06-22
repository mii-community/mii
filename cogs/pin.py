from discord import AllowedMentions, Message, TextChannel, RawReactionActionEvent, utils
from discord.ext.commands import Bot, Cog

import constant


class Pin(Cog):
    __slots__ = "bot"

    def __init__(self, bot: Bot):
        self.bot = bot

    async def fetch_message_from_reaction(self, reaction: RawReactionActionEvent) -> Message:
        channel: TextChannel = self.bot.get_channel(reaction.channel_id)
        return await channel.fetch_message(reaction.message_id)

    @Cog.listener()
    async def on_raw_reaction_add(self, reaction: RawReactionActionEvent):
        if reaction.emoji.name != constant.EMOJI_PUSHPIN:
            return

        message = await self.fetch_message_from_reaction(reaction)
        if message.pinned:
            return
        await message.pin()
        await message.reply(
            f"{reaction.member.mention} がピン留めしました。",
            allowed_mentions=AllowedMentions.none(),
        )

    @Cog.listener()
    async def on_raw_reaction_remove(self, reaction: RawReactionActionEvent):
        if reaction.emoji.name != constant.EMOJI_PUSHPIN:
            return

        message = await self.fetch_message_from_reaction(reaction)
        if utils.get(message.reactions, emoji=constant.EMOJI_PUSHPIN):
            return
        await message.unpin()
        await message.reply(
            "リアクションがゼロになったため、ピン留めが解除されました。",
            allowed_mentions=AllowedMentions.none()
        )


def setup(bot: Bot):
    bot.add_cog(Pin(bot))
