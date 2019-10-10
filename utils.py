import requests as req
import pickle
from bs4 import BeautifulSoup
import random
import discord

EMOTICONS = {":one:": 1, ":two:": 2, ":three:": 3, ":four:": 4, ":five:": 5, ":six:": 6, ":seven:": 7, ":eight:": 8, ":nine:": 9}

def get_hiluf(laaz_word):
    with open("words.pkl", "rb") as f:
        words = pickle.load(f)
    findings = []
    for word in words["words"]:
        if denikud(word["word"]) == denikud(laaz_word):
            findings.append(word)
        elif denikud(word["word"]).startswith(denikud(laaz_word)):
            findings.append(word)
        elif denikud(laaz_word) in denikud(word["word"]):
            findings.append(word)
    if len(findings) == 1:
        return findings[0]
    if len(findings) > 1:
        return findings

def get_random_hiluf():
    with open("words.pkl", "rb") as f:
        words = pickle.load(f)
        return random.choice(words["words"])

async def update():
    url = "https://halufon.hebrew-academy.org.il/words.php"
    words = req.get(url).json()
    with open("words.pkl", "wb") as f:
        pickle.dump(words, f)
    return words["update"]


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

def check(reaction, user, msg):
    samemsg = reaction.message.id == msg.id
    validreaction = reaction in reaction.message.reactions
    return samemsg and validreaction and not user.bot
