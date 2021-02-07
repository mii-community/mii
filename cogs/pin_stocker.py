import constant
from discord import (
    Embed,
    Message,
    RawBulkMessageDeleteEvent,
    RawMessageDeleteEvent,
    RawMessageUpdateEvent,
    TextChannel,
)
from discord.ext.commands import Bot, Cog, Context, command, has_permissions


class PinStocker(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        cat_room = 702044270609170443
        cat_logger = 763821640219230208
        cat_background = 655268967144882186
        self.ignore_categories = [cat_room, cat_logger, cat_background]

    async def send_pin_stock(self, pin: Message):
        embed = Embed(
            description=pin.content,
            url=pin.jump_url,
            timestamp=pin.created_at,
        )
        embed.set_author(name=pin.author, icon_url=pin.author.avatar_url)
        embed.set_footer(text=pin.channel.name)
        fixed_file = None
        if pin.attachments:
            if pin.attachments[0].is_spoiler():
                fixed_file = await pin.attachments[0].to_file(spoiler=True)
            elif pin.attachments[0].filename.endswith((".mov", ".mp4")):
                fixed_file = await pin.attachments[0].to_file()
            else:
                embed.set_image(url=pin.attachments[0].url)
        msg = pin.jump_url
        if pin.embeds:
            msg += "\nEmbed は messageUrl から確認してください。"
        ch_pin_stock = self.bot.get_channel(constant.CH_PIN_STOCK)
        return await ch_pin_stock.send(msg, embed=embed, file=fixed_file)

    async def delete_already_pinned_message(self, id, stocked_pins):
        for stocked_pin in stocked_pins:
            if str(id) in stocked_pin.content:
                await stocked_pin.delete()

    @command(aliases=["rep"])
    @has_permissions(administrator=True)
    async def refresh_pin_stocks(self, ctx: Context):
        for channel in ctx.guild.channels:
            if (
                channel.category is None
                or channel.category.id in self.ignore_categories
            ):
                continue
            if type(channel) != TextChannel:
                continue
            if channel.is_nsfw():
                continue
            for pin in await channel.pins():
                await self.send_pin_stock(pin)

    @Cog.listener()
    async def on_raw_message_edit(self, payload: RawMessageUpdateEvent):
        channel = self.bot.get_channel(payload.channel_id)
        if channel.category is None or channel.category.id in self.ignore_categories:
            return
        if channel.is_nsfw():
            return
        ch_pin_stock = self.bot.get_channel(constant.CH_PIN_STOCK)
        stocked_pins = await ch_pin_stock.history(limit=None).flatten()
        message_id = payload.message_id
        await self.delete_already_pinned_message(message_id, stocked_pins)
        message = await channel.fetch_message(message_id)
        if not message.pinned:
            return
        if message.pinned:
            await self.send_pin_stock(message)

    @Cog.listener()
    async def on_raw_message_delete(self, payload: RawMessageDeleteEvent):
        ch_pin_stock = self.bot.get_channel(constant.CH_PIN_STOCK)
        stocked_pins = await ch_pin_stock.history(limit=None).flatten()
        await self.delete_already_pinned_message(payload.message_id, stocked_pins)

    @Cog.listener()
    async def on_raw_bulk_message_delete(self, payload: RawBulkMessageDeleteEvent):
        ch_pin_stock = self.bot.get_channel(constant.CH_PIN_STOCK)
        stocked_pins = await ch_pin_stock.history(limit=None).flatten()
        for message_id in payload.message_ids:
            await self.delete_already_pinned_message(message_id, stocked_pins)

    @Cog.listener()
    async def on_guild_channel_delete(self, channel):
        ch_pin_stock = self.bot.get_channel(constant.CH_PIN_STOCK)
        stocked_pins = await ch_pin_stock.history(limit=None).flatten()
        await self.delete_already_pinned_message(channel.id, stocked_pins)


def setup(bot: Bot):
    bot.add_cog(PinStocker(bot))
