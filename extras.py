from sanic.response import json as json_response
from sanic import Blueprint

from db.db import db
from auth.auth import Auth
from responses.response import Response
from notifications.notify import Notify
from users import baseURI as userBaseURI

extras = Blueprint('tests')

@extras.route('/tests', methods=['POST'])
async def postChat(request):
    body = request.json
    message = body['message']
    token = body['apn_token']

    try:
        notify = Notify()
        notify.sendMessages([token], message, {})
    except Exception as e:
        return json_response({ 'error' : str(e) }, status=500)

    return json_response({ 'success': True })

@extras.route('/healthcheck', methods=['GET'])
async def getHealthcheck(request):
    return json_response({ 'success': True}, status=200)

@extras.route(userBaseURI + '/<id>' + '/clear_notifications', methods=['POST'])
async def postChat(request, id):
    body = request.json

    user = db.findUserById(id)
    if user == None:
        return json_response({ 'error': Response.NotFoundError }, status=404)

    if not Auth.ValidateUser(user, request):
        return json_response({ 'error':  Response.InvalidUser }, status=400)

    try:
        notify = Notify()
        notify.clearNotifications(user['apn_token'])
    except Exception as e:
        return json_response({ 'error' : str(e) }, status=500)

    return json_response({ 'success': True })
