import pymongo
from pymongo.database import Collection
from datetime import datetime, timedelta


def inserts(col: Collection):
    """
    Inserts all test documents.
    Please note that they have nested objects. While we know that it slightly impacts performance,
    we'd rather have a readable object for these exercises instead of one hard-to-read super document. 
    :param col: The collection where documents will be inserted.
    """
    doc1 = __base_document(1, 1, 1)
    doc2 = __base_document(1, 1, 2)
    doc3 = __base_document(2, 1, 1)
    doc4 = __base_document(3, 1, 1, customer_market_segment='randomnotmatching')
    docs = [doc1, doc2, doc3, doc4]
    print("INSERTING THE FOLLOWING DOCUMENTS:")
    for doc in docs:
        print(doc)
    col.insert_many(documents=docs)
    assert len(list(col.find({}))) == len(docs)


def indices(col: Collection):
    # query1

    # query2

    # query3
    col.create_index([('order.customer.mktsegment', pymongo.TEXT)], name='customer_mktsegment_index',
                     default_language='english')
    # query4


def __base_document(orderkey: int, partkey: int, suppkey: int, customer_market_segment: str = 'MARKET_SEGMENT'):
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
                    "name": "ASDFA",
                    "comment": "SADDFASDF",
                    "region": {
                        "key": 1,
                        "name": "SADFSAD",
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
                "type": "SADFA",
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
                    "name": "ADSFSA",
                    "region": {
                        "key": 1,
                        "name": "ASDFSAD",
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
