'''discord bot'''

import json
import os
import random
import re
import sys

import discord
from dotenv import load_dotenv
import pymongo
import requests

sys.path.append(os.path.abspath("/home/gf/projects/discord_bot/data"))


# Create lists of data from local database files in /data folder

# from data import prompts, replies, one_liners, paras
commands = {'add_reply': 'reply', 'add_one_liner': 'one_liner', 'add_para': 'para'}
# prompts_list = [d['prompt'] for d in prompts.prompts]
# replies_list = [d['reply'] for d in replies.replies]
# one_liners_list = [d['one_liner'] for d in one_liners.one_liners]
# paras_list = [d['para'] for d in paras.paras]

# Local environmental variables
result = load_dotenv()
if result:
    print("Env Loaded")
else:
    print("Local Environment File Not Found")

# Discord Connection
try:
    intents = discord.Intents.default()
    intents.message_content = True
    d_client = discord.Client(intents=intents)
    print("Discord Connected")
except Exception as oops:
    print(oops)

# Open Discord App
# os.system("/Applications/Discord.app/Contents/MacOS/Discord")

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
except Exception as e:
    print("Structure error")
    print(e)
    sys.exit()

def get_answers():
    '''Gets all answers from database'''
    answers = m_client.answers.answers.find()   
    replies, paras, one_liners = ([] for i in range(3))
    for i in answers:
        try:
            replies.append(i['reply'])
        except KeyError:
            pass
        try:
            paras.append(i['para'])
        except KeyError:
            pass
        try:
            one_liners.append(i['one_liner'])
        except KeyError:
            pass
    with open("answers.txt", "w") as f:
        f.write("\n\nReplies:\n\n")
        for r in replies:
            f.write(r)
            f.write("\n")
        f.write("\n\nParas:\n\n")
        for p in paras:
            f.write(p)
            f.write("\n")
        f.write("\n\nOne Liners:\n\n")
        for o in one_liners:
            f.write(o)
            f.write("\n")
        

get_answers()

def db_prompts(prompt):
    '''Call with argument "all" to return all prompts from the database.
        Any other argument checks if prompt exists and returns argument'''
    if prompt == "all":
        prompts_from_db = m_client.prompts.questions.find()
        return prompts_from_db
    prompt_exists = m_client.prompts.questions.find_one({"prompt": prompt})
    if prompt_exists is not None:
        return prompt_exists[prompt]
    else:
        return
try:
    prompts_list = [d['prompt'] for d in db_prompts()]
except TypeError as e:
    print(e)
    print("Prompts list does not exist or is empty")

def get_quote():
    '''Gets a random quote from https://zenquotes.io/api/random'''
    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " - " + json_data[0]['a']
    return(quote)

def check_dupe(value):
    '''Check for duplicate record in the database'''
    exists = m_client.answers.answers.count_documents({'ans_lower': value.lower()})
    if exists != 0:
        return f"'{value}' already exists in the database"
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
    print("User message: ", msg, type(msg))
    print(msg.split(), type(msg.split()))
    user_name = message.author.name

    if msg.startswith('hello'):
        ans = await message.channel.send(f'Hello, {user_name}!')

    if msg.startswith('pup'):
        await message.channel.send(file=discord.File('pup.jpeg'))

    if msg.startswith('inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if any((x:=word) in msg.split() for word in prompts_list):
        print(x)
        await message.channel.send(x.upper() + '? ' + random.choice(replies_list))

    if any((x:=word) in msg for word in commands.keys()):
        answer_type = commands[f'{x}']
        to_add = message.content.replace(x, '').strip()
        if not (ret:=check_dupe(to_add)):
            update_answers(answer_type, to_add)
            await message.channel.send(f"{to_add} added as a {answer_type}")
        if ret:
            await message.channel.send(ret)


d_client.run(os.getenv("TOKEN"))
