from pymongo import MongoClient
from datetime import datetime

client = MongoClient("localhost", 4321)
print(client.server_info())
