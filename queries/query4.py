from datetime import datetime, timedelta

from pymongo.database import Collection


def query4(collection: Collection, order_date: datetime, region: str):
    return collection.aggregate([
        {"$match": {
            "$and": [
                {"partsupp.supp.nation.region.name": {"$eq": region}},  # index optimized
                {"order.orderdate": {"$gte": order_date}},
                {"order.orderdate": {"$lt": order_date + timedelta(days=365)}}
            ]
        }},
        {"$project": {
            "n_name": "$partsupp.supp.nation.name",
            "l_extendedprice": "$extendedprice",
            "l_discount": "$discount"
        }},
        {"$group": {
            "_id": {"n_name": "$n_name"},
            "n_name": {"$first": "$n_name"},
            "revenue": {"$sum": {"$multiply": ["$l_extendedprice", {"$subtract": [1, "$l_discount"]}]}}
        }},
        {"$sort": {
            "revenue": -1
        }}
    ])
