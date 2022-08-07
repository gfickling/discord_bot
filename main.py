'''discord bot'''

import os
import sys
import discord
from dotenv import load_dotenv
import json
import pymongo
import random
import re
import requests


sys.path.append(os.path.abspath("/home/gf/projects/discord_bot/data"))
from data import prompts, replies, one_liners, paras

# Create lists of data for now...

commands = {'add_reply': 'reply', 'add_one_liner': 'one_liner', 'add_para': 'para'}
prompts_list = [d['prompt'] for d in prompts.prompts]
replies_list = [d['reply'] for d in replies.replies]
one_liners_list = [d['one_liner'] for d in one_liners.one_liners]
paras_list = [d['para'] for d in paras.paras]

# Local environmental variables
try:
    load_dotenv()
    print("Env Loaded")
except False:
    print("Local Environment File Not Found")

# Discord Connection
d_client = discord.Client()

# Mondo DB Connection
conn_str = os.getenv('MONDO_CONN')
m_client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
try:
    print("Client Server Version: " + m_client.server_info()['version'])
except Exception as e:
    print("Unable to connect to the Mondo DB Server")
    print(e)
    sys.exit(1)

# MongoDB Structure
try:
    db_list = m_client.list_databases()
    db_name_list = m_client.list_database_names()
    coll_list = []
    for db in db_list:
        db_name = db['name']
        if db_name not in ['admin', 'local']:
            db_is = m_client.get_database(db_name)
            colls = db_is.list_collection_names()
            for coll in colls:
                coll_list.append((db_name, coll))
    print("Databases: ", db_name_list)
    print("Collections: ", coll_list)
except Exception as e:
    print("Structure error")
    print(e)
    sys.exit()

def get_answers():
    '''Gets all answers from database'''


prompts_from_db = m_client.prompts.questions.find()

def get_quote():
    '''Gets a random quote from https://zenquotes.io/api/random'''
    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " - " + json_data[0]['a']
    return(quote)

def check_dupe(answer_type, value):
    '''Check for duplicate record in the database'''
    exists = m_client.answers.answers.count_documents({answer_type: re.compile(value, re.IGNORECASE)})
    if exists != 0:
        return f"'{value}' already exists as a {answer_type} option"
    return False

def update_answers(section, user_reply):
    '''Insert a user generated reply into the database'''
    to_add = {section: user_reply, 'ans_lower': user_reply.lower()}
    post_id = m_client.answers.answers.insert_one(to_add).inserted_id
    print(f'User reply {user_reply} added, id: {post_id}')

@d_client.event
async def on_ready():
    print(f'We have logged in as {d_client.user}')

@d_client.event
async def on_message(message):

    if message.author == d_client.user:
        return

    msg = message.content.lower()
    user_name = message.author.name

    if msg.startswith('hello'):
        await message.channel.send(f'Hello, {user_name}!')

    if msg.startswith('pup'):
        await message.channel.send(file=discord.File('pup.jpeg'))

    if msg.startswith('inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if any((x:=word) in msg for word in prompts_list):
        await message.channel.send(x.upper() + '? ' + random.choice(replies_list))

    if any((x:=word) in msg for word in commands.keys()):
        answer_type = commands[f'{x}']
        to_add = message.content.replace(x, '').strip()
        if not (ret:=check_dupe(answer_type, to_add)):
            update_answers(answer_type, to_add)
            await message.channel.send(f"{to_add} added as a {answer_type}")
        if ret:
            await message.channel.send(ret)


d_client.run(os.getenv("TOKEN"))
