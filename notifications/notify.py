from apns2.client import APNsClient, Notification
from apns2.payload import Payload

from config.config import Config

class Notify:
    def __init__(self, chat):
        self.config = Config()
        self.topic = 'BEPco.chatter'
        useSandbox = not self.config.isProd()
        self.client = APNsClient('certs/sandbox.pem', use_sandbox=useSandbox, use_alternative_port=False)
        self.chat = chat

    def sendMessages(self, users, message):
        custom = { 'chat_id': self.chat['_id'] }
        payload = Payload(alert=message, sound="default", badge=10, custom=custom)
        notifications = [Notification(token=user['apn_token'], payload=payload) for user in users]
        self.client.send_notification_batch(notifications, self.topic)
