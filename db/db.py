import json
from pymongo import MongoClient
from bson import ObjectId

class DB:
    def __init__(self):
        self.db = MongoClient('mongodb://localhost:27017/')['chatter']

    def findUserById(self, id):
        return self.toDict(self.db['users'].find_one({ '_id': ObjectId(id) }))

    def insertUser(self, user):
        return self.toDict(self.db['users'].insert({ 'first_name': user['first_name'], 'last_name': user['last_name'] }))

    def toDict(self, object):
        return json.loads(JSONEncoder().encode(object))


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


db = DB()
