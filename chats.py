import asyncio
from sanic.response import json as json_response
from sanic import Blueprint
from bson import ObjectId

from db.db import db
from responses.response import Response
from users import baseURI as userBaseURI
from notifications.notify import Notify

chats = Blueprint('chats')
baseURI = '/' + chats.name

#
# POST - /chats
# {
#   user_ids: [string]
# }
#
@chats.route(baseURI, methods=['POST'])
async def postChat(request):
    body = request.json

    if 'user_ids' not in body:
        return json_response({ 'error': Response.BadRequest }, status=400)

    chat_id = db.insertChat(body)
    return json_response({ 'chat': db.findChatById(chat_id) }, status=201)

#
# GET - /users/:id/chats
#
@chats.route(userBaseURI + '/<id>' + baseURI, methods=['GET'])
async def getUserChats(request, id):
    user = db.findUserById(id)
    if user == None:
        return json_response({ 'error': Response.NotFoundError })

    chats = db.findChatsByUserId(id)
    if 'removed_chat_ids' in user:
        chats = [chat for chat in chats if chat['_id'] not in user['removed_chat_ids']]

    for chat in chats:
        chat['users'] = db.findUsersByIds(chat['user_ids'])

    return json_response({ 'chats' : chats })

#
# PATCH - /users/:id/chats/:chat_id
# {
#   title: string
# }
@chats.route(userBaseURI + '/<id>' + baseURI + '/<chat_id>', methods=['PATCH'])
async def patchChat(request, id, chat_id):
    user = db.findUserById(id)
    if user == None:
        return json_response({ 'error': Response.NotFoundError })

    chat = db.findChatById(chat_id)
    if chat == None:
        return json_response({ 'error': Response.NotFoundError })

    body = request.json

    if 'title' not in body:
        return json_response({ 'error': Response.BadRequest }, status=400)

    db.updateChat(chat_id, body['title'])

    return json_response({ 'success' : 'chat updated' })

#
# PATCH - /users/:id/chats/:chat_id/add_users
# {
#   user_ids: [string]
# }
@chats.route(userBaseURI + '/<id>' + baseURI + '/<chat_id>/add_users', methods=['PATCH'])
async def patchChat(request, id, chat_id):
    user = db.findUserById(id)
    if user == None:
        return json_response({ 'error': Response.NotFoundError })

    chat = db.findChatById(chat_id)
    if chat == None:
        return json_response({ 'error': Response.NotFoundError })

    body = request.json

    if 'user_ids' not in body:
        return json_response({ 'error': Response.BadRequest }, status=400)

    notify = Notify()
    users = db.findUsersByIds(chat['user_ids'])
    apnTokens = [otherUser['apn_token'] for otherUser in users if otherUser['_id'] != user['_id']]
    custom = { 'chat_id' : chat['_id'], 'type' : 'users_added' }
    notify.sendMessages(apnTokens, user['first_name'] + ' ' + user['last_name'] + ' added more people to one of your chats.', custom)

    db.addUsersToChat(chat_id, body['user_ids'])
    chat = db.findChatById(chat_id)
    chat['users'] = db.findUsersByIds(chat['user_ids'])

    return json_response({ 'chat' : chat })


#
# DELETE - /users/:id/chats/:chat_id
#
@chats.route(userBaseURI + '/<id>' + baseURI + '/<chat_id>', methods=['DELETE'])
async def deleteChat(request, id, chat_id):
    user = db.findUserById(id)
    if user == None:
        return json_response({ 'error': Response.NotFoundError })

    chat = db.findChatById(chat_id)
    if chat == None:
        return json_response({ 'error': Response.NotFoundError })

    db.removeUserFromChat(id, chat_id)

    return json_response({ 'success' : 'user removed from chat' })
