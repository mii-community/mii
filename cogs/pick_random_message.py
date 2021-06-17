import random
from typing import List

from discord import AllowedMentions, Message, TextChannel, utils, Webhook
from discord.ext.commands import Bot, Cog
from discord.ext.tasks import loop

import constant


class PickRandomMessage(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.random_pickup.start()

    @loop(hours=1)
    async def random_pickup(self):
        # 周辺5件を抽出
        i = random.randint(3, len(self.pickup_source) - 2)
        messages = self.pickup_source[i - 3:i + 2]
        # 中央のメッセージリンクを送る
        await self.webhook.send(content=messages[2].jump_url)
        for message in reversed(messages):
            fixed_files = []
            additional_messages = "".join(f"\n[Sticker:{s.name}]" for s in message.stickers or [])
            for a in message.attachments or []:
                if a.is_spoiler():
                    fixed_files.append(await a.to_file(spoiler=True))
                    continue
                additional_messages += "\n" + (
                    f"[Audio: {a.filename}]" if a.url.endswith((".wav", ".mp3", ".ogg")) else a.url)

            await self.webhook.send(
                content=(message.content + additional_messages) or (
                    "" if message.attachments else "empty message"),
                username=f"{message.author.display_name}  {message.created_at.strftime('%Y年%m月%d日 %H時%M分')}",
                avatar_url=message.author.avatar_url,
                files=fixed_files,
                embeds=message.embeds,
                allowed_mentions=AllowedMentions.none()
            )

    @random_pickup.before_loop
    async def before_random_pickup(self):
        await self.bot.wait_until_ready()
        ch_pickup_source: TextChannel = self.bot.get_channel(constant.CH_PICKUP_SOURCE)
        self.pickup_source: List[Message] = await ch_pickup_source.history(limit=None).flatten()
        self.webhook: Webhook = utils.get(
            await self.bot.get_channel(constant.CH_SEND_TO).webhooks(),
            name=constant.WEBHOOK_NAME
        )


def setup(bot: Bot):
    bot.add_cog(PickRandomMessage(bot))
