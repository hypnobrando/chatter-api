import asyncio
from sanic.response import json as json_response
from sanic import Blueprint

from db.db import db
from responses.response import Response
from auth.auth import Auth

users = Blueprint('users')
baseURI = '/' + users.name

#
# POST - /users
# {
#   first_name: string,
#   last_name: string,
#   apn_token: string
# }
#
@users.route(baseURI, methods=['POST'])
async def postUser(request):
    body = request.json

    if 'first_name' not in body and 'last_name' not in body and 'apn_token' not in body:
        return json_response({ 'error': Response.BadRequest }, status=400)

    body['session_token'] = Auth.GenerateSessionToken()
    user_id = db.insertUser(body)
    user = db.findUserById(user_id)

    return json_response({ 'user': user }, status=201)

#
# GET - /users/:id
#
@users.route(baseURI + '/<id>', methods=['GET'])
async def getUser(request, id):
    user = db.findUserById(id)
    if user == None:
        return json_response({ 'error': Response.NotFoundError }, status=404)

    if not Auth.ValidateUser(user, request):
        return json_response({ 'error':  Response.InvalidUser }, status=400)

    newSessionToken = Auth.GenerateSessionToken()
    db.updateUserSessionToken(id, newSessionToken)
    user = db.findUserById(id)

    return json_response({ 'user': user }, status=200)

#
# DELETE - /users/:id
#
@users.route(baseURI + '/<id>', methods=['DELETE'])
async def deleteUser(request, id):
    user = db.findUserById(id)
    if user == None:
        return json_response({ 'error': Response.NotFoundError }, status=404)

    if not Auth.ValidateUser(user, request):
        return json_response({ 'error':  Response.InvalidUser }, status=400)

    db.removeUserById(id)
    return json_response({ 'success': True }, status=201)

#
# PATCH - /users/:id
# {
#   first_name: string,
#   last_name: string
# }
#
@users.route(baseURI + '/<id>', methods=['PATCH'])
async def patchUser(request, id):
    user = db.findUserById(id)
    if user == None:
        return json_response({ 'error': Response.NotFoundError }, status=404)

    if not Auth.ValidateUser(user, request):
        return json_response({ 'error':  Response.InvalidUser }, status=400)

    body = request.json
    if 'first_name' not in body and 'last_name' not in body:
        return json_response({ 'error': Response.BadRequest }, status=400)

    db.updateUserById(id, body['first_name'], body['last_name'])
    user = db.findUserById(id)
    return json_response({ 'user': user }, status=201)
