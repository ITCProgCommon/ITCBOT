import datetime
import discord
import traceback
from discord.ext import tasks, commands
from os import getenv
import random
import typing
import sqlite3
from discord import TextChannel, VoiceChannel, Role, Intents, app_commands
import asyncio
import csv
import pprint
import sys
import linecache
import time
# from git import *
from extensions.utils.bot_error import *
from extensions.utils.others import *
#a
final_update = get_startup_jst()

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

authority_role = ["", ""]


def failure(e):
    exc_type, exc_obj, tb = sys.exc_info()
    lineno = tb.tb_lineno
    mes = (str(lineno) + ":" + str(type(e)))
    return mes


@client.event
async def on_ready():
    print(f"{color.YELLOW}{client.user}{color.RESET}でログインしました")
    await client.tree.sync()
    await printLog(client, final_update)


@client.event
async def setup_hook():
    await client.load_extension("extensions.ping")
    await client.load_extension("extensions.get_date")
    await client.load_extension("extensions.shuffle")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.ChannelNotFound):
        await ctx.send(embed=any_error("指定したチャンネルが見つかりません"))
    elif isinstance(error, commands.CommandNotFound):
        return
    raise error



""" 
!bot_mes
ボットから好きなチャンネルに送信
(引き継ぎ時修正不要)
"""
#このコメントは消して下さい

@client.hybrid_command(description = "(管理者のみ)")
async def bot_mes(ctx, textchannel: typing.Optional[TextChannel], arg):
    authority = authority_check(client, ctx)
    if not authority:
        await ctx.send(embed=authority_error())
        await printLog(client, "!vote_role : Error00")
        return
    await textchannel.send(arg)




"""
!icon
アイコン画像を取得
(引き継ぎ時修正不要)
"""
@client.command()
async def get_icon(ctx,id):
    authority = authority_check(client, ctx)
    if not authority:
        await ctx.send(embed=authority_error())
        await printLog(client, "!vote_role : Error00")
        return
    guild=client.get_guild(377392053182660609)
    member=guild.get_member(int(id))
    try:
        avatar = member.avatar.url
        await ctx.send(avatar)
    except Exception as e:
        await ctx.send(f"{member.name} - {e}")


"""
!おみくじ
なんとなく
(引き継ぎ時修正不要)
"""


@client.hybrid_command(name="おみくじ", description="今日の運勢を表示します！")
async def おみくじ(ctx):

    unsei = ["大吉 ❤️", "吉 🤍", "小吉 🤍", "凶 💙", "大凶 💙"]

    daikichi_pool = []
    kichi_pool = []
    syoukichi_pool = []
    kyou_pool = []
    daikyou_pool = []

    luckyItem = []
    luckyIMG = []
    num = random.randrange(5)
    title = f"{unsei[num]}"
    with open('data/omikuji.csv') as f:
        reader = csv.reader(f)
        l = [row for row in reader]
        f_T = [list(x) for x in zip(*l)]
        for data in f_T[1]:
            if data == "大吉":
                pass
            elif data == "":
                pass
            else:
                daikichi_pool.append(data)
        for data in f_T[2]:
            if data == "吉":
                pass
            elif data == "":
                pass
            else:
                kichi_pool.append(data)
        for data in f_T[3]:
            if data == "小吉":
                pass
            elif data == "":
                pass
            else:
                syoukichi_pool.append(data)
        for data in f_T[4]:
            if data == "凶":
                pass
            elif data == "":
                pass
            else:
                kyou_pool.append(data)
        for data in f_T[5]:
            if data == "大凶":
                pass
            elif data == "":
                pass
            else:
                daikyou_pool.append(data)
        for data in f_T[8]:
            if data == "ラッキーアイテムimg":
                pass
            elif data == "":
                pass
            else:
                luckyIMG.append(data)
        for data in f_T[7]:
            if data == "ラッキーアイテム":
                pass
            elif data == "":
                pass
            else:
                luckyItem.append(data)

    if num == 0:
        num2 = random.randrange(len(daikichi_pool))
        description_ = daikichi_pool[num2]
    elif num == 1:
        num2 = random.randrange(len(kichi_pool))
        description_ = kichi_pool[num2]
    elif num == 2:
        num2 = random.randrange(len(syoukichi_pool))
        description_ = syoukichi_pool[num2]
    elif num == 3:
        num2 = random.randrange(len(kyou_pool))
        description_ = kyou_pool[num2]
    elif num == 4:
        num2 = random.randrange(len(daikyou_pool))
        description_ = daikyou_pool[num2]
    embed = discord.Embed(
        title=f"{title}", description=description_, color=0xffffff)
    num3 = random.randrange(len(luckyIMG))
    avatar = ctx.message.author.avatar.url
    embed.set_author(
        name=f"{ctx.author.name}さんの今日の運勢は…", icon_url=avatar)
    embed.add_field(name="ラッキーアイテム", value=f"{luckyItem[num3]}")
    try:
        img_url = f"img/omikuji/luckyItem/{luckyIMG[num3]}"
        file = discord.File(fp=img_url, filename="img.png")
    except:
        img_url = f"img/omikuji/luckyItem/noImage.png"
        file = discord.File(fp=img_url, filename="img.png")
    embed.set_thumbnail(url="attachment://img.png")

    await ctx.send(embed=embed, file=file)



"""
on_raw_reaction_add
"""


@ client.event
async def on_raw_reaction_add(payload):
    if payload.member.bot:
        return

    message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
    embeds = message.embeds
    for embed in embeds:  # embedを使用している場合はこの中を使用する。

        title = embed.title
        line = embed.description.split("\n")
        user = client.get_user(payload.user_id)
        user_name = user.name
        number = payload.emoji.name    

    #
    # rulesのメッセージの👍をクリックしたときの処理
    #
    #

    if payload.message_id == 1092095707164463194:
        user = client.get_user(payload.user_id)
        stamp = payload.emoji.name
        await message.remove_reaction(stamp, user)
        await user.send("ITC BOT 2023です！個人にDMを送信しづらい場合や、誰に質問していいかわからない場合はここに質問をしてください。")


"""
!さいころ
サイコロを回して1~6の乱数を生成
(引き継ぎ時修正不要)
"""


@ client.hybrid_command(description = "サイコロを回して1~6の乱数を生成")
async def さいころ(ctx):

    num = random.randrange(6)
    file = f"img/saikoro/saikoro{num}.gif"
    await ctx.send(file=discord.File(file))
    
    

"""
!じゃんけん [グー/チョキ/パー]
(引き継ぎ時修正不要)
"""


@ client.hybrid_command(description = "じゃんけん (グー) (チョキ) (パー)のいずれかを入力")
async def じゃんけん(ctx, arg):
    te = ["gu", "choki", "pa"]
    num = random.randrange(3)
    if arg == "グー":
        file = f"img/janken/gu{te[num]}.gif"
    elif arg == "チョキ":
        file = f"img/janken/choki{te[num]}.gif"
    elif arg == "パー":
        file = f"img/janken/pa{te[num]}.gif"

    await ctx.send(file=discord.File(file))




"""
DMを受け取ったときの処理（TwitterのDMみたいなシステムで相互に返信可）

"""


@ client.listen()
async def on_message(message):
    if message.author == client.user:
        return

    # DMを管理するサーバー
    guild = client.get_guild(1179403386358087783)

    # 本鯖
    itcGuild = client.get_guild(377392053182660609)

    # DMカテゴリーの取得
    DMcategory = client.get_channel(1189967187381866646)

    # DMを受け取る→データベースに送信　
    if type(message.channel) == discord.DMChannel:
        database = await client.get_channel(1189967453242019970).fetch_message(1189970901144453193)
        data_ = database.content.split("\n")
        for i in data_:
            data = i.split(" ")
            if int(data[0]) == message.author.id:
                sendMes = await client.get_channel(int(data[1])).send(message.content)
                await printLog(client, f"BOTが{message.author.name}からDMを受け取りました。\n{sendMes.jump_url}")
                return
        # 初めて送ってきた人はチャンネルを作成する
        channel = await guild.create_text_channel(message.author.name, category=DMcategory)
        send_Mes = await client.get_channel(channel.id).send(f"【{message.author.name}】\n\n{message.content}")
        new_database = f"{database.content}"
        new_database += f"\n{message.author.id} {channel.id}"
        await database.edit(content=new_database)
        await printLog(client, f"BOTが{message.author.name}からDMを初めて受け取りました。\n{sendMes.jump_url}\nDBに{message.author.name}を追加します。\n{database.jump_url}")
        return
    # データベースに返信を書き込む→DM送信
    if message.channel.category == DMcategory:
        database = await client.get_channel(1189967453242019970).fetch_message(1189970901144453193)
        data_ = database.content.split("\n")
        for i in data_:
            data = i.split(" ")
            if int(data[1]) == message.channel.id:
                member = itcGuild.get_member(int(data[0]))
                await printLog(client, f"本鯖に、{member.name}がいます")
                await member.send(message.content)
                await printLog(client, f"BOTから、{member.name}にDMを返信しました。\n{message.jump_url}")
                return

    # ロール一斉送信

    RoleCategory = client.get_channel(1189967653465489409)

    if message.channel.category == RoleCategory:
        await printLog(client, message.channel.topic)
        try:
            role = itcGuild.get_role(int(message.channel.topic))
            await printLog(client, f"文章を@{role.name}ロール保持者に一斉送信します。")

            members = role.members
            for member in members:
                await member.send(message.content)
                await printLog(client, f"|{member.name}に送信しました。")
        except:
            await printLog(client, "DM一斉送信に失敗しました。")
        return

"""
@体験入部のロールが付与された時、その人にBOTから自動でDMを送信する
"""


@ client.event
async def on_member_update(before, after):
    # 本鯖で体験入部ロールが付与されたときの処理
    if before.guild.id == 377392053182660609:
        guild = client.get_guild(377392053182660609)
        role = guild.get_role(851748635023769630)  # 体験入部

        # 送信する文章の取得
        teikeibunCh = client.get_channel(1189967822760181831)
        sendMes = await teikeibunCh.fetch_message(1189968135877562419)

        # roleの差分を取得
        # diff_role = list(set(before.roles) ^ set(after.roles))
        # await printLog(client, f"{before.name}の{diff_role}ロールが変更されました。")
        if (not (role in before.roles)) and (role in after.roles):
            try:
                await before.send(sendMes.content)
                await printLog(client, f"{before.name}に「体験入部が付与された時」のDMを送信しました。")
            except:  # 失敗したら報告
                await printLog(client, f"Error!!：{before.name}に「体験入部が付与された時」のDMを送信できませんでした。")
            return


"""
権限の確認
"""
token = getenv('DISCORD_BOT_TOKEN')
client.run(token)
