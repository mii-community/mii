
from discord.ext import commands

import os
import traceback

import dotenv
dotenv.load_dotenv()


EXTENSIONS = [
    "cogs.register",
    "cogs.room",
    "cogs.thread",
    "cogs.rename_ch",
    "cogs.close",
    "cogs.voice",
    "cogs.pin",
    "cogs.purge",
    "cogs.replace_emoji"
]


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or("!"), help_command=Help())
        
        for cog in EXTENSIONS:
            try:
                self.load_extension(cog)
            except Exception:
                traceback.print_exc()

    async def on_ready(self):
        print("logged in:", self.user.name, self.user.id)

class Help(commands.MinimalHelpCommand):
    def __init__(self):
        super().__init__()
        self.no_category = "その他"
        self.command_attrs["help"] = "コマンド一覧と簡単な説明を表示"
    
    def get_opening_note(self):
        return (f"!コマンド または <@678034377976053761> コマンド で利用することができます。")

    def get_ending_note(self):
        return (f"メッセージに📌リアクションをするとピン留めできます。\n"
                f"スレッドは発言があると一番上に移動します。")

if __name__ == '__main__':
    bot = MyBot()
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))
