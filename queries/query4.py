from datetime import datetime
from pymongo import MongoClient
from pymongo.database import Collection

client = MongoClient("localhost", 4321)


def query4(collection: Collection, order_date: datetime, region: str):
    pass
