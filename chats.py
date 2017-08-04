import asyncio
from sanic.response import json as json_response
from sanic import Blueprint
from bson import ObjectId

from db.db import db
from responses.response import Response
from users import baseURI as userBaseURI

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
    for chat in chats:
        chat['users'] = db.findUsersByIds(chat['user_ids'])
        
    return json_response({ 'chats' : chats })
