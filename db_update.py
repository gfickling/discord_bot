'''Update Mondo Database with bot commands and replies'''

import os
import sys
from pprint import pprint
from dotenv import load_dotenv
import pymongo


from data import prompts, replies, one_liners, paras

# Load the local environment variables in .env
load_dotenv()

# These are the local "databases"
sys.path.append(os.path.abspath(
    "/Users/graemefickling/projects/discord_bot/data"))

# Open Mondo DB Connection
conn_str = os.getenv('MONDO_CONN')
m_client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
try:
    print(m_client.server_info())
except Exception as e:
    print("Unable to connect to the Mondo DB Server")
    print(e)


def add_records():
    db = m_client.prompts
    result = db.questions.insert_many(prompts.prompts)
    pprint(result.inserted_ids)
    db = m_client.answers
    result = db.answers.insert_many(replies.replies)
    pprint(result.inserted_ids)
    result = db.answers.insert_many(one_liners.one_liners)
    pprint(result.inserted_ids)
    result = db.answers.insert_many(paras.paras)
    pprint(result.inserted_ids)


answer_types = ['reply', 'one_liner', 'para']


def add_ans_lower():
    db = m_client.answers
    for answer_type in answer_types:
        for doc in db.answers.find():
            try:
                val = doc[answer_type].lower()
                doc_id = doc['_id']
                db.answers.find_one_and_update(
                    {'_id': doc_id}, {'$set': {'ans_lower': val}})
            except Exception as e:
                print(e)
                pass


# add_records()
# add_ans_lower()

m_client.close()
