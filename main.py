import random

from hata import Client, wait_for_interruption, IntentFlag, create_partial_channel_from_id

users = {
    "kuzya": '334727140241047553',
    "bodya": '692105234759155744',
    'inna': '705803066955399209',
    "boris": '582213686094200870',
    "taras": '542056426886135838',
    'strelya': '642786993994072074',
    'satori': '717701525778071572',
    "relock": "582247565987414047",
    "pasha": "721356775697154050"
}

dota_list = [users['bodya'], users['inna'], users['boris'], users['taras'],
             users['satori'], users['pasha'], users['relock']]
civa_list = [users['bodya'], users['inna'], users['taras']]

channels = {
    'ttt': '1002860244516470847'
}

magicball = [
    "It is certain (Бесспорно)",
    "It is decidedly so (Предрешено)",
    "Without a doubt (Никаких сомнений)",
    "Yes — definitely (Определённо да)",
    "You may rely on it (Можешь быть уверен в этом)",
    "As I see it, yes (Мне кажется — «да»)",
    "Most likely (Вероятнее всего)",
    "Outlook good (Хорошие перспективы)",
    "Signs point to yes (Знаки говорят — «да»)",
    "Yes (Да)",
    "Reply hazy, try again (Пока не ясно, попробуй снова)",
    "Ask again later (Спроси позже)",
    "Better not tell you now (Лучше не рассказывать)",
    "Cannot predict now (Сейчас нельзя предсказать)",
    "Concentrate and ask again (Сконцентрируйся и спроси опять)",
    "Don’t count on it (Даже не думай)",
    "My reply is no (Мой ответ — «нет»)",
    "My sources say no (По моим данным — «нет»)",
    "Outlook not so good (Перспективы не очень хорошие)",
    "Very doubtful (Весьма сомнительно)",
]


def randquote():
    with open("quotes.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    return random.choice(lines)


with open('token', 'r') as f:
    token = f.readline()

Nue = Client(token,
             intents=IntentFlag().update_by_keys(
                 guild_users=False,
                 guild_presences=False,

             ))


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

    i = random.randint(0, 100)
    if client.mentioned_in(message) or message.content.startswith("/"):
        if '???' in message.content:
            await client.message_create(message, random.choice(magicball))
        elif "выбери" in message.content:
            if ":" in message.content:
                cont = message.content.split(":")[-1]
            else:
                cont = message.content.split("выбери")[-1]
            cont = cont.replace("?", "")
            cont = cont.replace("или", ",")
            arr = cont.split(',')
            await client.message_create(message, random.choice(arr))
        elif "dota" in message.content:
            msg = ''
            for user in dota_list:
                msg += f"<@{user}> "
            msg += "Cybersport time: Dota!"
            await client.message_create(message.channel, msg)
        elif "civa" in message.content:
            msg = ''
            for user in civa_list:
                msg += f"<@{user}> "
            msg += "Cybersport time: Civa!"
            await client.message_create(message.channel, msg)
        else:
            await client.message_create(message, randquote())


Nue.start()

wait_for_interruption()
