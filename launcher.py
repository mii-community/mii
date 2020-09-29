import os
import glob
import traceback
import pathlib
import asyncio

from discord.ext import commands

import constant
from database import Database


class MyBot(commands.Bot):
    def __init__(self, loop):
        super().__init__(
            command_prefix=commands.when_mentioned_or("!"),
            help_command=Help(),
            loop=loop,
        )
        for cog in pathlib.Path("cogs/").glob("*.py"):
            try:
                self.load_extension("cogs." + cog.stem)
                print(f"{cog.stem}.pyは正常に読み込まれました。")
            except:
                traceback.print_exc()

    @classmethod
    async def make_instance(cls, loop):
        instance = cls(loop=loop)
        instance.database = await Database.make_instance()
        return instance

    async def on_ready(self):
        print("logged in as:", self.user.name, self.user.id)


class Help(commands.DefaultHelpCommand):
    def __init__(self):
        super().__init__(no_category="その他", command_attrs={"help": "コマンド一覧と簡単な説明を表示"})

    def get_ending_note(self):
        return (
            f"メッセージに{constant.PIN_EMOJI}リアクションをするとピン留めできます。\n"
            "スレッドは発言があると一番上に移動します。\n"
            "!コマンド または @みぃ様 コマンド でも利用することができます。"
        )


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    bot = loop.run_until_complete(MyBot.make_instance(loop))
    bot.run(constant.DISCORD_BOT_TOKEN)
