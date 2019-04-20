import requests as req
import pickle
from bs4 import BeautifulSoup
import random
import discord


def get_hiluf(laaz_word):
    with open("words.pkl", "rb") as f:
        words = pickle.load(f)
    for word in words["words"]:
        if denikud(laaz_word) == denikud(word["word"]):
            return word


def get_random_hiluf():
    with open("words.pkl", "rb") as f:
        words = pickle.load(f)
        return random.choice(words["words"])


async def update():
    url = "https://halufon.hebrew-academy.org.il/words.php"
    words = req.get(url).json()
    with open("words.pkl", "wb") as f:
        pickle.dump(words, f)


def denikud(word):
    out = ""
    for char in word:
        if not 1424 <= ord(char) <= 1479:
            out += char
    return out


def define(word):
    url = "https://milog.co.il/" + word
    res = req.get(url)
    soup = BeautifulSoup(res.content, "html.parser")
    element = soup.find("div", {"class": "sr_e"})
    if not element:
        return
    return element.find("div", {"class": "sr_e_txt"}).text


def embedify(hiluf, definition):
    laaz_word = hiluf["word"]
    word_hebrew = hiluf["word_hebrew"]
    explanation = hiluf["explanation"]
    emb = discord.Embed(title=word_hebrew, color=random.randint(0, 16777215))
    if explanation:
        emb.add_field(name=f":הסבר", value=explanation)
    if definition:
        emb.add_field(name=f":משמעות {word_hebrew} ממילוג", value=definition)
    return emb
