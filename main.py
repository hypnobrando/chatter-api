from sanic import Sanic
from users import users

app = Sanic()
app.blueprint(users)
app.run(host="0.0.0.0", port=8080)
