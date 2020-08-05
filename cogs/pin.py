from discord.ext import commands
import discord
import constant

class PinCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction_pin):
        if reaction_pin.emoji.name != constant.EMOJI_PIN:
            return
        channel = self.bot.get_channel(reaction_pin.channel_id)
        message = await channel.fetch_message(reaction_pin.message_id)
        if message.pinned:
            return
        await message.pin()
        await channel.send(f"{reaction_pin.member.display_name}がピン留めしました。")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, reaction_pin):
        if reaction_pin.emoji.name != constant.EMOJI_PIN:
            return
        channel = self.bot.get_channel(reaction_pin.channel_id)
        message = await channel.fetch_message(reaction_pin.message_id)
        if not message.pinned:
            return
        reaction = discord.utils.get(message.reactions, emoji=constant.EMOJI_PIN)
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