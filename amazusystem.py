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


def is_bot(user):
    return user.bot


# events
@client.event
async def on_ready():
    await client.get_channel(CH_STARTUP).send("start up succeed. ")


@client.event
async def on_message(message):
    if is_bot(message.author):
        return
    if message.content == "!register":
        await register(message)
    elif message.channel.id == CH_QUESTIONNAIRE:
        await message.add_reaction(EMOJI_SANSEI)
        await message.add_reaction(EMOJI_HANTAI)


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
