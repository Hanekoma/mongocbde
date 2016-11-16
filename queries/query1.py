from datetime import datetime
from pymongo.collection import Collection


def query1(collection: Collection, date: datetime):
    return collection.aggregate([
        {"$match": {
            "shipdate": {"$lte": date}
        }},
        {"$project": {
            "l_returnflag": "$returnflag",
            "l_linestatus": "$linestatus",
            "l_quantity": "$quantity",
            "l_extendedprice": "$extendedprice",
            "l_discount": "$discount",
            "l_tax": "$tax"
        }},
        {"$group": {
            "_id": {"l_returnflag": "$l_returnflag", "l_linestatus": "$l_linestatus"},
            "l_returnflag": {"$first": "$l_returnflag"},
            "l_linestatus": {"$first": "$l_linestatus"},
            "sum_qty": {"$sum": "$l_quantity"},
            "sum_base_price": {"$sum": "$l_extendedprice"},
            "sum_disc_price": {"$sum": {"$multiply": ["$l_extendedprice", {"$subtract": [1, "$l_discount"]}]}},
            "sum_charge": {"$sum": {
                "$multiply": [{"$multiply": ["$l_extendedprice", {"$subtract": [1, "$l_discount"]}]},
                              {"$add": [1, "$l_tax"]}]}},
            "avg_qty": {"$avg": "$l_quantity"},
            "avg_price": {"$avg": "$l_extendedprice"},
            "avg_disc": {"$avg": "$l_discount"},
            "count_order": {"$sum": 1}
        }},
        {"$sort": {
            "returnflag": 1,
            "linestatus": 1
        }}
    ])
