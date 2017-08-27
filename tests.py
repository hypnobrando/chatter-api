from sanic.response import json as json_response
from sanic import Blueprint

from notifications.notify import Notify

tests = Blueprint('tests')

@tests.route('/tests', methods=['POST'])
async def postChat(request):
    body = request.json
    message = body['message']
    token = body['apn_token']

    notify = Notify()
    notify.sendMessages([token], message, {})
    return json_response({ 'success': True })

@tests.route('/healthcheck', methods=['GET'])
async def getHealthcheck(request):
    return json_response({ 'success': True}, status=200)
