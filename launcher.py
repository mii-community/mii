import os
import ssl
import traceback

import asyncpg
import dotenv
from discord.ext import commands

dotenv.load_dotenv()

# consts
CH_REGISTER = int(os.getenv("CH_REGISTER", "608656664601690142"))
CH_JOIN = int(os.getenv("CH_JOIN", "653923742245978129"))
CH_ROOM_MASTER = int(os.getenv("CH_ROOM_MASTER", "702042912338346114"))
CH_THREAD_MASTER = int(os.getenv("CH_THREAD_MASTER", "702030388033224714"))
CH_VOICE = int(os.getenv("CH_VOICE", "655319117691355166"))
CH_VOICE_TEXT = int(os.getenv("CH_VOICE_TEXT", "655319030428598303"))

CAT_ROOM = int(os.getenv("CAT_ROOM", "702044270609170443"))
CAT_ROOM_ARCHIVE = int(os.getenv("CAT_ROOM_ARCHIVE", "711058666387800135"))
CAT_THREAD = int(os.getenv("CAT_THREAD", "662856289151615025"))
CAT_THREAD_ARCHIVE = int(os.getenv("CAT_THREAD_ARCHIVE", "702074011772911656"))

ROLE_MEMBER = int(os.getenv("ROLE_MEMBER", "652885488197435422"))
ROLE_ARCHIVE = int(os.getenv("ROLE_ARCHIVE", "702420267309203466"))


async def create_db_pool():
    # 残念なことに、ここから--
    ctx = ssl.create_default_context(cafile="")
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    # --ここまでのコードがないと接続ができない。
    bot.datebase = await asyncpg.create_pool(os.getenv("DATABASE_URL"), ssl=ctx)


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
            f"メッセージに📌リアクションをするとピン留めできます。\n"
            f"スレッドは発言があると一番上に移動します。\n"
            f"!コマンド または @みぃ様 コマンド でも利用することができます。"
        )


if __name__ == "__main__":
    bot = MyBot()
    bot.loop.run_until_complete(create_db_pool())
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))
