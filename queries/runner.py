from datetime import datetime, timedelta
from pymongo import MongoClient
from queries.inserts import inserts, indices
from queries.printer import printer
from queries.query1 import query1
from queries.query2 import query2
from queries.query3 import query3
from queries.query4 import query4

client = MongoClient("localhost", 4321)
db = client.get_database('albertoriol')
col = db.get_collection('cbde')
client.drop_database(db.name)
assert len(list(col.find({}))) == 0
indices(col)
inserts(col)

print()
print("QUERY 1 RESULT: ")
printer(list(query1(collection=col,
                    date=datetime.now() + timedelta(days=7))))
print()
print("QUERY 2 RESULT: ")
printer(list(query2(collection=col,
                    size=3,
                    part_type='type1',
                    region='REGION')))

print()
print("QUERY 3 RESULT: ")
printer(list(query3(collection=col,
                    market_segment='MARKET_SEGMENT',
                    order_date=datetime.now(),
                    ship_date=datetime.now())))
print()
print("QUERY 4 RESULT: ")
printer(list(query4(collection=col,
                    order_date=datetime.now() - timedelta(days=2),
                    region='REGION')))
