import constant
from discord import AllowedMentions, Embed, utils
from discord.ext.commands import Bot, Cog


class Pin(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_raw_reaction_add(self, reaction):
        if reaction.emoji.name != constant.PIN_EMOJI:
            return
        channel = self.bot.get_channel(reaction.channel_id)
        message = await channel.fetch_message(reaction.message_id)
        if message.pinned:
            return
        await message.pin()
        await channel.send(
            f"{reaction.member.mention}がピン留めしました。",
            allowed_mentions=AllowedMentions.none(),
        )

    @Cog.listener()
    async def on_raw_reaction_remove(self, reaction):
        if reaction.emoji.name != constant.PIN_EMOJI:
            return
        channel = self.bot.get_channel(reaction.channel_id)
        message = await channel.fetch_message(reaction.message_id)
        if not message.pinned:
            return
        reaction = utils.get(message.reactions, emoji=constant.PIN_EMOJI)
        if reaction:
            return
        await message.unpin()
        embed = Embed(
            title=f"送信者:{message.author.display_name}",
            description=f"メッセージ内容:{message.content}",
            color=0xFF0000,
        )
        await channel.send("リアクションがゼロになったため、ピン留めが解除されました。", embed=embed)


def setup(bot: Bot):
    bot.add_cog(Pin(bot))
