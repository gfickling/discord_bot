'''discord bot'''

import discord
from dotenv import load_dotenv
import os
import requests
import json
import random

load_dotenv()
client = discord.Client()

queries = [
    "who",
    "what",
    "when",
    "where",
    "why",
    "how"
]

replies = [
    "Woah there",
    "This is not a drill",
    "You and whose army",
    "That's what she said",
    "In my past life, I was also an idiot",
    "Run in, go pants on fire",
    "It's not too late",
    "It's too late"
]

def get_quote():
    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " - " + json_data[0]['a']
    return(quote)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    msg = message.content.lower()

    if msg.startswith('$hello'):
        await message.channel.send('Hello!')

    if msg.startswith('$pup'):
        await message.channel.send(file=discord.File('pup.jpeg'))

    if msg.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)
        await message.channel.send(file=discord.File('pup.jpeg'))

    if any((x:=word) in msg for word in queries):
        await message.channel.send(x.upper() + '? ' + random.choice(replies))

client.run(os.getenv('TOKEN'))