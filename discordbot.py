import discord

client = discord.Client()

# 起動時に動作する処理
@client.event
async def on_ready():
    channel = client.get_channel(678041133179469834)
    await channel.send('起動しました。')

# アカウント登録の処理
register_channel_id = "625220520698183690"
@client.event
async def on_message(message):
    # BOTのメッセージに反応させない
    if message.author == client.user:
        return
    # 別のチャンネルで実行させない
    if message.channel != register_channel_id:
        await message.send("ここでは実行できません。")
        return
    if message.channel == client.get_channel(625220520698183690)
    # コマンド処理
    if message.content == "!register":
        # チャンネルを指定
        channel = client.get_channel(678041133179469834)
        # メンバー数を再計算
        user_count = sum(1 for member in channel.members if not member.bot)
        # 指定したチャンネルへのメッセージ送信
        await message.channel.send(f"{message.author.name}が参加しました。\n{user_count}人目の参加者です。")
        # ダイレクトメッセージへのメッセージ送信
        dm = await message.author.create_dm()
        await clean_content.dm.send(f"{message.author.mention} アカウントが登録されました。\nまず何をすればいいかわからない方へ▽\nstep1: <#655311853844430858> にて自己紹介をしましょう！\nstep2: <#653919145729064970> から各サーバーに入室してください！\n【Tips】スパム防止のため #welcome と #register は非表示になりました。そして #welcome の上位互換の <#661167351412162580> が閲覧できるようになりました。")

# Botの起動とDiscordサーバーへの接続
client.run('Njc4MDM0Mzc3OTc2MDUzNzYx.XkdcfA.wNgxL19wmcvvXIsysVOxWmNYDhE')

