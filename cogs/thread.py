from discord.ext import commands
import discord
import os

# consts
CH_THREAD_MASTER = int(os.getenv("CH_THREAD_MASTER", "702030388033224714"))
CAT_THREAD = int(os.getenv("CAT_THREAD", "662856289151615025"))
CAT_THREAD_ARCHIVE = int(os.getenv("CAT_THREAD_ARCHIVE", "702074011772911656"))
ROLE_MEMBER = int(os.getenv("ROLE_MEMBER", "652885488197435422"))
ROLE_ARCHIVE = int(os.getenv("ROLE_ARCHIVE", "702420267309203466"))


class ThreadCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if (message.author.bot
            or message.channel.category.id != CAT_THREAD):
            return
        elif message.channel.id == CH_THREAD_MASTER:
            named = message.content
            matched = discord.utils.get(message.guild.channels, name=named)
            if not matched:
                new_channel = await self.bot.get_channel(CAT_THREAD).create_text_channel(name=named)
                await new_channel.edit(topic="thread-author: " + str(message.author.id))
                await message.channel.send(
                    f"{message.author.mention} {new_channel.mention} を作成しました。"
                )
            elif matched.category.id == CAT_THREAD:
                await message.channel.send(
                    f"{message.author.mention} {matched.mention} はもう作られています。"
                )
            elif matched.category.id == CAT_THREAD_ARCHIVE:
                await matched.edit(category=self.bot.get_channel(CAT_THREAD))
                role = message.guild.get_role(ROLE_ARCHIVE)
                await matched.set_permissions(role, overwrite=None)
                role = message.guild.get_role(ROLE_MEMBER)
                await matched.set_permissions(role, read_messages=True)
                await matched.edit(topic="thread-author: " + str(message.author.id))
                await message.channel.send(
                    f"{message.author.mention} {matched.mention} をアーカイブから戻しました。スレッドの作者は上書きされました。"
                )
        else:
            position = self.bot.get_channel(CH_THREAD_MASTER).position + 1
            await message.channel.edit(position=position)

def setup(bot):
    bot.add_cog(ThreadCog(bot))
