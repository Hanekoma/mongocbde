from pymongo import MongoClient

client = MongoClient("localhost", 4321)
print(client.server_info())
