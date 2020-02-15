# はじまりのじゅもん
import discord
client = discord.Client()

# 起動通知処理部
@client.event
async def on_ready():
    channel = client.get_channel(678041133179469834)
    await channel.send('起動しました。')

# アカウント登録機能処理部
register = client.get_channel(678136433512284208)
join = client.get_channel(678041133179469834)
@client.event
async def on_message(message):
    # if BOTのメッセージだったとき then 無視する
    if message.author.bot: return
    # if !registerを受け取ったとき then チャンネルを照合する
    if message.content == "!register":

            
            # メンバー数を再計算
            user_count = sum(1 for member in join.members if not member.bot)
            # 参加者通知へメッセージ送信
            await join.send(f"{message.author.name}が参加しました。\n{user_count}人目の参加者です。")
            # ダイレクトメッセージを作成
            dm = await message.author.create_dm()
            # ダイレクトメッセージへチュートリアルを送信
            await dm.send(f"{message.author.mention} アカウントが登録されました。\nまず何をすればいいかわからない方へ▽\nstep1: <#655311853844430858> にて自己紹介をしましょう！\nstep2: <#653919145729064970> から各サーバーに入室してください！\n【Tips】スパム防止のため #welcome と #register は非表示になりました。そして #welcome の上位互換の <#661167351412162580> が閲覧できるようになりました。")
        
# Botの起動とDiscordサーバーへの接続処理部
client.run('Njc4MDM0Mzc3OTc2MDUzNzYx.XkdcfA.wNgxL19wmcvvXIsysVOxWmNYDhE')