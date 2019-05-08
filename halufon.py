# invite link https://discordapp.com/api/oauth2/authorize?client_id=568373639859273738&permissions=522304&scope=bot

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
    dev = message.author.id == 220946685612785664
    if message.content == f"{client.user.mention} לךלישון" and dev:
        await client.close()

    if message.content == f"{client.user.mention} !אקראי":
        hiluf = utils.get_random_hiluf()
        word = hiluf["word"]
        definition = utils.define(utils.denikud(word))
        emb = utils.embedify(hiluf, definition)
        await message.channel.send(f":חילוף של {word}", embed=emb)

    elif message.content == f"{client.user.mention} !עדכן" and dev:
        update = await utils.update()
        await message.channel.send(f"עדכון אחרון: {update}")

    elif message.content.startswith(client.user.mention):
        laaz_word = message.content.replace(client.user.mention + " ", "")
        hiluf = utils.get_hiluf(laaz_word)
        if not hiluf:
            await message.channel.send(f".חילוף ל{laaz_word} לא נמצא")
            return
        definition = utils.define(laaz_word)
        emb = utils.embedify(hiluf, definition)
        word = hiluf["word"]
        await message.channel.send(f":חילוף של {word}", embed=emb)


with open("Token.txt") as f:
    token = f.read()
    client.run(token)
