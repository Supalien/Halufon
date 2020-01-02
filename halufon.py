# invite link https://discordapp.com/api/oauth2/authorize?client_id=568373639859273738&permissions=522304&scope=bot

import discord
import asyncio
import utils
import random
import re

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
    if message.author.bot: return
    dev = message.author.id == 220946685612785664
    match = re.match(r"<@!(\d+)>\s+((.+\s*)+)", message.content)
    if not match or match.group(1) != str(client.user.id): return
    cont = match.group(2)
    if cont == "לךלישון" and dev:
        await client.close()

    elif cont == "!אקראי":
        hiluf = utils.get_random_hiluf()
        word = hiluf["word"]
        definition = utils.define(utils.denikud(word))
        emb = utils.embedify(hiluf, definition)
        await message.channel.send(f":חילוף של {word}", embed=emb)

    elif cont == "!עדכן" and dev:
        update = await utils.update()
        await message.channel.send(f"עדכון אחרון: {update}")

    else:
        laaz_word = cont.strip()
        hiluf = utils.get_hiluf(laaz_word)
        if not hiluf:
            await message.channel.send(f".חילוף למילה {laaz_word} לא נמצא")
            return
        if type(hiluf) == dict:
            definition = utils.define(laaz_word)
            emb = utils.embedify(hiluf, definition)
            word = hiluf["word"]
            await message.channel.send(f":חילוף ל {word}", embed=emb)
        else:
            hiluf = hiluf[:9]
            emb = discord.Embed(
                title="לחץ על המספרים למטה כדי להרחיב. :1234:", color=random.randint(0, 16777215))
            for i, h in enumerate(hiluf):
                emb.add_field(name=f"{i+1}. {h['word']}", value=h["word_hebrew"])
            msg = await message.channel.send(f":נמצאו {len(hiluf)} חילופים ל{laaz_word}", embed=emb)
            for i in range(1, len(hiluf) + 1):
                await msg.add_reaction(str(i) + "\N{combining enclosing keycap}")
            reaction = await client.wait_for('reaction_add', timeout=60.0, check=lambda r, u: utils.check(r, u, msg))
            hiluf = hiluf[int(reaction[0].emoji[0]) - 1]
            definition = utils.define(utils.denikud(hiluf["word_hebrew"]))
            emb = utils.embedify(hiluf, definition)
            word = hiluf["word"]
            await message.channel.send(f":חילוף ל {word}", embed=emb)

with open("Token.txt") as f:
    token = f.read()
    client.run(token)
