from sanic import Sanic
from users import users
from chats import chats
from messages import messages

app = Sanic()
app.blueprint(users)
app.blueprint(chats)
app.blueprint(messages)
app.run(host="0.0.0.0", port=8080)
