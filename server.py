from sanic import Sanic
from sanic.response import json
import asyncio

queue = []
app = Sanic()

@app.route("/1")
async def root(request):
    print("request 1")
    await asyncio.sleep(3)
    return json({"hello" : "world"})

@app.route("/2")
async def root(request):
    print("request 2")
    await asyncio.sleep(3)
    return json({"hello" : "world"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
