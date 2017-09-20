import aiohttp
from aiohttp import web
import asyncio


clients = set()

async def monitor():
    while True:
        await asyncio.sleep(3)
        print(len(clients))

async def websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)
    clients.add(ws)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if not msg.data or msg.type == aiohttp.WSMsgType.ERROR:
                await ws.close()
                clients.remove(ws)
            else:
                ws.send_str(msg.data)

    return ws

app = web.Application(debug=False)
app.router.add_get('/', websocket_handler)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(monitor())
    web.run_app(app, host='0.0.0.0', port=8888, loop=loop)

#  gunicorn server_aiohttp:app -k aiohttp.worker.GunicornWebWorker --workers=4 --bind=0.0.0.0:8888
