from dotenv import load_dotenv
import os
from pprint import pprint
import pymongo
import sys

load_dotenv()

sys.path.append(os.path.abspath("/home/gf/projects/discord_bot/data"))
from data import prompts, replies, one_liners, paras

# Mondo DB Connection
conn_str = os.getenv('MONDO_CONN')
m_client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
try:
    print(m_client.server_info())
except Exception:
    print("Unable to connect to the Mondo DB Server")

db = m_client.paras

result = db.paras.insert_many(paras.paras)

pprint(result.inserted_ids)
