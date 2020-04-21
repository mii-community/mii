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
CH_QUESTIONNAIRE = int(os.getenv("CH_QUESTIONNAIRE", "660392800399130633"))
CH_ADDROOM = int(os.getenv("CH_ADDROOM", "702042912338346114"))
CH_ADDTHREAD = int(os.getenv("CH_ADDTHREAD", "702030388033224714"))
CAT_ROOM = int(os.getenv("CAT_ROOM", "702044270609170443"))
CAT_THREAD = int(os.getenv("CAT_THREAD", "662856289151615025"))
EMOJI_SANSEI = os.getenv("EMOJI_SANSEI", "<:sansei:660392552528347157>")
EMOJI_HANTAI = os.getenv("EMOJI_HANTAI", "<:hantai:660392595159121959>")
REGISTER_ROLE_NAME = os.getenv("REGISTER_ROLE_NAME", "member")


# functions
async def register(message):
    if not message.channel.id == CH_REGISTER:
        await message.channel.send("ここでは実行できません。")
        return
    role = discord.utils.get(message.guild.roles, name=REGISTER_ROLE_NAME)
    await message.author.add_roles(role)
    user_count = sum(
        1 for member in client.get_channel(CH_JOIN).members if not member.bot
    )
    await client.get_channel(CH_JOIN).send(
        f"{message.author.name}が参加しました。\n現在の参加者数は{user_count}人です。"
    )
    dm = await message.author.create_dm()
    await dm.send(
        (
            f"{message.author.mention} アカウントが登録されました。\n"
            "まず何をすればいいかわからない方へ▽\n"
            "step1: <#655311853844430858> にて自己紹介をしましょう！\n"
            "step2: <#653919145729064970> から各サーバーに入室してください！\n"
            "【Tips】スパム防止のため #welcome と #register は非表示になりました。\n"
            "そして #welcome の上位互換の <#661167351412162580> が閲覧できるようになりました。"
        )
    )


async def addroom(message):
    if not message.channel.id == CH_ADDROOM:
        await message.channel.send("ここでは実行できません。")
        return
    ch_name = str(message.author.display_name + "の部屋")
    new_channel = await client.get_channel(CAT_ROOM).create_text_channel(name= ch_name)
    await message.channel.send(
        f"{message.author.mention} {new_channel.mention} を作成しました。"
    ) 
    channel = client.get_channel(new_channel.id)
    creator = channel.guild.get_member(message.author.id)
    await channel.set_permissions(creator, manage_channels=True, manage_messages=True, manage_permissions=True)


async def addthread(message):
    if not message.channel.id == CH_ADDTHREAD:
        await message.channel.send("ここでは実行できません。")
        return
    name_search = message.content
    ch_name = str(name_search[6:])
    new_channel = await client.get_channel(CAT_THREAD).create_text_channel(name= ch_name) 
    reply = f"{message.author.mention} {new_channel.mention} を作成しました。"
    await message.channel.send(reply)


async def pin(reaction_event):
    channel = await client.fetch_channel(reaction_event.channel_id)
    message = await channel.fetch_message(reaction_event.message_id)
    if message.pinned:
        return
    await message.pin()
    await channel.send(f"{reaction_event.member.name}がピン留めしました。")


async def unpin(reaction_event):
    channel = await client.fetch_channel(reaction_event.channel_id)
    message = await channel.fetch_message(reaction_event.message_id)
    if not message.pinned:
        return
    reaction = discord.utils.get(message.reactions, emoji=reaction_event.emoji.name)
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
    elif message.content == "!open":
        await addroom(message)
    elif message.content.startswith('!open'):
        await addthread(message)
    elif message.channel.id == CH_QUESTIONNAIRE:
        await message.add_reaction(EMOJI_SANSEI)
        await message.add_reaction(EMOJI_HANTAI)
    elif message.content == '!purge':
        await purge(message)


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


client.run(TOKEN)
