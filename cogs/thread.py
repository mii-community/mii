from discord.ext import commands
import discord
import os
import launcher


class ThreadCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if (message.author.bot
                or message.channel.category.id != launcher.CAT_THREAD):
            return
        elif message.channel.id == launcher.CH_THREAD_MASTER:
            named = message.content
            matched = discord.utils.get(message.guild.channels, name=named)
            if not matched:
                new_channel = await self.bot.get_channel(launcher.CAT_THREAD).create_text_channel(name=named)
                await new_channel.edit(topic="thread-author: " + str(message.author.id))
                await message.channel.send(
                    f"{message.author.mention} {new_channel.mention} を作成しました。"
                )
            elif matched.category.id == launcher.CAT_THREAD:
                await message.channel.send(
                    f"{message.author.mention} {matched.mention} はもう作られています。"
                )
            elif matched.category.id == launcher.CAT_THREAD_ARCHIVE:
                await matched.edit(category=self.bot.get_channel(launcher.CAT_THREAD))
                role = message.guild.get_role(launcher.ROLE_ARCHIVE)
                await matched.set_permissions(role, overwrite=None)
                role = message.guild.get_role(launcher.ROLE_MEMBER)
                await matched.set_permissions(role, read_messages=True)
                await matched.edit(topic="thread-author: " + str(message.author.id))
                await message.channel.send(
                    f"{message.author.mention} {matched.mention} をアーカイブから戻しました。スレッドの作者は上書きされました。"
                )
        else:
            position = self.bot.get_channel(launcher.CH_THREAD_MASTER).position + 1
            await message.channel.edit(position=position)


def setup(bot):
    bot.add_cog(ThreadCog(bot))
