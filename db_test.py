from pymongo import MongoClient
from pprint import pprint
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv('MONDO_CONN'))
db=client.admin
serverStatusResult=db.command("serverStatus")
pprint(serverStatusResult)
