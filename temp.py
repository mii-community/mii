import os

import discord
from discord import Message, Guild, CategoryChannel, TextChannel, VoiceState
import dotenv
from discord.ext.commands import Bot
from typing import Callable, Any, NoReturn
import json

dotenv.load_dotenv()

client = discord.Client()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# consts
CH_STARTUP        = int(os.getenv("CH_STARTUP",         "678483492564107284"))
CH_REGISTER       = int(os.getenv("CH_REGISTER",        "653111096747491328"))
CH_JOIN           = int(os.getenv("CH_JOIN",            "653923742245978129"))
CH_ROOM_MASTER    = int(os.getenv("CH_ROOM_MASTER",     "702042912338346114"))
CH_THREAD_MASTER  = int(os.getenv("CH_THREAD_MASTER",   "702030388033224714"))
CH_VOICE          = int(os.getenv("CH_VOICE",           "655319030428598303"))
CH_VOICE_TEXT     = int(os.getenv("CH_VOICE_TEXT",      "655319030428598303"))

CAT_ROOM          = int(os.getenv("CAT_ROOM",           "702044270609170443"))
CAT_THREAD        = int(os.getenv("CAT_THREAD",         "662856289151615025"))
CAT_ARCHIVE       = int(os.getenv("CAT_ARCHIVE",        "702074011772911656"))

MEMBER_ROLE_NAME  = str(os.getenv("MEMBER_ROLE_NAME",   "member"            ))
ARCHIVE_ROLE_NAME = str(os.getenv("ARCHIVE_ROLE_NAME",  "view archive"      ))


class Mii(Bot):
    
    GUILD_MII:         int = int(os.getenv("GUILD_MII",          "608634154019586059"))
    CH_STARTUP:        int = int(os.getenv("CH_STARTUP",         "678483492564107284"))
    CH_REGISTER:       int = int(os.getenv("CH_REGISTER",        "653111096747491328"))
    CH_JOIN:           int = int(os.getenv("CH_JOIN",            "653923742245978129"))
    CH_ROOM_MASTER:    int = int(os.getenv("CH_ROOM_MASTER",     "702042912338346114"))
    CH_THREAD_MASTER:  int = int(os.getenv("CH_THREAD_MASTER",   "702030388033224714"))
    CH_VOICE:          int = int(os.getenv("CH_VOICE",           "655319030428598303"))
    
    CAT_ROOM:          int = int(os.getenv("CAT_ROOM",           "702044270609170443"))
    CAT_THREAD:        int = int(os.getenv("CAT_THREAD",         "662856289151615025"))
    CAT_ARCHIVE:       int = int(os.getenv("CAT_ARCHIVE",        "702074011772911656"))
    
    MEMBER_ROLE_NAME:  str = str(os.getenv("MEMBER_ROLE_NAME",   "member"            ))
    ARCHIVE_ROLE_NAME: str = str(os.getenv("ARCHIVE_ROLE_NAME",  "view archive"      ))

    voice_members: list = []

    def __init__(self: Bot):
        @self.event
        async def on_ready() -> NoReturn:
            self.guild: Guild = self.get_guild(self.GUILD_MII)
            self.room_category: CategoryChannel = discord.utils.get(self.guild.categories, id=self.CAT_ROOM)
            self.check_rooms()

    async def check_runnable(self: Bot, message: Message, id: int) -> bool:
        if message.channel.id == id:
            return True
        else:
            await message.channel.send("ここでは実行できません。")
            return False

    def get_rooms(self: Bot) -> list[TextChannel]:
        return [
            channel for channel in self.room_category.channels if channel.id != self.CH_ROOM_MASTER
        ]

#    def get_room

    async def register(self: Bot, message: Message) -> NoReturn:
        if await self.check_runnable(message, CH_REGISTER):
            role = discord.utils.get(message.guild.roles, name=MEMBER_ROLE_NAME)
            await message.author.add_roles(role)
            user_count = sum(
                1 for member in client.get_channel(CH_JOIN).members if not member.bot
            )
            await client.get_channel(CH_JOIN).send(
                f"{message.author.mention}が参加しました。"
            )

    async def add_room(self: Bot, message: Message) -> NoReturn:
        if await self.check_runnable(message, id):
            if self.room_exists(message.author.id):
                return
            
            room_category: CategoryChannel = discord.utils.get(message.guild.categories, id=self.CAT_ROOM)
            for channel in room_category.channels:
                channel: TextChannel = channel
                # if channel.type

    async def room_exists(self: Bot, userid: int) -> bool:
        for channel in self.get_rooms():
            # if channel.
            pass
        return False

    async def check_rooms(self: Bot) -> NoReturn:
        for channel in self.get_rooms():
            # if 
            pass


# if __name__ == "__main__":
#     mii = Mii()
#     mii.run(TOKEN)

#######################################################################
#                                  #                                  #
#                                  #                                  #
#                                 ###                                 #
#                                #####                                #
#                              #########                              #
#                           ###############                           #
#                      #########################                      #
#              #########################################              #
# ################################################################### #
# ################################################################### #
#              #########################################              #
#                      #########################                      #
#                           ###############                           #
#                              #########                              #
#                                #####                                #
#                                 ###                                 #
#                                  #                                  #
#                                  #                                  #
#######################################################################


# functions
async def register(message):

    if not message.channel.id == CH_REGISTER:
        return await message.channel.send("ここでは実行できません。")
    
    role = discord.utils.get(message.guild.roles, name=MEMBER_ROLE_NAME)
    await message.author.add_roles(role)
    user_count = sum(
        1 for member in client.get_channel(CH_JOIN).members if not member.bot
    )
    await client.get_channel(CH_JOIN).send(
        f"{message.author.mention}が参加しました。"
    )


async def add_room(message):
    if not message.channel.id == CH_ROOM_MASTER:
        await message.channel.send("ここでは実行できません。")
        return
    ch_name = str(message.author.display_name + "の部屋")
    
    # for channel in CAT_ROOM.channels:
    #     matched = channel
    #     if matched.topic == "room-author: " + str(message.author.id):
    #         await message.channel.send(
    #             f"{message.author.mention} {matched.mention} あなたの部屋はもう作られています。"
    #         )
    #         return
    # わからん！

    if not matched:
        new_channel = await client.get_channel(CAT_ROOM).create_text_channel(name=ch_name)
        channel = client.get_channel(new_channel.id)
        creator = channel.guild.get_member(message.author.id)
        await new_channel.edit(topic="room-author: " + str(message.author.id))
        await channel.set_permissions(creator, manage_messages=True)
        await message.channel.send(
            f"{message.author.mention} {new_channel.mention} を作成しました。"
        )
        return
 

async def open_thread(message):
    if not message.channel.id == CH_THREAD_MASTER:
        await message.channel.send("ここでは実行できません。")
        return
    name_search = message.content
    ch_name = str(name_search[6:])
    matched = discord.utils.get(message.guild.channels, name=ch_name)
    if not matched:
        new_channel = await client.get_channel(CAT_THREAD).create_text_channel(name=ch_name)
        await new_channel.edit(topic="thread-author: " + str(message.author.id))
        await message.channel.send(
            f"{message.author.mention} {new_channel.mention} を作成しました。"
        )
        return
    elif matched.category.id == CAT_THREAD:
        await message.channel.send(
            f"{message.author.mention} {matched.mention} はもう作られています。"
        )
        return
    elif matched.category.id == CAT_ARCHIVE:
        await matched.edit(category=client.get_channel(CAT_THREAD))
        role = discord.utils.get(message.guild.roles, name=ARCHIVE_ROLE_NAME)
        await matched.set_permissions(role, overwrite=None)
        role = discord.utils.get(message.guild.roles, name=MEMBER_ROLE_NAME)
        await matched.set_permissions(role, read_messages=True)
        await matched.edit(topic="thread-author: " + str(message.author.id))
        await message.channel.send(
            f"{message.author.mention} {matched.mention} をアーカイブから戻しました。スレッドの作者は上書きされました。"
        )
        return


async def age(message):
    if message.channel.id == CH_THREAD_MASTER:
        return
    position = client.get_channel(CH_THREAD_MASTER).position + 1
    await message.channel.edit(position=position)


async def close_thread(message):
    if not message.channel.category.id == CAT_THREAD:
        await message.channel.send("ここでは実行できません。")
        return
    if (message.author.guild_permissions.administrator
            or message.channel.topic == "thread-author: " + str(message.author.id)):
        role = discord.utils.get(message.guild.roles, name=MEMBER_ROLE_NAME)
        await message.channel.set_permissions(role, overwrite=None)
        role = discord.utils.get(message.guild.roles, name=ARCHIVE_ROLE_NAME)
        await message.channel.set_permissions(role, read_messages=True, send_messages=False)
        await message.channel.edit(category=client.get_channel(CAT_ARCHIVE))
        return
    else:
        await message.channel.send("権限がありません。")


async def pin(reaction_event):
    channel = client.get_channel(reaction_event.channel_id)
    message = await channel.fetch_message(reaction_event.message_id)
    if message.pinned:
        return
    await message.pin()
    await channel.send(f"{reaction_event.member.name}がピン留めしました。")


async def unpin(reaction_event):
    channel = client.get_channel(reaction_event.channel_id)
    message = await channel.fetch_message(reaction_event.message_id)
    if not message.pinned:
        return
    reaction = discord.utils.get(
        message.reactions, emoji=reaction_event.emoji.name)
    if reaction:
        return
    await message.unpin()
    embed = discord.Embed(
        title=f"送信者:{message.author}",
        description=f"メッセージ内容:{message.content}",
        color=0xFF0000,
    )
    await channel.send("リアクションがゼロになったため、ピン留めが解除されました。", embed=embed)


async def purge(message):
    if message.author.guild_permissions.administrator:
        await message.channel.purge()
        await message.channel.send("✅")
    else:
        await message.channel.send("権限がありません。")


def is_bot(user):
    return user.bot



async def vc_rename(message):
    members = client.get_channel(CH_VOICE).members
    if not message.author in members:
        return
    name = message.content
    named = str(name[8:])
    channel = client.get_channel(CH_VOICE)
    await channel.edit(name=named)
    channel = client.get_channel(CH_VOICE_TEXT)
    await channel.edit(name=named + "-text")



# events
@client.event
async def on_ready():
    await client.get_channel(CH_STARTUP).send("start up succeed. ")
    print("start up succeed.")


@client.event
async def on_message(message):
    if is_bot(message.author):
        return
    if message.content == "!register":
        await register(message)
    elif message.content.startswith("!vc"):
        await vc_rename(message)
    elif message.content == "!open":
        await add_room(message)
    elif message.content.startswith("!open"):
        await open_thread(message)
    elif message.content == "!close":
        await close_thread(message)
    elif message.content == "!purge":
        await purge(message)
    elif message.channel.category.id == CAT_THREAD:
        await age(message)


@client.event
async def on_raw_reaction_add(reaction_event):
    if is_bot(reaction_event.member):
        return
    if reaction_event.emoji.name == "\N{PUSHPIN}":
        await pin(reaction_event)


@client.event
async def on_raw_reaction_remove(reaction_event):
    if reaction_event.emoji.name == "\N{PUSHPIN}":
        await unpin(reaction_event)

@client.event
async def on_voice_state_update(member, before: VoiceState, after: VoiceState) -> NoReturn:
    for member in after.members:
        if not member.name in VOICE_MEMBERS:
            VOICE_MEMBERS.append(member.name)

# 提案 rename
#
# #functions
# async def rename_with_check(message, member_index):
#     if not member_index == 1:
#         return
#     name = message.content
#     named = str(name[8:])
#     channel = client.get_channel(CH_VOICE)
#     await channel.edit(name=named)

# # @client.event
# # async def on_message(message): ←あとでここにぶち込むコード　今ぶち込めよ
#     if message.content.startswith("!rename") and VOICE_MEMBERS:
#         for i in range(len(VOICE_MEMBERS))
#             await rename_with_check(message, i)




# rename kuro type ↓


# functions
# async def vc_rename(message):
#     members = client.get_channel(CH_VOICE).members
#     if not message.author in members:
#         return
#     name = message.content
#     named = str(name[8:])
#     channel = client.get_channel(CH_VOICE)
#     await channel.edit(name=named)
#     channel = client.get_channel(CH_VOICE_TEXT)
#     await channel.edit(name=named + "-text")

# @client.event
# async def on_message(message):
#   if message.content.startswith("!vc"):
#       await vc_rename(message)

client.run(TOKEN)
