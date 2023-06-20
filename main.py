'''discord bot'''

import os
import random
import sys

import discord
from dotenv import load_dotenv
import pymongo
from helpers import build_help_message, check_dupe, db_prompts, get_answers, get_quote, update_answers

sys.path.append(os.path.abspath("/home/gf/projects/discord_bot/data"))


# Create lists of data from local database files in /data folder

# from data import prompts, replies, one_liners, paras
commands = {'add_reply': 'reply', 'add_one_liner': 'one_liner', 'add_para': 'para'}
contractions = ["'d", "'s", "'ll", "'re", "'ve"]
# prompts = [d['prompt'] for d in prompts.prompts]
# replies = [d['reply'] for d in replies.replies]
# one_liners = [d['one_liner'] for d in one_liners.one_liners]
# paras = [d['para'] for d in paras.paras]

# Local environmental variables
RESULT = load_dotenv()
if RESULT:
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

# load prompts and answers from database
try:
    replies, paras, one_liners = get_answers(m_client)
    prompts = [d['prompt'] for d in db_prompts(m_client, "all")]
    if not prompts:
        print("Prompts list is empty")
except Exception as e:
    print("Problem loading database: ",e)

# add contractions to prompts
try:
    prompts_to_update = prompts.copy()
    for prompt in prompts_to_update:
        for cont in contractions:
            prompts.append(prompt + cont)

except Exception as e:
    print("Problem with contractions", e)




@d_client.event
async def on_ready():
    '''Connected to Discord?'''    
    print(f'We have logged in as {d_client.user}')
    
@d_client.event
async def on_message(message):
    '''Interact with Discord'''
    if message.author == d_client.user:
        return
    print(message.content)
    msg_list = message.content.lower().split()
    print(msg_list)
    user_global_name = message.author.global_name
    if d_client.user.mentioned_in(message):#only reply to mentions
        if 'hello' in msg_list:
            await message.channel.send(f'Hello, {user_global_name}!')
            return

        elif 'pup' in msg_list:
            await message.channel.send(file=discord.File('pup.jpeg'))
            return
        
        elif any((x:=word) in ['inspire', 'inspiring', 'inspiration','inspirational'] for word in msg_list):
                print(x)
                quote = get_quote()
                await message.channel.send(quote)
                return
        
        elif 'help' in msg_list:
            help_message = build_help_message(prompts, 'help')
            await message.channel.send(help_message)
            return
        
        elif 'commands' in msg_list:
            help_message = build_help_message(commands, 'commands')
            await message.channel.send(help_message)
            return

        elif any((x:=word) in msg_list for word in prompts):
            print(x)
            await message.channel.send("All I can say is " + random.choice(replies))
            return
        
        elif any('?' in s for s in msg_list[-1:]):
                await message.channel.send("If you're asking me? " + random.choice(replies))
                return

        elif any((x:=word) in msg_list for word in commands.keys()):
            answer_type = commands[f'{x}']
            to_add = message.content.replace(x, '').strip()
            if not (duplicate:=check_dupe(to_add)):
                update_answers(answer_type, to_add)
                await message.channel.send(f"{to_add} added as a {answer_type}")
            if duplicate:
                await message.channel.send(duplicate)
            return


d_client.run(os.getenv("TOKEN"))
