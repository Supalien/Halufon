# invite link https://discordapp.com/api/oauth2/authorize?client_id=568373639859273738&permissions=522304&scope=bot

# TODO: random word

import discord
import asyncio
import utils
import random

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.mention)
    print(client.user.id)
    print(discord.__version__)
    print('---------')


@client.event
async def on_message(message):
    if message.content == f"{client.user.mention} לךלישון" and message.author.id == 220946685612785664:
        await client.close()

    if message.content.startswith(client.user.mention):
        laaz_word = message.content.replace(client.user.mention + " ", "")
        hiluf = utils.get_hiluf(laaz_word)
        if hiluf:
            word_hebrew = hiluf["word_hebrew"]
            explanation = hiluf["explanation"]
            emb = discord.Embed(title=word_hebrew, color=random.randint(0,16777215))
            if hiluf["explanation"]:
                emb.add_field(name = f":הסבר", value = explanation)
            definition = utils.define(word_hebrew)
            if definition:
                emb.add_field(name = f":משמעות {word_hebrew} ממילוג", value = definition)
            await message.channel.send(f":חילוף של {laaz_word}", embed=emb)
        else:
            await message.channel.send(f"{laaz_word} לא נמצא")

with open("Token.txt") as f:
    token = f.read()
    client.run(token)
