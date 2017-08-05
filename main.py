from sanic import Sanic
from users import users
from chats import chats
from messages import messages
from config.config import Config

config = Config()

app = Sanic()
app.blueprint(users)
app.blueprint(chats)
app.blueprint(messages)

if __name__ == "__main__":
    print("Starting up chatter api in " + config.env + "...")
    app.run(host="0.0.0.0", port=8080)
