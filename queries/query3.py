from datetime import datetime

from pymongo.database import Collection


def query3(collection: Collection, market_segment: str, order_date: datetime, ship_date: datetime):
    return collection.aggregate([
        # c_mktsegment is the most selective, given there are 150k customer vs 6M line_item & 1.5M orders
        {"$match": {
            "$and": [
                {"order.customer.mktsegment": {"$eq": market_segment}},  # index optimized
                {"order.orderdate": {"$lt": order_date}},
                {"shipdate": {"$gt": ship_date}}
            ]
        }},
        {"$project": {
            "l_orderkey": "$order.key",
            "l_extendedprice": "$extendedprice",
            "l_discount": "$discount",
            "o_orderdate": "$order.orderdate",
            "o_shippriority": "$order.shippriority"
        }},
        {"$group": {
            "_id": {"l_orderkey": "$l_orderkey", "o_orderdate": "$o_orderdate", "o_shippriority": "$o_shippriority"},
            "l_orderkey": {"$first": "$l_orderkey"}, # only one key per group
            "revenue": {"$sum": {"$multiply": ["$l_extendedprice", {"$subtract": [1, "$l_discount"]}]}},
            "o_orderdate": {"$first": "$o_orderdate"}, # only one orderdate per group (one order)
            "o_shippriority": {"$first": "$o_shippriority"} # only one shippriority per group (one order)
        }},
        {"$sort": {
            "revenue": -1,
            "o_orderdate": 1
        }}
    ])
