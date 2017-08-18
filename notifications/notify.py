from apns2.client import APNsClient, Notification
from apns2.payload import Payload

from config.config import Config

class Notify:
    def __init__(self):
        self.config = Config()
        self.topic = 'BEPco.chatter'
        useSandbox = not self.config.isProd()
        self.client = APNsClient('certs/sandbox.pem', use_sandbox=useSandbox, use_alternative_port=False)

    def sendMessages(self, apnTokens, message, custom):
        payload = Payload(alert=message, sound="default", custom=custom, content_available=1)
        notifications = [Notification(token=token, payload=payload) for token in apnTokens if token != None]
        self.client.send_notification_batch(notifications, self.topic)
