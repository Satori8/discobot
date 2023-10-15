from re import search


class WordleResultParser:
    def __init__(self):
        i = 0

    @staticmethod
    def parse_message(msg):
        if match := search(r"Wordle \d+ \d/\d", msg.content):
            guesses = int(match.group().split(" ")[2].split("/")[0])
            return f"Wordle", guesses, msg.author

        if match := search(r"СЛОВКО \d+ \d/\d", msg.content):
            guesses = int(match.group().split(" ")[2].split("/")[0])
            return f"Slovko", guesses, msg.author

        if match := search(r"I played contexto\.me #\d+ and got it in \d+ guesses\.", msg.content):
            guesses = int(match.group().split(" ")[8])
            return f"Contexto", guesses, msg.author

    @staticmethod
    def get_stats(messages):
        stats = {}
        for msg in messages:
            res = WordleResultParser.parse_message(msg)
            if not res:
                continue
            game, score, player = res
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
