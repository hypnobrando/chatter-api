import asyncio
from sanic.response import json as json_response
from sanic import Blueprint
from bson import ObjectId

from db.db import db
from responses.response import Response
from users import baseURI as userBaseURI
from chats import baseURI as chatBaseURI

messages = Blueprint('messages')
baseURI = '/' + messages.name

#
# POST -/users/:user_id/chats/:chat_id/messages
# {
#   message: string
# }
#
@messages.route(userBaseURI + '/<user_id>' + chatBaseURI + '/<chat_id>' + baseURI, methods=['POST'])
async def postChat(request, user_id, chat_id):
    user = db.findUserById(user_id)
    chat = db.findChatById(chat_id)

    if user == None or chat == None:
        return json_response({ 'error': Response.NotFoundError })

    body = request.json

    if 'message' not in body:
        return json_response({ 'error': Response.BadRequest }, status=400)

    db.insertMessage(user_id, chat_id, body['message'])
    messages = db.findMessagesByChatId(chat_id)
    chat = db.findChatById(chat_id)
    users = db.findUsersByIds(chat['user_ids'])

    return json_response({ 'messages': messages, 'chat': chat, 'users': users }, status=201)

#
# GET -/chats/:chat_id/messages
#
@messages.route(chatBaseURI + '/<chat_id>/messages', methods=['GET'])
async def getChatMessages(request, chat_id):
    chat = db.findChatById(chat_id)

    if chat == None:
        return json_response({ 'error': Response.NotFoundError })

    messages = db.findMessagesByChatId(chat_id)
    chat = db.findChatById(chat_id)
    users = db.findUsersByIds(chat['user_ids'])

    return json_response({ 'messages': messages, 'chat': chat, 'users': users }, status=201)
