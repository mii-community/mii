
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
]


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or("!"))
        
        for cog in EXTENSIONS:
            try:
                self.load_extension(cog)
            except Exception:
                traceback.print_exc()

    async def on_ready(self):
        print("logged in:", self.user.name, self.user.id)


if __name__ == '__main__':
    bot = MyBot()
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))
