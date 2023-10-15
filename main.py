from result_parser import WordleResultParser
from constants import Users, magicball, Channels
from datetime import datetime
import discord
import random

TEST = False


def random_quote():
    with open("quotes.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    return random.choice(lines)


if TEST:
    with open('test_token', 'r') as f:
        token = f.readline()
else:
    with open('token', 'r') as f:
        token = f.readline()

intents = discord.Intents.default()
intents.message_content = True
discobot = discord.Client(intents=intents)


@discobot.event
async def on_ready():
    print('online')


async def send_stats(week):
    stats_message = ''
    channel = discobot.get_channel(Channels.Wordle)
    time = datetime.today()
    time = time.replace(hour=0, minute=0)
    if week:
        stats_message += f" ::: Stats of a week :::\n\n"
        time = time.replace(day=time.day - 7)
    else:
        stats_message += f" ::: Stats of a day :::\n\n"
    history = channel.history(limit=500, after=time)
    messages = [i async for i in history]
    stats = WordleResultParser.get_stats(messages)

    if stats == {}:
        await channel.send("No stats")
        return

    for game in stats:
        stats_message += f" ::: {game} :::\n"
        stats[game] = dict(sorted(stats[game].items(), key=lambda item: item[1][0]))
        for player in stats[game]:
            stats_message += f"{player} : {stats[game][player][0]}"
            if stats[game][player][1]:
                stats_message += f" after {stats[game][player][1]} attemps"
            stats_message += "\n"
        stats_message += "\n"
    await channel.send(stats_message)


@discobot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.type == 1:
        txt = message.content
        await discobot.get_channel(Channels.Tavern).send(txt)

    if discobot.user.mentioned_in(message) or (message.content and message.content.startswith("\\")):
        msg = ''

        if '\\stats' in message.content:
            if 'week' in message.content:
                await send_stats(1)
            else:
                await send_stats(0)

        if '???' in message.content:
            msg = random.choice(magicball)

        elif "\\o" in message.content:
            msg = f"<@{message.author.id}> o/"
        elif "o/" in message.content:
            f"<@{message.author.id}> \\o"

        elif "обери" in message.content:
            if ":" in message.content:
                cont = message.content.split(":")[-1]
            else:
                cont = message.content.split("обери")[-1]
            cont = cont.replace("?", "")
            cont = cont.replace("чи", ",")
            arr = cont.split(',')
            msg = random.choice(arr)

        elif "dota" in message.content or message.content == "\\d":
            for user in Users.dota_list:
                msg += f"<@{user}> "
            msg += "Cybersport time: Dota!"

        elif "civa" in message.content or message.content == "\\c":
            for user in Users.civa_list:
                msg += f"<@{user}> "
            msg += "Cybersport time: Civa!"

        elif message.content == f"<@{discobot.user.id}>":
            msg = random_quote()

        if msg:
            await message.channel.send(msg)


discobot.run(token)
