import requests as req
import pickle


def get_hiluf(laaz_word):
    with open("words.pkl", "rb") as f:
        words = pickle.load(f)
    for word in words["words"]:
        if laaz_word == denikud(word["word"]):
            return word


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
