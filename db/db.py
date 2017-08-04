import json
import datetime
from pymongo import MongoClient
from bson import ObjectId

class DB:
    def __init__(self):
        self.db = MongoClient('mongodb://localhost:27017/')['chatter']

    # Users

    def findUserById(self, id):
        return self.deserialize(self.db['users'].find_one({ '_id': ObjectId(id) }))

    def insertUser(self, user):
        return self.deserialize(self.db['users'].insert({ 'first_name': user['first_name'], 'last_name': user['last_name'] }))

    def findUsersByIds(self, user_ids):
        return self.deserialize(list(self.db['users'].find({ '_id': { '$in': [ObjectId(user_id) for user_id in user_ids] } })))

    # Chats

    def findChatById(self, id):
        return self.deserialize(self.db['chats'].find_one({ '_id': ObjectId(id) }))

    def insertChat(self, chat):
        mongo_user_ids = [ObjectId(user_id) for user_id in chat['user_ids']]
        return self.deserialize(self.db['chats'].insert({ 'user_ids':  mongo_user_ids }))

    def findChatsByUserId(self, user_id):
        return self.deserialize(list(self.db['chats'].find({ 'user_ids': { '$elemMatch': { '$eq': ObjectId(user_id) } } })))

    # messages

    def insertMessage(self, user_id, chat_id, message):
        return self.deserialize(self.db['messages'].insert({ 'user_id': ObjectId(user_id), 'chat_id': ObjectId(chat_id), 'message': message, 'timestamp': datetime.datetime.utcnow() }))

    def findMessagesByChatId(self, chat_id):
        return self.deserialize(list(self.db['messages'].find({ 'chat_id': { '$eq': ObjectId(chat_id) } })))

    # Helpers

    def deserialize(self, object):
        return json.loads(JSONEncoder().encode(object))


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, (datetime.datetime, datetime.date)):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


db = DB()
