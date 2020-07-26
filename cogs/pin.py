import discord
from discord.ext import commands


class PinCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction_event):
        if reaction_event.member.bot:
            return
        if reaction_event.emoji.name != "\N{PUSHPIN}":
            return
        channel = self.bot.get_channel(reaction_event.channel_id)
        message = await channel.fetch_message(reaction_event.message_id)
        if message.pinned:
            return
        await message.pin()
        await channel.send(f"{reaction_event.member.display_name}がピン留めしました。")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, reaction_event):
        if reaction_event.emoji.name != "\N{PUSHPIN}":
            return
        channel = self.bot.get_channel(reaction_event.channel_id)
        message = await channel.fetch_message(reaction_event.message_id)
        if not message.pinned:
            return
        reaction = discord.utils.get(message.reactions, emoji=reaction_event.emoji.name)
        if reaction:
            return
        await message.unpin()
        embed = discord.Embed(
            title=f"送信者:{message.author.display_name}",
            description=f"メッセージ内容:{message.content}",
            color=0xFF0000,
        )
        await channel.send("リアクションがゼロになったため、ピン留めが解除されました。", embed=embed)


def setup(bot):
    bot.add_cog(PinCog(bot))
