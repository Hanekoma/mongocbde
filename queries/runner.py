from datetime import datetime

from pymongo import MongoClient

from queries.inserts import inserts, indices
from queries.query3 import query3

client = MongoClient("localhost", 4321)
db = client.get_database('albertoriol')
col = db.get_collection('cbde')
col.delete_many({})
assert len(list(col.find({}))) == 0
indices(col)
inserts(col)

print("QUERY 3 RESULT: ")
print(list(query3(col, 'MARKET_SEGMENT', datetime.now(), datetime.now())))
