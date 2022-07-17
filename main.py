'''discord bot'''

import discord
from dotenv import load_dotenv
import os
import requests
import json
import pymongo
import random

# Local environmental variables
load_dotenv()

# Discord Connection
d_client = discord.Client()

# Mondo DB Connection
conn_str = os.getenv('MONDO_CONN')
m_client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
try:
    print("Connected to Mondo DB Server, details:")
    print(m_client.server_info())
except Exception:
    print("Unable to connect to the Mondo DB Server")

db = m_client.userReplies

user_replies = db.replies

queries = {
    "who",
    "what",
    "when",
    "where",
    "why",
    "how"
}

replies = {
    "Woah there",
    "This is not a drill",
    "You and whose army",
    "That's what she said",
    "In my past life, I was also an idiot",
    "Run in, go pants on fire",
    "It's not too late",
    "It's too late"
}

def get_quote():
    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " - " + json_data[0]['a']
    return(quote)

def update_replies(user_reply):
    if  

@d_client.event
async def on_ready():
    print(f'We have logged in as {d_client.user}')

@d_client.event
async def on_message(message):

    if message.author == d_client.user:
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

d_client.run(os.getenv('TOKEN'))