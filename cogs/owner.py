import constant
from discord import AllowedMentions, Member, TextChannel
from discord.ext.commands import Bot, Cog, Context, command, is_owner


class Owner(Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot: Bot):
        self.bot = bot

    @is_owner()
    @command(name="room")
    async def db_set_room_id(
        self, ctx: Context, member: Member, channel: TextChannel = None
    ):
        if channel is None:
            channel = ctx.channel
        # データベースからデータをもらう
        data_ch = await self.bot.database.fetch_row(
            constant.TABLE_NAME, author_id=member.id, channel_type="room"
        )
        # データがなければ新規作成
        if data_ch is None:
            await self.bot.database.insert(
                constant.TABLE_NAME,
                channel_id=channel.id,
                author_id=member.id,
                channel_type="room",
            )
        # データの上書き
        else:
            await self.bot.database.delete_row(
                constant.TABLE_NAME,
                author_id=member.id,
                channel_type="room",
            )
            await self.bot.database.insert(
                constant.TABLE_NAME,
                {"author_id": member.id},
                channel_id=channel.id,
                channel_type="room",
            )
        await channel.edit(sync_permissions=True)
        await channel.set_permissions(
            member, manage_messages=True, manage_channels=True
        )
        await ctx.send(
            f"{channel.mention}の所有者は{member.mention}にセットされました。",
            allowed_mentions=AllowedMentions.none(),
        )

    @is_owner()
    @command(name="thread")
    async def db_set_thread_id(
        self, ctx: Context, member: Member, channel: TextChannel = None
    ):
        if channel is None:
            channel = ctx.channel
        # データベースからデータをもらう
        data_ch = await self.bot.database.fetch_row(
            constant.TABLE_NAME, channel_id=channel.id
        )
        # データがなければ新規作成
        if data_ch is None:
            await self.bot.database.insert(
                constant.TABLE_NAME,
                channel_id=channel.id,
                author_id=member.id,
                channel_type="thread",
            )
        # データの上書き
        else:
            await self.bot.database.update(
                constant.TABLE_NAME,
                {"author_id": member.id},
                channel_id=channel.id,
                channel_type="thread",
            )
        await ctx.send(
            f"{channel.mention}の所有者は{member.mention}にセットされました。",
            allowed_mentions=AllowedMentions.none(),
        )

    @is_owner()
    @command(name="rcce")
    async def reset_count_custom_emoji(self, ctx: Context):
        await self.bot.database.delete_all(constant.COUNT_EMOJI)
        await ctx.send("カスタム絵文字のカウントをリセットしました。")


def setup(bot: Bot):
    bot.add_cog(Owner(bot))
