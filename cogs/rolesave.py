import io
import json

import constant
import discord
from discord.ext import commands


class RoleSave(commands.Cog):
    __slots__ = ("bot", "channel", "guild", "cache", "message")

    def __init__(self, bot, name=None):
        self.bot = bot
        self.name = name if name is not None else type(self).__name__
        self.cache = dict()

    @commands.Cog.listener()
    async def on_ready(self):
        self.channel: discord.TextChannel = self.bot.get_channel(constant.CH_ROLESAVE)
        self.guild: discord.Guild = self.channel.guild

        def func1(m: discord.Message):
            return (
                m.author == self.bot.user
                and m.attachments
                and m.attachments[0].filename == "role.json"
            )

        data = io.BytesIO()
        async for message in self.channel.history().filter(func1):
            await message.attachments[0].save(data)
            self.message = message
            break
        try:
            self.cache: dict = json.loads(data.read().decode("UTF-8"))
        except Exception:
            self.cache = {}
        self.cache.update(
            {
                str(m.id): [r.id for r in m.roles if not r.is_default()]
                for m in self.guild.members
            }
        )
        await self._save()
        print("{0}:role_save起動しました".format(self.bot.user))

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if before.roles != after.roles:
            self.cache[str(after.id)] = [
                r.id for r in after.roles if not r.is_default()
            ]
            await self._save()

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        await self._save()

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if str(member.id) in self.cache:
            role_ids = self.cache[str(member.id)]
            [
                self.bot.loop.create_task(member.add_roles(role))
                for role in [self.guild.get_role(i) for i in role_ids]
                if role is not None
            ]

    async def _save(self):
        Data = discord.File(
            io.StringIO(json.dumps(self.cache, indent=4, sort_keys=True)),
            filename="role.json",
        )
        self.message = await self.channel.send(file=Data)

    @property
    def converted_cache(self):
        return {
            self.bot.get_user(int(key)): [self.guild.get_role(i) for i in value]
            for key, value in self.cache.items()
        }


def setup(bot: commands.Bot):
    bot.add_cog(RoleSave(bot))
