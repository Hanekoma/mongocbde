from datetime import datetime

import pymongo
from pymongo import MongoClient
from pymongo.database import Collection


def inserts(col: Collection):
    col


def indices(col: Collection):
    # query1

    # query2

    # query3
    col.create_index([('order.customer.mktsegment', pymongo.TEXT)], name='customer_mktsegment_index',
                     default_language='english')
    # query4
