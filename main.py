import random
from ids import Users, magicball, Rooms
from hata import Client, wait_for_interruption, IntentFlag, create_partial_channel_from_id


def randquote():
    with open("quotes.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    return random.choice(lines)


with open('token', 'r') as f:
    token = f.readline()

Nue = Client(token, intents=IntentFlag().update_by_keys( guild_users=False, guild_presences=False, ))


@Nue.events
async def ready(client):
    print('online')


@Nue.events
async def message_create(client, message):
    if message.author.is_bot:
        return

    if message.channel.type == 1:
        txt = message.content
        chan = create_partial_channel_from_id(799935025813913632, 0, 0)
        await client.message_create(chan, txt)
        return

    if client.mentioned_in(message) or (message.content and message.content.startswith("/")):
        if '???' in message.content:
            await client.message_create(message, random.choice(magicball))
        elif "обери" in message.content:
            if ":" in message.content:
                cont = message.content.split(":")[-1]
            else:
                cont = message.content.split("обери")[-1]
            cont = cont.replace("?", "")
            cont = cont.replace("чи", ",")
            arr = cont.split(',')
            await client.message_create(message, random.choice(arr))
        elif "dota" in message.content:
            msg = ''
            for user in Users.dota_list:
                msg += f"<@{user}> "
            msg += "Cybersport time: Dota!"
            await client.message_create(message.channel, msg)
        elif "civa" in message.content:
            msg = ''
            for user in Users.civa_list:
                msg += f"<@{user}> "
            msg += "Cybersport time: Civa!"
            await client.message_create(message.channel, msg)
        else:
            await client.message_create(message, randquote())

Nue.start()

wait_for_interruption()
