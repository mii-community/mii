import constant
from discord import Embed
from discord.ext.commands import Bot, Cog, command


class VCNotifier(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel == after.channel:
            return
        vc = after.channel or before.channel
        if not str(vc.id) in constant.VOICE_CHANNELS.keys():
            return
        if after.channel:
            embed = Embed(description=f"{member.mention}が入室しました。", colour=0x000000)
        elif before.channel:
            embed = Embed(description=f"{member.mention}が退室しました。", colour=0x000000)
        else:
            return
        embed.set_footer(text="このメッセージは30秒後に自動で削除されます。")
        vc_text = self.bot.get_channel(constant.VOICE_CHANNELS[str(vc.id)]["vc_text"])
        await vc_text.send(embed=embed, delete_after=30)


def setup(bot: Bot):
    bot.add_cog(VCNotifier(bot))
