from asyncio import Lock, Queue

from discord import Message, TextChannel
from discord.ext.commands import Bot, Cog

import constant


class MessageCountManager(Cog):
    __slots__ = "bot", "lock", "message_queue"

    def __init__(self, bot: Bot):
        self.bot = bot
        self.lock = Lock()
        self.message_queue = Queue(maxsize=25)

    async def update_message_queue(self, message: Message) -> None:
        async with self.lock:
            if self.message_queue.full():
                try:
                    delete_message: Message = await self.message_queue.get()
                    await delete_message.delete()
                except Exception:
                    pass
            await self.message_queue.put(message)

    @Cog.listener()
    async def on_ready(self):
        monitoring_channel: TextChannel = self.bot.get_channel(constant.CH_LIMITED_MESSAGE_COUNT)
        async for message in monitoring_channel.history(oldest_first=True):
            await self.update_message_queue(message)

    @Cog.listener()
    async def on_message(self, message: Message):
        if message.channel.id == constant.CH_LIMITED_MESSAGE_COUNT:
            await self.update_message_queue(message)


def setup(bot: Bot):
    bot.add_cog(MessageCountManager(bot))
