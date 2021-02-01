import constant
from discord.ext.commands import Bot, Cog, Context, command


class Room(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command()
    async def open(self, ctx: Context):
        """ルームマスターで使うことであなたの部屋を作成します。"""
        author = ctx.author
        if author.bot:
            return
        channel = ctx.channel
        if channel.id != constant.CH_ROOM_MASTER:
            await ctx.send("ここでは実行できません。")
            return
        data_room = await self.bot.database.fetch_row(
            constant.TABLE_NAME, author_id=author.id, channel_type="room"
        )
        guild = ctx.guild
        creator = guild.get_member(author.id)
        cat_room = self.bot.get_channel(constant.CAT_ROOM)
        # ルームを持っていない場合
        if data_room is None:
            name = f"{author.display_name}の部屋"
            new_room = await cat_room.create_text_channel(name=name)
            await new_room.set_permissions(
                creator, manage_messages=True, manage_channels=True
            )
            await ctx.send(f"{author.mention} {new_room.mention} を作成しました。")
            await self.bot.database.insert(
                constant.TABLE_NAME,
                channel_id=new_room.id,
                author_id=author.id,
                channel_type="room",
            )
            return
        # ルームカテゴリーにある場合
        ch_room = self.bot.get_channel(data_room["channel_id"])
        if ch_room.category == cat_room:
            text = "あなたの部屋はもう作られています。"
        # アーカイブカテゴリーにある場合
        elif ch_room.category.id == constant.CAT_ROOM_ARCHIVE:
            text = "をアーカイブから戻しました。"
            await ch_room.edit(category=cat_room)
            await ch_room.edit(sync_permissions=True)
            await ch_room.set_permissions(
                creator, manage_messages=True, manage_channels=True
            )
        await ctx.send(f"{author.mention} {ch_room.mention} {text}")


def setup(bot: Bot):
    bot.add_cog(Room(bot))
