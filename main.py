from sanic import Sanic
from users import users
from chats import chats

app = Sanic()
app.blueprint(users)
app.blueprint(chats)
app.run(host="0.0.0.0", port=8080)
