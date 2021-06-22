from io import BytesIO, StringIO
from json import dumps, loads
from typing import Dict, List

from discord import File, Guild, Member, Message, TextChannel
from discord.ext.commands import Bot, Cog

import constant


class RoleManager(Cog):
    __slots__ = ("bot", "store_channel", "target_guild", "role_cache")
    role_cache: Dict[str, List[int]]

    def __init__(self, bot: Bot):
        self.bot = bot

    def has_role_data(self, message: Message) -> bool:
        return (
                message.author == self.bot.user
                and message.attachments
                and message.attachments[0].filename == "role.json"
        )

    @Cog.listener()
    async def on_ready(self):
        self.store_channel: TextChannel = self.bot.get_channel(constant.CH_STORE_ROLE_DATA)
        self.target_guild: Guild = self.store_channel.guild
        role_data = BytesIO()

        try:
            message_with_data: Message = await self.store_channel.history().filter(self.has_role_data).next()
            await message_with_data.attachments[0].save(role_data)
            self.role_cache = loads(role_data.read().decode("UTF-8"))
        except Exception:  # データが読み込めない場合、データが存在しない場合など
            self.role_cache = dict()

        self.role_cache.update(
            {
                str(member.id): [role.id for role in member.roles]
                for member in self.target_guild.members
            }
        )
        await self.role_save()
        print("launched role_save")

    @Cog.listener()
    async def on_member_update(self, before: Member, after: Member):
        if before.roles == after.roles:
            return
        self.role_cache[str(after.id)] = [role.id for role in after.roles]
        await self.role_save()

    @Cog.listener()
    async def on_member_remove(self, member: Member):
        await self.role_save()

    @Cog.listener()
    async def on_member_join(self, member: Member):
        if str(member.id) not in self.role_cache:
            return
        role_ids = self.role_cache[str(member.id)]
        # bool(None) -> false
        roles = list(filter(bool, map(self.target_guild.get_role, role_ids)))
        await member.edit(roles=roles)

    async def role_save(self) -> None:
        role_json = File(
            StringIO(dumps(self.role_cache, indent=4, sort_keys=True)),
            filename="role.json"
        )
        await self.store_channel.send(file=role_json)


def setup(bot: Bot):
    bot.add_cog(RoleManager(bot))
