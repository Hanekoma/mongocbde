from pymongo.collection import Collection


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
