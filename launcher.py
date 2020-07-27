import os
import ssl
import traceback

import asyncpg
from discord.ext import commands

import constant


async def create_db_pool():
    # 残念なことに、ここから--
    ctx = ssl.create_default_context(cafile="")
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    # --ここまでのコードがないと接続ができない。
    bot.datebase = await asyncpg.create_pool(constant.DATABASE_URL, ssl=ctx)


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or("!"), help_command=Help()
        )
        for cog in [cogs for cogs in os.listdir("./cogs") if cogs.endswith(".py")]:
            try:
                cog = cog.replace(".py", "")
                self.load_extension("cogs." + cog)
                print(f"{cog}.pyは正常に読み込まれました。")
            except:
                traceback.print_exc()

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
    bot.loop.run_until_complete(create_db_pool())
    bot.run(constant.DISCORD_BOT_TOKEN)
