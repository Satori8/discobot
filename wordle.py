from datetime import datetime
from re import search

from constants import Channels


class WordleResultParser:
    def __init__(self):
        i = 0

    @staticmethod
    def parse_message(msg):
        res = []
        if match := search(r"Wordle \d+ \d/\d", msg.content):
            guesses = int(match.group().split(" ")[2].split("/")[0])
            res.append((f"Wordle", guesses, msg.author))

        if match := search(r"СЛОВКО \d+ \d/\d", msg.content):
            guesses = int(match.group().split(" ")[2].split("/")[0])
            res.append((f"Slovko", guesses, msg.author))

        if match := search(r"I played contexto\.me #\d+ and got it in \d+ guesses\.", msg.content):
            guesses = int(match.group().split(" ")[8])
            res.append((f"Contexto", guesses, msg.author))
        return res

    @staticmethod
    def get_stats(messages):
        stats = {}
        for msg in messages:
            res = WordleResultParser.parse_message(msg)
            if not res:
                continue
            for r in res:
                game, score, player = r
                if player.global_name is not None:
                    name = player.global_name
                else:
                    name = player.name

                if game not in stats:
                    stats.update({game: {}})
                if name not in stats[game]:
                    stats[game].update({name: [0, 0]})
                stats[game][name][0] += score
                stats[game][name][1] += 1
        return stats

    @staticmethod
    async def send_stats(ctx, week):
        channel = ctx.bot.get_channel(Channels.Wordle)
        stats_message = ''
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
            await ctx.send("No stats")
            return

        for game in stats:
            stats_message += f" ::: {game} :::\n"
            stats[game] = dict(sorted(stats[game].items(), key=lambda item: item[1][0]))
            for player in stats[game]:
                stats_message += f"{player} : {stats[game][player][0]}"
                if stats[game][player][1] > 1:
                    stats_message += f" after {stats[game][player][1]} attemps"
                stats_message += "\n"
            stats_message += "\n"
        await ctx.send(stats_message)


class Wordle:
    letters = ['e', 'a', 'r', 't', 'o', 'l', 's', 'i', 'n', 'c', 'u', 'y', 'd', 'h', 'p', 'm', 'g', 'b', 'f', 'k', 'w',
               'v',
               'z', 'x', 'q', 'j']

    def __init__(self):
        self.tries = 0
        self.state = 0
        self.guess = ''
        self.words = []
        self.load_words()

    def load_words(self):
        with open('words', 'r') as f:
            self.words = f.readlines()

        with open('used', 'r') as f:
            self.used = f.readlines()

        for word in self.used:
            if word in self.words:
                self.words.remove(word)

        self.words = [word.replace('\n', '') for word in self.words]

    async def solve(self, message):
        feedback, msg = "", ""
        msg_txt = message.content
        if msg_txt == 'restart':
            self.tries = 0
            self.state = 0
            self.load_words()
        elif msg_txt == 'stop':
            msg = "Stop playing wordle"
            self.state = 4

        if self.state == 0:
            msg = f"{len(self.words)} available words remaining.\n"
            msg += f'Try {self.tries + 1}. Your word?'
            self.state = 1
            self.tries += 1

        elif self.state == 1:
            if len(msg_txt) != 5 or not msg_txt.isalpha():
                msg = "Wrong input! Try again"
            else:
                self.guess = msg_txt.lower()
                self.state = 2
                msg = 'Feedback?'

        elif self.state == 2:
            feedback = msg_txt
            if len(feedback) != 5 or not (set(feedback) <= set('wgy')):
                msg = "Wrong input! Try again"
            else:
                self.state = 0
                self.filter_words(feedback)
                try:
                    msg = f"Next guess: {self.words[0]}"
                except IndexError:
                    self.state = 4
                    msg = f"No more words in dictionary!"

        if feedback == 'ggggg':
            self.state = 4
            msg = "GG!"

        await message.author.send(msg)
        if self.state == 0:
            await self.solve(message)

    def filter_words(self, feedback):
        if self.guess in self.words:
            self.words.remove(self.guess)

        remove_list = []
        found_letters = []
        for j in range(5):
            if feedback[j] == 'g':
                found_letters.append(self.guess[j])
                for word in self.words:
                    if word[j] != self.guess[j]:
                        remove_list.append(word)

            if feedback[j] == 'y':
                found_letters.append(self.guess[j])

                for word in self.words:
                    if word[j] == self.guess[j] and word:
                        remove_list.append(word)
                    if self.guess[j] not in word and word:
                        remove_list.append(word)

            if feedback[j] == 'w':
                for word in self.words:
                    if self.guess[j] in word and self.guess[j] not in found_letters:
                        remove_list.append(word)

            for word in remove_list:
                if word in self.words:
                    self.words.remove(word)
