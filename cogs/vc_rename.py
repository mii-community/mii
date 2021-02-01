import constant
from discord import Embed
from discord.ext.commands import Bot, Cog, Context, command


class VCRename(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command()
    async def vc(self, ctx: Context, name: str):
        """VC参加中に使うことでVCのリネームができます。"""
        state = ctx.author.voice
        if not state:
            await ctx.send(f"{ctx.author.mention} VCに参加していないため実行できません。")
            return
        if state.channel.id == constant.CH_AFK:
            await ctx.send(f"{ctx.author.mention} AFKチャンネルに接続中は実行できません。")
            return
        if ctx.channel.id != constant.VOICE_CHANNELS[str(state.channel.id)]["vc_text"]:
            await ctx.send(f"{ctx.author.mention} VCに対応したチャンネルで実行してください。")
            return
        if not ctx.channel.id in [
            value.get("vc_text") for value in constant.VOICE_CHANNELS.values()
        ]:
            await ctx.send(f"{ctx.author.mention} ここでは実行できないコマンドです。")
            return

        await state.channel.edit(name=name)
        await ctx.channel.edit(name=f"{name}-no-mic")
        embed = Embed(
            description=f"{ctx.author.mention} がチャンネル名を {name} に変更しました。",
            colour=0x000000,
        )
        embed.set_footer(text="このメッセージは30秒後に自動で削除されます。")
        await ctx.send(embed=embed, delete_after=30)

    @Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        vc = after.channel or before.channel
        if not str(vc.id) in constant.VOICE_CHANNELS.keys():
            return
        name = constant.VOICE_CHANNELS[str(vc.id)]["name"]
        if len(vc.members) != 0 or vc.name == name:
            return
        await vc.edit(name=name)
        vc_text = self.bot.get_channel(constant.VOICE_CHANNELS[str(vc.id)]["vc_text"])
        await vc_text.edit(name=f"{name}-no-mic")
        embed = Embed(description="接続人数が0になったのでチャンネル名をリセットしました。", colour=0x000000)
        embed.set_footer(text="このメッセージは30秒後に自動で削除されます。")
        await vc_text.send(embed=embed, delete_after=30)


def setup(bot: Bot):
    bot.add_cog(VCRename(bot))
