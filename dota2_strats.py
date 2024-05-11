import random
from PIL import Image, ImageDraw, ImageFont


def parse_strats():
    with open("strats.txt", encoding="UTF-8") as f:
        lines = f.readlines()
        strats = []
        for line in lines:
            name, heroes_line = line.split(":")
            heroes = heroes_line.split(",")
            strats.append((name, heroes))

    return strats

def parse_hero_strats(hero):
    with open("strats.txt", encoding="UTF-8") as f:
        lines = f.readlines()
        strats = []
        for line in lines:
            if hero not in line:
                continue
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
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    return new_im


def make_name_image(name):
    pass


def make_full_strats_image():
    max_width = 0
    max_height = 0
    strat_images = []
    for strat in parse_strats():
        str = strat[0]
        heroes_image = make_portraits_image(strat[1])
        text_offest = 200
        font = ImageFont.truetype('arial.ttf', 16)
        text_width = font.getmask(str).getbbox()[2]
        new_im = Image.new('RGBA', (heroes_image.width + text_offest, 32))
        d1 = ImageDraw.Draw(new_im)
        d1.text((text_offest - text_width - 5, 7), str, fill=(255, 255, 255), font=font)
        new_im.paste(heroes_image, (text_offest, 0))
        if new_im.width > max_width:
            max_width = new_im.width
        max_height += new_im.height
        strat_images.append(new_im)
    strats_image = Image.new('RGBA', (max_width, max_height))
    y_offset = 0
    for img in strat_images:
        strats_image.paste(img, (0, y_offset))
        y_offset += img.height
    return strats_image

i = 0
