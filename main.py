import os

import dotenv
dotenv.load_dotenv()

from discord.ext import commands

class MyBot(commands.Bot):

    async def on_ready(self):
        print("logged in:" + self.user.name, self.user.id)

if __name__ == '__main__':
    bot = MyBot(command_prefix='!')
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))