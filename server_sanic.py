from sanic import Sanic
import uvloop
import asyncio

app = Sanic(__name__)
clients = set()

async def monitor():
    while True:
        await asyncio.sleep(3)
        print(len(clients))

@app.websocket('/')
async def test(request, ws):
    while True:
        data = await ws.recv()
        await ws.send(data)
        if ws not in clients:
            clients.add(ws)


if __name__ == '__main__':
    server = app.create_server(
        host='0.0.0.0',
        port=8888,
        debug=False
    )
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    loop.create_task(monitor())
    asyncio.ensure_future(server)
    loop.run_forever()

#  gunicorn server_sanic:app -k sanic.worker.GunicornWorker --workers=4 --bind=0.0.0.0:8888
#  python3.5 -m sanic server_sanic.app --host=0.0.0.0 --port=8888 --workers=4




