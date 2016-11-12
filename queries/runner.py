from datetime import datetime

from pymongo import MongoClient

from queries.inserts import inserts, indices
from queries.query3 import query3

client = MongoClient("localhost", 4321)
db = client.get_database('albertoriol')
col = db.get_collection('cbde')
col.delete_many({})
indices(col)
inserts(col)

print(list(query3(col, "", datetime.now(), datetime.now())))
