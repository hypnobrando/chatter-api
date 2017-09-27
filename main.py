from sanic import Sanic

from config.config import Config
from users import users
from chats import chats
from messages import messages
from extras import extras

config = Config()

app = Sanic()
app.blueprint(users)
app.blueprint(chats)
app.blueprint(messages)
app.blueprint(extras)

if __name__ == "__main__":
    print("Starting up chatter api in " + config.env + "...")
    app.run(host="0.0.0.0", port=8080)
