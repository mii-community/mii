import discord

client = discord.Client()

# 起動時に動作する処理
@client.event
async def on_ready():
    channel = client.get_channel(678041133179469834)
    await channel.send('起動しました。')

# アカウント登録の処理
@client.event
async def on_message(message):
    # BOTのメッセージに反応させない
    if message.author == client.user:
        return
    # コマンド処理
    if message.content == "!register":
        channel = client.get_channel(678041133179469834)
        user_count = sum(1 for member in channel.members if not member.bot)
        reply = f"{message.author.name}が参加しました。\n{user_count}人目の参加者です。"
        await message.channel.send(reply)

# Botの起動とDiscordサーバーへの接続
client.run('Njc4MDM0Mzc3OTc2MDUzNzYx.XkdcfA.wNgxL19wmcvvXIsysVOxWmNYDhE')

