import discord
import os
client = discord.Client()
TOKEN = os.environ["DISCORD_BOT_TOKEN"]

# 定数一覧
CH_STARTUP = 678483492564107284
CH_REGISTER = 653111096747491328
CH_JOIN = 653923742245978129
CH_QUESTIONNAIRE = 660392800399130633
EMOJI_SANSEI = "<:sansei:660392552528347157>"
EMOJI_HANTAI = "<:hantai:660392595159121959>"

# 関数一覧
async def startup():
    await client.get_channel(CH_STARTUP).send("起動しました。")

async def register(message):
    if not message.channel.id == CH_REGISTER:
        await message.channel.send("ここでは実行できません。")
        return
    role = discord.utils.get(message.guild.roles, name="member")
    await message.author.add_roles(role)
    user_count = sum(1 for member in client.get_channel(CH_JOIN).members if not member.bot)
    await client.get_channel(CH_JOIN).send(f"{message.author.name}が参加しました。\n現在の参加者数は{user_count}人です。")
    dm = await message.author.create_dm()
    await dm.send((f"{message.author.mention} アカウントが登録されました。\n"
                    "まず何をすればいいかわからない方へ▽\n"
                    "step1: <#655311853844430858> にて自己紹介をしましょう！\n"
                    "step2: <#653919145729064970> から各サーバーに入室してください！\n"
                    "【Tips】スパム防止のため #welcome と #register は非表示になりました。\n"
                    "そして #welcome の上位互換の <#661167351412162580> が閲覧できるようになりました。"))

async def questionnaire(message):
    await message.add_reaction(EMOJI_SANSEI)
    await message.add_reaction(EMOJI_HANTAI)

async def pin(payload):
    user = client.get_user(payload.user_id)
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    if message.pinned:
        return
    await message.pin()
    await channel.send(f"{user.name}がピン留めしました。")

async def unpin(payload):
    user = client.get_user(payload.user_id)
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    if not message.pinned:
        return
    reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
    if reaction:
        return
    await message.unpin()
    await channel.send("リアクションがゼロになったため、ピン留めが解除されました。")
    embed = discord.Embed(title=f"送信者:{message.author}", description=f"メッセージ内容:{message.content}", color=0xff0000)
    await channel.send(embed=embed)

# イベント一覧
@client.event
async def on_ready():
    await startup()

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content == "!register":
        await register(message)
    if message.channel.id == CH_QUESTIONNAIRE:
        await questionnaire(message)

@client.event
async def on_raw_reaction_add(payload):
    user = client.get_user(payload.user_id)
    if user.bot:
        return
    if payload.emoji.name == "\N{PUSHPIN}":
        await pin(payload)

@client.event
async def on_raw_reaction_remove(payload):
    user = client.get_user(payload.user_id)
    if user.bot:
        return
    if payload.emoji.name == "\N{PUSHPIN}":
        await unpin(payload)

client.run(TOKEN)