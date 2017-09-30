from apns2.client import APNsClient, Notification
from apns2.payload import Payload

from config.config import Config

class Notify:
    def __init__(self):
        self.config = Config()
        self.topic = 'BEPco.chatter'
        useSandbox = not self.config.isProd()
        cert = 'certs/sandbox.pem' if useSandbox else 'certs/prod.pem'
        self.client = APNsClient(cert, use_sandbox=True, use_alternative_port=False)

    def sendMessages(self, apnTokens, message, custom):
        payload = Payload(alert=message, sound="default", custom=custom, content_available=1)
        notifications = [Notification(token=token, payload=payload) for token in apnTokens if token != None]
        self.client.send_notification_batch(notifications, self.topic)

    def clearNotifications(self, apnToken):
        payload = Payload(alert=None, badge=0, custom={ 'type': 'clear' })
        notifications = [Notification(token=apnToken, payload=payload)]
        self.client.send_notification_batch(notifications, self.topic)
