import random
from PIL import Image

def parse_strats():
    with open("strats.txt") as f:
        lines = f.readlines()
        strats = []
        for line in lines:
            name, heroes_line = line.split(":")
            heroes = heroes_line.split(",")
            strats.append((name, heroes))

    return strats


def random_strat():
    return random.choice(parse_strats())

def make_hero_image_links(heroes):
    links = []
    for hero in heroes:
        hero = hero.replace(" ", "")
        hero = hero.replace("\n", "")
        links.append(f"icons/{hero}.png")
    return links


def make_portraits_image(heroes):
    filenames = make_hero_image_links(heroes)
    images = [Image.open(x) for x in filenames]
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGBA', (total_width, max_height))

    x_offset = 0
    for im in images:
      new_im.paste(im, (x_offset,0))
      x_offset += im.size[0]

    return new_im

i = 0