from random import randint
from typing import List

from discord import AllowedMentions, Attachment, Message, TextChannel, utils, Webhook
from discord.ext.commands import Bot, Cog
from discord.ext.tasks import loop

import constant


class PickRandomMessage(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.send_random_message.start()

    def slice_five_messages(self) -> List[Message]:
        # メッセージのリストから、5件スライスする。
        i = randint(3, len(self.pickup_source) - 2)
        return self.pickup_source[i - 3:i + 2]

    @staticmethod
    def attachment_to_text(attachment: Attachment) -> str:
        # メッセージの添付ファイルを、
        # 音声データを "[Audio: {ファイル名}]", その他を URL に加工する。
        if attachment.url.endswith((".wav", ".mp3", ".ogg")):
            return f"[Audio: {attachment.filename}]"
        else:
            return attachment.url

    @loop(hours=1)
    async def send_random_message(self) -> None:
        messages = self.slice_five_messages()

        # リスト中央のメッセージリンクを送る。
        await self.webhook.send(content=messages[2].jump_url)

        for message in messages:
            # ステッカーを "[Sticker: {ステッカー名}]" に加工する。
            # スポイラーではないアタッチメントを加工する。
            # 元がスポイラーならスポイラーにしたファイルにする。
            stickers_name = "".join(f"\n[Sticker: {s.name}]" for s in message.stickers)
            attachments_text = "".join(
                f"\n{self.attachment_to_text(a)}" for a in message.attachments if not a.is_spoiler()
            )
            spoiled_files = [await a.to_file(spoiler=True) for a in message.attachments if a.is_spoiler()]

            # Webhookで送信するには、content, embed または file のいずれかが必要なので、
            # すべてなければ content に "[Empty Message]" を代入する。
            # https://discord.com/developers/docs/resources/webhook#execute-webhook
            modified_content = message.content + stickers_name + attachments_text
            if modified_content == "" and (not (message.embeds or spoiled_files)):
                modified_content = "[Empty Message]"

            await self.webhook.send(
                content=modified_content,
                username=f"{message.author.display_name}  {message.created_at.strftime('%Y年%m月%d日 %H時%M分')}",
                avatar_url=message.author.avatar_url,
                files=spoiled_files,
                embeds=message.embeds,
                allowed_mentions=AllowedMentions.none()
            )

    @send_random_message.before_loop
    async def before_send_random_message(self) -> None:
        # Bot の準備が終わるまで待つ。
        # 特定のテキストチャンネルの全メッセージをリストにする。
        # ランダムに抽出したメッセージの送り先の Webhook を取得する。
        await self.bot.wait_until_ready()
        ch_pickup_source: TextChannel = self.bot.get_channel(constant.CH_PICKUP_SOURCE)
        self.pickup_source: List[Message] = await ch_pickup_source.history(limit=None, oldest_first=True).flatten()
        self.webhook: Webhook = utils.get(
            await self.bot.get_channel(constant.CH_SEND_TO).webhooks(),
            name=constant.WEBHOOK_NAME
        )


def setup(bot: Bot) -> None:
    bot.add_cog(PickRandomMessage(bot))
