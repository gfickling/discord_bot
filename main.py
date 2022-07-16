'''discord bot script'''

#Discord API Wrapper
import discord
from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()
client = discord.Client()

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

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$pup'):
        await message.channel.send(file=discord.File('pup.jpeg'))

    if message.content.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)
        await message.channel.send(file=discord.File('pup.jpeg'))

client.run(os.getenv('TOKEN'))