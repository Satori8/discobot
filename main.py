import random
import discord
from discord.ext import commands
import io
import dota2_strats
from constants import Channels, magicball, Users
from wordle import WordleResultParser, Wordle
from threading import Thread
import socket
import time


tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.bind(('0.0.0.0', 8000))
tcp.listen(1)
def accepter():
    while True:
        connection, addr = tcp.accept()
        print('Connected with ' + addr[0] + ':' + str(addr[1]))
        connection.send(b'Connection: OK\n')
        time.sleep(1)

Thread(target=accepter).start()

TEST = True
wordle_mode = False
wordle: Wordle = None

if TEST:
    #with open('test_token', 'r') as f:
    #    token = f.readline()
    token = 'EWde54SiuUsNiIJAKts4z4zeCjNngsR-NmN_tw.cQXZQG.AOykTN3kzNxATNxQzN3YjM2ETM'[::-1]
else:
    with open('token', 'r') as f:
        token = f.readline()

intents = discord.Intents.default()
intents.message_content = True
discobot = commands.Bot(command_prefix='\\', intents=intents)
discobot.remove_command("help")


@discobot.event
async def on_ready():
    print('online')


@discobot.command(name="stats", description="Show wordle stats")
async def send_stats(ctx, *arg):
    week = (arg and arg[0] == "week")
    await WordleResultParser.send_stats(ctx, week)


@discobot.command(name="d", description="Call all people to dota")
async def dota_call(ctx):
    msg = ''
    for user in Users.dota_list:
        msg += f"<@{user}> "
    msg += "Cybersport time: Dota!"
    await ctx.send(msg)


@discobot.command(name="s", description="Random strat for dota")
async def dota_call(ctx):
    name, heroes = dota2_strats.random_strat()
    msg = f'Рандомна страта: {name}\n'
    image = dota2_strats.make_portraits_image(heroes)
    with io.BytesIO() as image_binary:
        image.save(image_binary, 'PNG')
        image_binary.seek(0)
        await ctx.send(msg, file=discord.File(fp=image_binary, filename='image.png'))


@discobot.command(name="strats", description="Show all strats for dota")
async def dota_call(ctx):
    msg = 'Всі записані стратки:\n'
    image = dota2_strats.make_full_strats_image()
    with io.BytesIO() as image_binary:
        image.save(image_binary, 'PNG')
        image_binary.seek(0)
        await ctx.send(msg, file=discord.File(fp=image_binary, filename='image.png'))

@discobot.command(name="w", description="Direct message command. Play wordle.")
@commands.dm_only()
async def play_wordle(ctx):
    global wordle
    await ctx.message.author.send(
        "```Lest play wordle. Give me a word, then follow it with feedback in format:\n\t'*****' where '*': \n\t\t 'y' for yellow letters\n\t\t 'g' for green letters\n\t\t 'w' for white(gray) letters\n For example: 'gwwgy'\n 'stop' - to stop\n 'restart' - to restart```")
    wordle = Wordle()


@discobot.command(name="help", description="Returns all commands available")
async def help(ctx):
    helptext = "```"

    for command in discobot.commands:
        helptext += f"\\{command} - {command.description}\n"
    helptext += "```"
    await ctx.send(helptext)


@discobot.event
async def on_message(message):
    global wordle
    if message.author.bot:
        return

    await discobot.process_commands(message)

    if not message.guild:
        global wordle_mode, wordle
        txt = message.content
        channel = None
        if txt.startswith("Wordle"):
            channel = Channels.Wordle
        if txt.startswith("\\c"):
            if "шинок" in txt.lower():
                channel = Channels.Tavern
            if "wordle" in txt.lower():
                channel = Channels.Wordle
            elif "doka2" in txt.lower():
                channel = Channels.Doka
            elif "test" in txt.lower():
                channel = Channels.Test
            txt = " ".join(txt.split(" ")[2:])

        if wordle:
            await wordle.solve(message)
            if wordle.state == 4:
                wordle = None
        elif channel:
            await discobot.get_channel(channel).send(txt)

    if discobot.user.mentioned_in(message) or (message.content and message.content.startswith("\\")):
        msg = ''

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

        elif message.content == f"<@{discobot.user.id}>":
            msg = random_quote()

        if msg:
            await message.channel.send(msg)


def random_quote():
    with open("quotes.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    return random.choice(lines)


discobot.run(token)
