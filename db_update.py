from dotenv import load_dotenv
import os
from pprint import pprint
import pymongo
import sys

from data import prompts, replies, one_liners, paras

#Load the local environment variables in .env
load_dotenv()

# These are the local "databases"
sys.path.append(os.path.abspath("/home/gf/projects/discord_bot/data"))


# Open Mondo DB Connection
conn_str = os.getenv('MONDO_CONN')
m_client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
try:
    print(m_client.server_info())
except Exception:
    print("Unable to connect to the Mondo DB Server")

db = m_client.prompts
result = db.questions.insert_many(prompts.prompts)
pprint(result.inserted_ids)
db = m_client.answers
result = db.replies.insert_many(replies.replies)
pprint(result.inserted_ids)
db = m_client.answers
result = db.one_liners.insert_many(one_liners.one_liners)
pprint(result.inserted_ids)
db = m_client.answers
result = db.paras.insert_many(paras.paras)
pprint(result.inserted_ids)

m_client.close()