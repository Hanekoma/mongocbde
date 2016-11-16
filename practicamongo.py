from pymongo import MongoClient
from pymongo.database import Collection
from datetime import datetime, timedelta


def inserts(col: Collection):
    """
    Inserts all test documents.
    Please note that they have nested objects. While we know that it slightly impacts performance,
    we'd rather have a readable object for these exercises instead of one hard-to-read super document.
    :param col: The collection where documents will be inserted.
    """
    col.drop()
    doc1 = __base_document(1, 1, 1,
                           part_type='type1')
    doc2 = __base_document(1, 1, 2,
                           part_type='type1')
    doc3 = __base_document(2, 1, 1,
                           part_type='different_type',
                           nation_name='NATION2')
    doc4 = __base_document(3, 1, 1,
                           customer_market_segment='random',
                           region_name='random',
                           nation_name='random')

    docs = [doc1, doc2, doc3, doc4]
    print("INSERTING THE FOLLOWING DOCUMENTS:")
    for doc in docs:
        print(doc)

    col.insert_many(documents=docs)
    assert len(list(col.find({}))) == len(docs)


def indices(col: Collection):
    # query1
    col.create_index('shipdate', name='lineitem_shipdate_index',
                     default_language='english')

    # query2 & query4
    col.create_index('partsupp.supp.nation.region.name', name='supplier_region_index',
                     default_language='english')

    # query3
    col.create_index('order.customer.mktsegment', name='customer_mktsegment_index',
                     default_language='english')


def __base_document(orderkey: int,
                    partkey: int,
                    suppkey: int,
                    customer_market_segment: str = 'MARKET_SEGMENT',
                    region_name: str = 'REGION',
                    nation_name: str = 'NATION',
                    part_type='SADFA'):
    yesterday = datetime.now() - timedelta(days=1)
    tomorrow = datetime.now() + timedelta(days=1)
    return {
        "_id": "{}_{}_{}".format(orderkey, partkey, suppkey),
        "linenumber": 1,
        "quantity": 1,
        "extendedprice": 100,
        "discount": 0.30,
        "tax": 1,
        "returnflag": "T",
        "linestatus": "T",
        "shipdate": tomorrow,
        "commitdate": yesterday,
        "receiptdate": yesterday,
        "shipinstruct": "whatever",
        "shipmode": "whatever",
        "comment": "whatever",
        "order": {
            "key": orderkey,
            "status": "A",
            "totalprice": 1,
            "orderdate": yesterday,
            "orderpriority": "ASDFAS",
            "clerk": "asdfasdf",
            "shippriority": 1,
            "comment": "ASFDASD",
            "customer": {
                "name": "Pepe",
                "address": "SADDF",
                "nation": {
                    "key": 1,
                    "name": nation_name,
                    "comment": "SADDFASDF",
                    "region": {
                        "key": 1,
                        "name": region_name,
                        "comment": "SADFSAF"
                    }
                },
                "phone": "safdsdfsafd",
                "acctbal": 1,
                "mktsegment": customer_market_segment,
                "comment": "SADFSAD"
            }
        },
        "partsupp": {
            "availqty": 1,
            "supplycost": 1,
            "comment": "SADFSAFD",
            "part": {
                "key": partkey,
                "name": "ADSF",
                "mfgr": "ASDF",
                "brand": "SADFA",
                "type": part_type,
                "size": 3,
                "container": "SADFAS",
                "retailprice": 3,
                "comment": "SADDFASDF"
            },
            "supp": {
                "key": suppkey,
                "name": "SADFA",
                "address": "ASDFSADF",
                "nation": {
                    "key": 1,
                    "name": nation_name,
                    "region": {
                        "key": 1,
                        "name": region_name,
                        "comment": "SADFDASDF"
                    },
                    "comment": "SADFAS"
                },
                "phone": "123891923",
                "acctbal": 3,
                "comment": "DSAAFSA"
            }
        }
    }


def printer(res):
    for item in res:
        print(item)


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


def query2(collection: Collection, size: int, part_type: str, region: str):
    return collection.aggregate([
        {"$match": {
            "$and": [
                {"partsupp.part.size": {"$eq": size}},
                {"partsupp.part.type": {"$eq": part_type}},
                {"partsupp.supp.nation.region.name": {"$eq": region}},
                {"partsupp.supplycost": {"$eq": get_min(query2_aux(collection=collection,
                                                                   region=region))}}
            ]
        }},
        {"$project": {
            "s_acctbal": "$partsupp.supp.acctbal",
            "s_name": "$partsupp.supp.name",
            "n_name": "$partsupp.supp.nation.name",
            "p_partkey": "$partsupp.part.key",
            "p_mfgr": "$partsupp.part.mfgr",
            "s_address": "$partsupp.supp.address",
            "s_phone": "$partsupp.supp.phone",
            "s_comment": "$partsupp.supp.comment"
        }},
        {"$sort": {
            "s_acctbal": -1,
            "n_name": 1,
            "s_name": 1,
            "p_partkey": 1
        }}
    ])


def query2_aux(collection: Collection, region: str):
    return collection.aggregate([
        {"$match": {
            "partsupp.supp.nation.region.name": {"$eq": region}
        }},
        {"$project": {
            "ps_supplycost": "$partsupp.supplycost"
        }},
        {"$group": {
            "_id": {},
            "min_supplycost": {"$min": "$ps_supplycost"}
        }}
    ])


def get_min(res):
    for item in res:
        return item.get('min_supplycost')


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
            "l_orderkey": {"$first": "$l_orderkey"},  # only one key per group
            "revenue": {"$sum": {"$multiply": ["$l_extendedprice", {"$subtract": [1, "$l_discount"]}]}},
            "o_orderdate": {"$first": "$o_orderdate"},  # only one orderdate per group (one order)
            "o_shippriority": {"$first": "$o_shippriority"}  # only one shippriority per group (one order)
        }},
        {"$sort": {
            "revenue": -1,
            "o_orderdate": 1
        }}
    ])


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


def main():
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


if __name__ == '__main__':
    main()
