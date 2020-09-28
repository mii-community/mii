import os
import ssl
import traceback
import pathlib

import asyncpg
from discord.ext import commands

import constant


def get_db_context():
    # 残念なことに、ここから--
    ctx = ssl.create_default_context(cafile="")
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    # --ここまでのコードがないと接続ができない。
    return ctx


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
        self.database = await asyncpg.create_pool(
            constant.DATABASE_URL, ssl=get_db_context()
        )

    async def on_ready(self):
        print("logged in as:", self.user.name, self.user.id)


class Help(commands.DefaultHelpCommand):
    def __init__(self):
        super().__init__()
        self.no_category = "その他"
        self.command_attrs["help"] = "コマンド一覧と簡単な説明を表示"

    def get_ending_note(self):
        return (
            f"メッセージに{constant.PIN_EMOJI}リアクションをするとピン留めできます。\n"
            f"スレッドは発言があると一番上に移動します。\n"
            f"!コマンド または @みぃ様 コマンド でも利用することができます。"
        )


if __name__ == "__main__":
    bot = MyBot()
    # bot.loop.run_until_complete(bot.__ainit__())
    bot.run(constant.DISCORD_BOT_TOKEN)
