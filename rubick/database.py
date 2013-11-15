from bson.objectid import ObjectId
from copy import copy
import os
from pymongo import MongoClient
assert ObjectId
from recordtype import recordtype


def connect_to_db():
    mongo_url = os.environ.get("MONGODB_URI") or "mongodb://localhost/rubick"
    client = MongoClient(mongo_url)
    return client[mongo_url.split('/')[-1]]


def get_db():
    db = connect_to_db()
    return db


class Cluster(recordtype('Cluster',
                         [('id', str(ObjectId())), 'name', 'description',
                          'status', 'nodes', 'private_key', 'data'],
                         default=None)):
    @classmethod
    def from_doc(klass, doc):
        doc['id'] = str(doc['_id'])
        del doc['_id']
        return Cluster(**doc)

    def as_doc(self):
        doc = copy(self._asdict())
        doc['_id'] = ObjectId(doc['id'])
        del doc['id']
        return doc

    def for_json(self):
        return copy(self._asdict())


class RuleGroup:
    VALIDITY = 'validity'
    HA = 'high-availability'
    BEST_PRACTICES = 'best-practices'

    all = [VALIDITY, HA, BEST_PRACTICES]
