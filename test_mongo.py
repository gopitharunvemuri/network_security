from pymongo import MongoClient
from dotenv import load_dotenv
import os
import certifi
ca = certifi.where()
load_dotenv()
url = os.getenv("MONGO_DB_URL")

client = MongoClient(url)
try:
    client.admin.command("ping")
    print("ping successfull")
except Exception as e:
    print(e)
