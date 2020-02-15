# はじまりのじゅもん
import discord
client = discord.Client()

# 起動通知処理部
@client.event
async def on_ready():
    channel = client.get_channel(678041133179469834)
    await channel.send('起動しました。')

# アカウント登録機能処理部
@client.event
async def on_message(message):
    if message.author.bot: return
    if message.content == "!register":
        if message.channel.id == 678136433512284208:
            role = discord.utils.get(message.guild.roles, name="member")
            await message.author.add_roles(role)
            join = client.get_channel(678041133179469834)
            user_count = sum(1 for member in join.members if not member.bot)
            await join.send(f"{message.author.name}が参加しました。\n{user_count}人目の参加者です。")
            dm = await message.author.create_dm()
            await dm.send(f"{message.author.mention} アカウントが登録されました。\nまず何をすればいいかわからない方へ▽\nstep1: <#655311853844430858> にて自己紹介をしましょう！\nstep2: <#653919145729064970> から各サーバーに入室してください！\n【Tips】スパム防止のため #welcome と #register は非表示になりました。そして #welcome の上位互換の <#661167351412162580> が閲覧できるようになりました。")
        else: await message.channel.send("ここでは実行できません。")

# Botの起動とDiscordサーバーへの接続処理部
client.run('Njc4MDM0Mzc3OTc2MDUzNzYx.XkdcfA.wNgxL19wmcvvXIsysVOxWmNYDhE')