import os

import discord
import dotenv

dotenv.load_dotenv()

client = discord.Client()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")


# consts
CH_STARTUP = int(os.getenv("CH_STARTUP", "678483492564107284"))
CH_REGISTER = int(os.getenv("CH_REGISTER", "653111096747491328"))
CH_JOIN = int(os.getenv("CH_JOIN", "653923742245978129"))
CH_ROOM_MASTER = int(os.getenv("CH_ROOM_MASTER", "702042912338346114"))
CH_THREAD_MASTER = int(os.getenv("CH_THREAD_MASTER", "702030388033224714"))
CH_VOICE = int(os.getenv("CH_VOICE", "655319117691355166"))
CH_VOICE_TEXT = int(os.getenv("CH_VOICE_TEXT", "655319030428598303"))

CAT_ROOM = int(os.getenv("CAT_ROOM", "702044270609170443"))
CAT_THREAD = int(os.getenv("CAT_THREAD", "662856289151615025"))
CAT_ARCHIVE = int(os.getenv("CAT_ARCHIVE", "702074011772911656"))

MEMBER_ROLE_NAME = str(os.getenv("MEMBER_ROLE_NAME", "member"))
ARCHIVE_ROLE_NAME = str(os.getenv("ARCHIVE_ROLE_NAME", "view archive"))


# functions
async def register(message):
    if not message.channel.id == CH_REGISTER:
        await message.channel.send("ここでは実行できません。")
        return
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
    matched = discord.utils.get(message.guild.channels, name=ch_name)
    if not matched:
        new_channel = await client.get_channel(CAT_ROOM).create_text_channel(name=ch_name)
        channel = client.get_channel(new_channel.id)
        creator = channel.guild.get_member(message.author.id)
        await channel.set_permissions(creator, manage_messages=True)
        await message.channel.send(
            f"{message.author.mention} {new_channel.mention} を作成しました。"
        )
        return
    elif matched.category.id == CAT_ROOM:
        await message.channel.send(
            f"{message.author.mention} {matched.mention} はもう作られています。"
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
    await channel.send(f"{reaction_event.member.display_name}がピン留めしました。")


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
        title=f"送信者:{message.author.display_name}",
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


async def vc_rename(message):
    if message.channel.id != CH_VOICE_TEXT:
        await message.channel.send(f"{message.author.mention} ここでは実行できません。")
        return
    state = message.author.voice
    if not state:
        await message.channel.send(f"{message.author.mention} VCに参加していないため実行できません。")
        return
    if state.channel.id != CH_VOICE:
        await message.channel.send(f"{message.author.mention} AFKチャンネルに接続中は実行できません。")
        return
    name = message.content
    named = str(name[4:])
    channel = client.get_channel(CH_VOICE)
    await channel.edit(name=named)
    channel = client.get_channel(CH_VOICE_TEXT)
    await channel.edit(name=named + "-text")
    await message.channel.send(f"{message.author.mention} チャンネル名を {named} に上書きしました。")


async def vc_in(member):
    embed = discord.Embed(
        description=f"{member.display_name}が入室しました。",
        colour=0x000000
    )
    await client.get_channel(CH_VOICE_TEXT).send(embed=embed, delete_after=30)


async def vc_out(member):
    embed = discord.Embed(
        description=f"{member.display_name}が退室しました。",
        colour=0x000000
    )
    await client.get_channel(CH_VOICE_TEXT).send(embed=embed, delete_after=30)


async def vc_reset():
    channel = client.get_channel(CH_VOICE)
    await channel.edit(name="vc")
    channel = client.get_channel(CH_VOICE_TEXT)
    await channel.edit(name="vc-text")
    await channel.send(f"接続人数が0になったのでチャンネル名をリセットしました。")


def is_bot(user):
    return user.bot


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
    elif message.content.startswith("!vc "):
        await vc_rename(message)
    elif message.content == "!open":
        await add_room(message)
    elif message.content.startswith("!open "):
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
async def on_voice_state_update(member, before, after):
    if before.channel == after.channel:
        return
    elif not before.channel:
        if after.channel.id != CH_VOICE:
            return
        elif len(after.channel.members) >= 5:
            await vc_in(member)
            return
    elif not after.channel:
        if before.channel.id != CH_VOICE:
            return
        elif len(before.channel.members) >= 5:
            await vc_out(member)
            return
        elif (len(before.channel.members) == 0
                and before.channel.name != "vc"):
            await vc_reset()

client.run(TOKEN)
