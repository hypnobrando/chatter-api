from sanic import Sanic

from config.config import Config
from users import users
from chats import chats
from messages import messages
from tests import tests

config = Config()

app = Sanic()
app.blueprint(users)
app.blueprint(chats)
app.blueprint(messages)
app.blueprint(tests)

if __name__ == "__main__":
    print("Starting up chatter api in " + config.env + "...")
    app.run(host="0.0.0.0", port=8080)
