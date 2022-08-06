'''discord bot'''

import os
from secrets import token_hex
import sys
import discord
from dotenv import load_dotenv
import json
import pymongo
import random
import requests


sys.path.append(os.path.abspath("/home/gf/projects/discord_bot/data"))
from data import prompts, replies, one_liners, paras

# Create lists of data for now...

prompts_list = [d['prompt'] for d in prompts.prompts]
replies_list = [d['reply'] for d in replies.replies]
one_liners_list = [d['one_liner'] for d in one_liners.one_liners]
paras_list = [d['para'] for d in paras.paras]

# Local environmental variables
load_dotenv()
token = os.getenv("TOKEN")

# Discord Connection
d_client = discord.Client()

# Mondo DB Connection
conn_str = os.getenv('MONDO_CONN')
m_client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
try:
    print(m_client.server_info())
except Exception as e:
    print("Unable to connect to the Mondo DB Server")
    print(e)

prompts_from_db = m_client.prompts.questions.find()


def get_quote():
    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " - " + json_data[0]['a']
    return(quote)

# def update_replies(user_reply):
#     if "replies" in db.

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

    if any((x:=word) in msg for word in prompts_list):
        await message.channel.send(x.upper() + '? ' + random.choice(replies_list))

d_client.run(token)
