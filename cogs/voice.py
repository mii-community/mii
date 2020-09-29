import os

import discord
from discord.ext import commands

import constant


class VoiceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def vc(self, ctx, named):
        """VC参加中に使うことでVCのリネームができます。"""
        if ctx.channel.id != constant.CH_VOICE_TEXT:
            await ctx.send(f"{ctx.author.mention} ここでは実行できません。")
            return
        state = ctx.author.voice
        if not state:
            await ctx.send(f"{ctx.author.mention} VCに参加していないため実行できません。")
            return
        if state.channel.id != constant.CH_VOICE:
            await ctx.send(f"{ctx.author.mention} AFKチャンネルに接続中は実行できません。")
            return
        channel = self.bot.get_channel(constant.CH_VOICE)
        await channel.edit(name=named)
        await ctx.channel.edit(name=f"{named}-text")
        await ctx.send(f"{ctx.author.mention} チャンネル名を {named} に上書きしました。")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel == after.channel:
            return

        voice_channel = after.channel or before.channel
        if voice_channel.id != constant.CH_VOICE:
            return

        vc_members = len(voice_channel.members)
        vc_text = self.bot.get_channel(constant.CH_VOICE_TEXT)

        if after.channel and vc_members >= 2:
            embed = discord.Embed(
                description=f"{member.display_name}が入室しました。", colour=0x000000
            )
        elif before.channel and vc_members >= 1:
            embed = discord.Embed(
                description=f"{member.display_name}が退室しました。", colour=0x000000
            )
        elif vc_members == 0 and voice_channel.name != "vc":
            await voice_channel.edit(name="vc")
            await vc_text.edit(name="vc-text")
            embed = discord.Embed(
                description="接続人数が0になったのでチャンネル名をリセットしました。", colour=0x000000
            )

        await vc_text.send(embed=embed, delete_after=60)


def setup(bot):
    bot.add_cog(VoiceCog(bot))
