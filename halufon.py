# invite link https://discordapp.com/api/oauth2/authorize?client_id=568373639859273738&permissions=522304&scope=bot

import discord
import asyncio
import utils

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
            await message.channel.send(hiluf["word_hebrew"])
        else:
            await message.channel.send(f"\"{laaz_word}\" לא נמצא")

with open("Token.txt") as f:
    token = f.read()
    client.run(token)
