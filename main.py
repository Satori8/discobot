import time

from hata import Client, wait_for_interruption, IntentFlag, create_partial_channel_from_id
from model import Ebanko
import random

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
ebanko = Ebanko()

mat = [
    "че сука",
    "че блять",
    "че городишь то",
    "че мелешь",
    "слышь бля",
    "я твой рот выебу",
    "я твой рот выебу ты гандон",
    "такой пиздятины вломлю",
    "я приеду твою жопу засуну",
    "ты сука пидарас",
    "слыш щенок блять",
    "давай всретимся такой пиздятины получишь",
    "иди нахуй сука",
    "иди нахуй",
    "да иди ты нахуй",
    "слышь соска ебало закрой",
    "ебало закрыл или ебало закрыла",
    "ебало завали бля",
    "ебало завали блять",
    "ты сука пидарас",
    "да ты мой хуй сосешь гандон",
    "ты с моего хуя будешь кушать",
    "да ты ваще охуевший",
    "слышь хуесосина",
    "тут твой рот выебут",
    "ты хочешь чтобы я тебя выебал просто",
    "с моего хуя хоть десять сделаю тебя устраивает",
    "ебало на нуль",
    "пасть закрой сучара бля",
    "пиздельник завали",
    "ты сучка ебанная",
    "ты сука",
    "ты блять",
    "ты гнида сука",
    "слыш щенок блять",
    "я поймаю тебя тебе больно будет",
    "я приеду такой пиздятины тебе вломлю",
    "сосать заставлю суку бля",
    "тут ваши не ляшут щенок",
    "в глаза смотри мне сука",
    "ты сука пидарас",
    "ты пидарас ,ты гандон я на личности пошел",
    "я ебал твой рот",
    "да я тебе хуй рот засуну блять",
    "ты или ебанутый или",
    "еще есть ебанутые как ты",
    "слыш ты берега походу попутал",
    "да я че то непойму ты или ебанутый или че",
    "ты выебываешся ебаный ты в рот",
    "ты мой хуй кушай блять че звонишь чебуречный",
    "с моего хуя хоть десять сделаю тебя устраивает",
    "кто чеббуреки кушает и кто заказывает того роз ебал ты че ебнутый что ли",
    "блять еще есть такие ебанутые как ты",
    "ты че ебнутый что ли",
    "ебаный в рот ты понимаешь не о чем сейчас",
    "ну а че тогда выебываешся блять",
    "тут твой рот выебут",
    "я ебал таких клиентов с утра до ночи",
    "таких клиентов как ты я ебу в жопу выебу",
    "да ты мой хуй сосешь гандон ты че",
    "ты с моего хуя будешь кушать",
    "ты хочешь чтобы я тебя выебал просто",
    "да я тебе хуй рот засуну блять",
    "я твой рот выебу",
    "я тебя выебу сука",
    "я твой рот выебу ты забудешь где родился и как родился",
    "блять сука я застрелю тебя блять ты че ахуевший гандон ты че",
    "за такие вещи я тебя закопаю",
    "я если поймаю тебе очень больно будет",
    "блять я твой рот ебал ты где сейчас я сейчас приеду",
    "я сейчас приеду я твою жопу засуну",
    "да ты приключений ищешь на свою жопу",
]

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
    if 'mkm' in message.author.full_name and not client.mentioned_in(message):
        if i >= 95:
            await client.message_create(message, ebanko.toxify(message.content))
    elif client.mentioned_in(message) or message.content.startswith("/"):
        if 'mkm' in message.author.full_name:
            if i >= 70:
                await client.message_create(message, ebanko.toxify(message.content))
            else:
                await client.message_create(message, randquote())
        elif 'скажи ему' in message.content:
            await client.message_create(message.channel, f"<@!{users['kuzya']}> " + random.choice(mat))
        elif '???' in message.content:
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
        elif "/2" in message.content:
            await client.message_create(message, ebanko.toxify(message.content))
        else:
            await client.message_create(message, randquote())


Nue.start()

wait_for_interruption()
