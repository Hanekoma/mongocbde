from pymongo.collection import Collection


def query2(collection: Collection, size: int, part_type: str, region: str):
    return collection.aggregate([
        {"$match": {
            "$and": [
                {"partsupp.part.size": {"$eq": size}},  # index optimized
                {"partsupp.part.type": {"$eq": part_type}},
                {"order.customer.nation.region.name": {"$eq": region}},
                {"partsupp.supplycost": {"$eq": get_min(query2_aux(collection=collection,
                                                                   region=region))}}
            ]
        }},
        {"$project": {
            "s_acctbal": "$partsupp.supp.acctbal",
            "s_name": "$partsupp.supp.name",
            "n_name": "$order.customer.nation.name",
            "p_partkey": "$partsupp.part.key",
            "p_mfgr": "$partsupp.part.mfgr",
            "s_address": "$partsupp.supp.address",
            "s_phone": "$partsupp.supp.phone",
            "s_comment": "$partsupp.supp.comment",
            "s_suppkey": "$partsupp.supp.key",
            "l_orderkey": "$order.key"
        }},
        {"$group": {
            "_id": {"l_orderkey": "$l_orderkey", "p_partkey": "$p_partkey", "s_suppkey": "$s_suppkey"},
            "s_acctbal": {"$first": "$s_acctbal"},
            "s_name": {"$first": "$s_name"},
            "n_name": {"$first": "$n_name"},
            "p_partkey": {"$first": "$p_partkey"},
            "p_mfgr": {"$first": "$p_mfgr"},
            "s_address": {"$first": "$s_address"},
            "s_phone": {"$first": "$s_phone"},
            "s_comment": {"$first": "$s_comment"}
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
            "order.customer.nation.region.name": {"$eq": region}  # index optimized
        }},
        {"$project": {
            "ps_supplycost": "$partsupp.supplycost",
            "l_orderkey": "$order.key",
            "p_partkey": "$partsupp.part.key",
            "s_suppkey": "$partsupp.supp.key"
        }},
        {"$group": {
            "_id": {},
            "min_supplycost": {"$min": "$ps_supplycost"}
        }}
    ])


def get_min(res):
    for item in res:
        return item.get('min_supplycost')
