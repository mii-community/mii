import os
import traceback
import pathlib

from discord.ext import commands

import constant
from database import Database


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or("!"), help_command=Help()
        )
        for cog in pathlib.Path("cogs/").glob("*.py"):
            try:
                self.load_extension("cogs." + cog.stem)
                print(f"{cog.stem}.pyは正常に読み込まれました。")
            except:
                traceback.print_exc()

    async def __ainit__(self):
        self.database = Database()
        await self.database.__ainit__()

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
    bot = MyBot()
    bot.loop.run_until_complete(bot.__ainit__())
    bot.run(constant.DISCORD_BOT_TOKEN)
