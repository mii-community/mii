# インストールした discord.py を読み込む
import discord

# 自分のBotのアクセストークンに置き換えてください
TOKEN = 'Njc4MDM0Mzc3OTc2MDUzNzYx.Xkc80Q.NTXUeZe9HSPR8IheNo2RuYXZpxQ'

# 接続に必要なオブジェクトを生成
client = discord.Client()

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/register」と発言したら「はじめまして」が返る処理
    if message.content == '/register':
        await message.channel.send('い')

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)