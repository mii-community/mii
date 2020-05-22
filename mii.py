import os

import discord
import dotenv

dotenv.load_dotenv()

client = discord.Client()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")


# consts
CH_STARTUP = int(os.getenv("CH_STARTUP", "678483492564107284"))
CH_REGISTER = int(os.getenv("CH_REGISTER", "608656664601690142"))
CH_JOIN = int(os.getenv("CH_JOIN", "653923742245978129"))
CH_ROOM_MASTER = int(os.getenv("CH_ROOM_MASTER", "702042912338346114"))
CH_THREAD_MASTER = int(os.getenv("CH_THREAD_MASTER", "702030388033224714"))
CH_VOICE = int(os.getenv("CH_VOICE", "655319117691355166"))
CH_VOICE_TEXT = int(os.getenv("CH_VOICE_TEXT", "655319030428598303"))

CAT_ROOM = int(os.getenv("CAT_ROOM", "702044270609170443"))
CAT_THREAD = int(os.getenv("CAT_THREAD", "662856289151615025"))
CAT_THREAD_ARCHIVE = int(os.getenv("CAT_THREAD_ARCHIVE", "702074011772911656"))
CAT_ROOM_ARCHIVE = int(os.getenv("CAT_THREAD_ARCHIVE", "711058666387800135"))

MEMBER_ROLE_NAME = str(os.getenv("MEMBER_ROLE_NAME", "member"))
ARCHIVE_ROLE_NAME = str(os.getenv("ARCHIVE_ROLE_NAME", "view archive"))

emojis_main = {
    "あ": "99_aa", "い": "98_ii", "う": "97_uu", "え": "96_ee", "お": "95_oo",
    "か": "94_ka", "き": "93_ki", "く": "92_ku", "け": "91_ke", "こ": "90_ko",
    "さ": "89_sa", "し": "88_si", "す": "87_su", "せ": "86_se", "そ": "85_so",
    "た": "84_ta", "ち": "83_ti", "つ": "82_tu", "て": "81_te", "と": "80_to",
    "な": "79_na", "に": "78_ni", "ぬ": "77_nu", "ね": "76_ne", "の": "75_no",
    "は": "74_ha", "ひ": "73_hi", "ふ": "72_hu", "へ": "71_he", "ほ": "70_ho",
    "ま": "69_ma", "み": "68_mi", "む": "67_mu", "め": "66_me", "も": "65_mo",
    "や": "64_ya", "ゆ": "63_yu", "よ": "62_yo",
    "ら": "61_ra", "り": "60_ri", "る": "59_ru", "れ": "58_re", "ろ": "57_ro",
    "わ": "56_wa", "を": "55_wo",
    "ん": "54_nn",
    "ぁ": "53_la", "ぃ": "52_li", "ぅ": "51_lu", "ぇ": "50_le", "ぉ": "49_lo",
    "っ": "48_ltu",
    "ゃ": "47_lya", "ゅ": "46_lyu", "ょ": "45_lyo",
    "〜": "44_nobasi", "ー": "44_nobasi",
    "！": "43_exclamation", "!": "43_exclamation",
    "？": "42_question", "?": "42_question",
    "、": "41_touten", ",": "41_touten",
    "。": "40_kuten", ".": "40_kuten"
}

emojis_sub1 = {
    "が": "94_ka", "ぎ": "93_ki", "ぐ": "92_ku", "げ": "91_ke", "ご": "90_ko",
    "ざ": "89_sa", "じ": "88_si", "ず": "87_su", "ぜ": "86_se", "ぞ": "85_so",
    "だ": "84_ta", "ぢ": "83_ti", "づ": "82_tu", "で": "81_te", "ど": "80_to",
    "ば": "74_ha", "び": "73_hi", "ぶ": "72_hu", "べ": "71_he", "ぼ": "70_ho",
}

emojis_sub2 = {
    "ぱ": "74_ha", "ぴ": "73_hi", "ぷ": "72_hu", "ぺ": "71_he", "ぽ": "70_ho",
}


# functions
def is_bot(user):
    return user.bot


def get_vc_channel(before, after):
    if after.channel:
        return after.channel
    elif before.channel:
        return before.channel


async def send_help(message):
    embed = discord.Embed(
        title="各種機能について",
        description=(
            "**!open**\nあなたの部屋を作成します。\n\n"
            "**!open <name>**\n指定した名前のスレッドを作成します。\n\n"
            "**!rename <name>**\n自分の作成した部屋/スレッドをリネームします。\n\n"
            "**!close**\n自分の作成したスレッドをアーカイブします。\n\n"
            "**!vc <name>**\nVC参加中のVC名を変更します。\n\n"
            "**!emoji <text>**\nサポート済みの絵文字に置き換えます。\n\n"
            "**!purge <number>**\n指定された数のメッセージを一括削除します。\n"
            "全削除する場合は<number>にallと指定してください\n\n"
            "**Others**\n"
            "メッセージに📌リアクションをするとピン留めできます。\n"
            "スレッドは発言があると一番上に移動します。\n"
            "--------------------------------------"
        ),
        color=0x000000
    )
    embed.set_footer(text="*このメッセージは60秒後に自動で削除されます。")
    await message.delete()
    await message.channel.send(embed=embed, delete_after=60)


async def register(reaction_event):
    channel = client.get_channel(CH_REGISTER)
    message = await channel.fetch_message(reaction_event.message_id)
    guild = discord.utils.find(
        lambda g: g.id == reaction_event.guild_id, client.guilds)
    member = discord.utils.find(
        lambda m: m.id == reaction_event.user_id, guild.members)
    role = discord.utils.get(guild.roles, name=MEMBER_ROLE_NAME)
    if role in member.roles:
        await message.remove_reaction(reaction_event.emoji, member)
        return
    await message.remove_reaction(reaction_event.emoji, member)
    await member.add_roles(role)
    await client.get_channel(CH_JOIN).send(
        f"{reaction_event.member.mention}が参加しました。"
    )


async def open_room(message):
    if message.channel.id != CH_ROOM_MASTER:
        await message.channel.send("ここでは実行できません。")
        return
    category = client.get_channel(CAT_ROOM_ARCHIVE)
    for channel in category.channels:
        if channel.topic == "room-author: " + str(message.author.id):
            await channel.edit(category=client.get_channel(CAT_ROOM))
            role = discord.utils.get(
                message.guild.roles, name=ARCHIVE_ROLE_NAME)
            await channel.set_permissions(role, overwrite=None)
            role = discord.utils.get(
                message.guild.roles, name=MEMBER_ROLE_NAME)
            await channel.set_permissions(role, read_messages=True)
            creator = channel.guild.get_member(message.author.id)
            await channel.set_permissions(creator, manage_messages=True)
            await message.channel.send(
                f"{message.author.mention} {channel.mention} をアーカイブから戻しました。"
            )
            return
    category = client.get_channel(CAT_ROOM)
    for channel in category.channels:
        if channel.topic == "room-author: " + str(message.author.id):
            await message.channel.send(
                f"{message.author.mention} {channel.mention} あなたの部屋はもう作られています。"
            )
            return
    named = message.author.display_name + "の部屋"
    new_channel = await category.create_text_channel(name=named)
    creator = new_channel.guild.get_member(message.author.id)
    await new_channel.edit(topic="room-author: " + str(message.author.id))
    await new_channel.set_permissions(creator, manage_messages=True)
    await message.channel.send(
        f"{message.author.mention} {new_channel.mention} を作成しました。"
    )


async def open_thread(message):
    if message.channel.id != CH_THREAD_MASTER:
        await message.channel.send("ここでは実行できません。")
        return
    name = message.content
    named = str(name[6:])
    matched = discord.utils.get(message.guild.channels, name=named)
    if not matched:
        new_channel = await client.get_channel(CAT_THREAD).create_text_channel(name=named)
        await new_channel.edit(topic="thread-author: " + str(message.author.id))
        await message.channel.send(
            f"{message.author.mention} {new_channel.mention} を作成しました。"
        )
    elif matched.category.id == CAT_THREAD:
        await message.channel.send(
            f"{message.author.mention} {matched.mention} はもう作られています。"
        )
    elif matched.category.id == CAT_THREAD_ARCHIVE:
        await matched.edit(category=client.get_channel(CAT_THREAD))
        role = discord.utils.get(message.guild.roles, name=ARCHIVE_ROLE_NAME)
        await matched.set_permissions(role, overwrite=None)
        role = discord.utils.get(message.guild.roles, name=MEMBER_ROLE_NAME)
        await matched.set_permissions(role, read_messages=True)
        await matched.edit(topic="thread-author: " + str(message.author.id))
        await message.channel.send(
            f"{message.author.mention} {matched.mention} をアーカイブから戻しました。スレッドの作者は上書きされました。"
        )


async def age_thread(message):
    if message.channel.id == CH_THREAD_MASTER:
        return
    position = client.get_channel(CH_THREAD_MASTER).position + 1
    await message.channel.edit(position=position)


async def close_ch(message):
    if (message.channel.category.id != CAT_ROOM
            and message.channel.category.id != CAT_THREAD):
        await message.channel.send("ここでは実行できません。")
        return
    elif (message.channel.topic != "room-author: " + str(message.author.id)
            and message.channel.topic != "thread-author: " + str(message.author.id)):
        await message.channel.send("権限がありません。")
        return
    elif message.channel.category.id == CAT_ROOM:
        await message.channel.edit(category=client.get_channel(CAT_ROOM_ARCHIVE))
    elif message.channel.category.id == CAT_THREAD:
        await message.channel.edit(category=client.get_channel(CAT_THREAD_ARCHIVE))
    role = discord.utils.get(message.guild.roles, name=MEMBER_ROLE_NAME)
    await message.channel.set_permissions(role, overwrite=None)
    role = discord.utils.get(message.guild.roles, name=ARCHIVE_ROLE_NAME)
    await message.channel.set_permissions(role, read_messages=True, send_messages=False)


async def rename_ch(message):
    if (message.channel.category.id != CAT_ROOM
            and message.channel.category.id != CAT_THREAD):
        await message.channel.send("ここでは実行できません。")
        return
    elif (message.channel.topic != "room-author: " + str(message.author.id)
            and message.channel.topic != "thread-author: " + str(message.author.id)):
        await message.channel.send("権限がありません。")
        return
    name = message.content
    named = str(name[8:])
    await message.channel.edit(name=named)
    await message.channel.send(f"{message.author.mention} チャンネル名を {named} に上書きしました。")


async def rename_vc(message):
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


async def notify_vc(member, before, after):
    if after.channel:
        embed = discord.Embed(
            description=f"{member.display_name}が入室しました。",
            colour=0x000000
        )
        await client.get_channel(CH_VOICE_TEXT).send(embed=embed, delete_after=60)
    elif before.channel:
        embed = discord.Embed(
            description=f"{member.display_name}が退室しました。",
            colour=0x000000
        )
        await client.get_channel(CH_VOICE_TEXT).send(embed=embed, delete_after=60)


async def reset_vc_name():
    channel = client.get_channel(CH_VOICE)
    await channel.edit(name="vc")
    channel = client.get_channel(CH_VOICE_TEXT)
    await channel.edit(name="vc-text")
    embed = discord.Embed(
        description=f"接続人数が0になったのでチャンネル名をリセットしました。",
        colour=0x000000
    )
    await channel.send(embed=embed, delete_after=60)


async def check_webhook(message):
    webhooks = await message.channel.webhooks()
    if not webhooks:
        webhook = await message.channel.create_webhook(name="mii")
        return webhook
    for webhook in webhooks:
        if webhook.name == "mii":
            return webhook
    webhook = await message.channel.create_webhook(name="mii")
    return webhook


def get_emoji_id(message, emoji_alias):
    get_emoji = discord.utils.get(message.guild.emojis, name=emoji_alias)
    emoji_id = get_emoji.id
    return emoji_id


def get_replaced_char(message, replace_char):
    if replace_char in emojis_main:
        emoji_alias = emojis_main[replace_char]
        emoji_id = get_emoji_id(message, emoji_alias)
        replaced_char = "<:" + emoji_alias + ":" + str(emoji_id) + ">"
        return replaced_char
    elif replace_char in emojis_sub1:
        emoji_alias = emojis_sub1[replace_char]
        emoji_id = get_emoji_id(message, emoji_alias)
        replaced_char = "<:" + emoji_alias + ":" + str(emoji_id) + ">" + "ﾞ "
        return replaced_char
    elif replace_char in emojis_sub2:
        emoji_alias = emojis_sub2[replace_char]
        emoji_id = get_emoji_id(message, emoji_alias)
        replaced_char = "<:" + emoji_alias + ":" + str(emoji_id) + ">" + "ﾟ "
        return replaced_char
    else:
        replaced_char = replace_char
        return replaced_char


async def replace_emoji(message):
    webhook = await check_webhook(message)
    replace_string = str(message.content[7:])
    replaced_string = []
    for replace_char in replace_string:
        replaced_char = get_replaced_char(message, replace_char)
        replaced_string.append(replaced_char)
    content = ">>> " + "".join(replaced_string)
    await message.delete()
    await webhook.send(
        avatar_url=message.author.avatar_url,
        username=message.author.display_name,
        content=content
    )


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
    if not message.author.guild_permissions.manage_messages:
        await message.channel.send(f"メッセージ管理の権限がありません。")
        return
    num = message.content[7:]
    if num == "all":
        await message.channel.purge(limit=None)
        await message.channel.send("✅")
        return
    try:
        num = int(num)
    except:
        await message.channel.send(
            f"不正な引数です。削除するメッセージ数か、全て削除する場合はallを入力してください。"
        )
        return
    await message.channel.purge(limit=num)
    await message.channel.send("✅")


# events
@client.event
async def on_ready():
    await client.get_channel(CH_STARTUP).send("start up succeed. ")
    print("start up succeed.")


@client.event
async def on_message(message):
    if is_bot(message.author):
        return
    elif message.content == "!open":
        await open_room(message)
    elif message.content.startswith("!open "):
        await open_thread(message)
    elif message.content.startswith("!rename "):
        await rename_ch(message)
    elif message.content == "!close":
        await close_ch(message)
    elif message.content.startswith("!vc "):
        await rename_vc(message)
    elif message.content.startswith("!purge "):
        await purge(message)
    elif message.content.startswith("!emoji "):
        await replace_emoji(message)
    elif message.content == "!help":
        await send_help(message)
    if message.channel.category.id == CAT_THREAD:
        await age_thread(message)


@client.event
async def on_raw_reaction_add(reaction_event):
    if is_bot(reaction_event.member):
        return
    if reaction_event.emoji.name == "\N{PUSHPIN}":
        await pin(reaction_event)
    elif reaction_event.channel_id == CH_REGISTER:
        await register(reaction_event)


@client.event
async def on_raw_reaction_remove(reaction_event):
    if reaction_event.emoji.name == "\N{PUSHPIN}":
        await unpin(reaction_event)


@client.event
async def on_voice_state_update(member, before, after):
    if before.channel == after.channel:
        return
    channel = get_vc_channel(before, after)
    if channel.id != CH_VOICE:
        return
    i = len(channel.members)
    if i >= 5:
        await notify_vc(member, before, after)
    elif i == 0 and channel.name != "vc":
        await reset_vc_name()


client.run(TOKEN)
