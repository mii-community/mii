import constant
from discord import Message, utils
from discord.ext.commands import Bot, Cog


class Thread(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message):
        author = message.author
        channel = message.channel
        if author.bot:
            return

        # 新着順ソート
        if (
            channel.category.id == constant.CAT_THREAD
            and channel.id != constant.CH_THREAD_MASTER
        ):
            position = self.bot.get_channel(constant.CH_THREAD_MASTER).position + 1
            if channel.position <= position:
                return
            await channel.edit(position=position)

        if channel.id == constant.CH_THREAD_MASTER:
            name = message.content
        elif message.content.startswith("##"):
            name = message.content[2:]
        else:
            return
        guild = message.guild
        ch_thread = utils.get(guild.channels, name=name)
        cat_thread = self.bot.get_channel(constant.CAT_THREAD)
        ch_main = self.bot.get_channel(constant.CH_MAIN)
        # 同名CHがない場合
        if ch_thread is None:
            new_thread = await cat_thread.create_text_channel(name=name)
            await channel.send(f"{author.mention} {new_thread.mention} を作成しました。")
            if not message.channel == ch_main:
                await ch_main.send(f"{new_thread.mention} が作成されました。")
            await self.bot.database.insert(
                constant.TABLE_NAME,
                channel_id=new_thread.id,
                author_id=author.id,
                channel_type="thread",
            )
            return
        # 同名CHがスレッドカテゴリーにある場合
        if ch_thread.category == cat_thread:
            text = "はもう作られています。"
        # 同名CHがアーカイブカテゴリーにある場合
        elif ch_thread.category.id == constant.CAT_THREAD_ARCHIVE:
            text = "をアーカイブから戻しました。"
            await ch_thread.edit(category=cat_thread)
            await ch_thread.edit(sync_permissions=True)
            await ch_main.send(f"{ch_thread.mention} が再開されました。")
            await self.bot.database.update(
                constant.TABLE_NAME,
                {"author_id": author.id},
                channel_id=ch_thread.id,
                channel_type="thread",
            )
        await channel.send(f"{author.mention} {ch_thread.mention} {text}")


def setup(bot: Bot):
    bot.add_cog(Thread(bot))
