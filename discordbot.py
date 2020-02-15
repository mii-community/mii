import discord

client = discord.Client()

# 起動時に動作する処理
@client.event
async def on_ready():
    channel = client.get_channel(678041133179469834)
    await channel.send('起動しました。')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/register」と発言したら「はじめまして」が返る処理
    if message.content == '/register':
        channel = client.get_channel(678041133179469834)
        await channel.send('い')


# Botの起動とDiscordサーバーへの接続
client.run('TONjc4MDM0Mzc3OTc2MDUzNzYx.Xkc80Q.NTXUeZe9HSPR8IheNo2RuYXZpxQKEN')