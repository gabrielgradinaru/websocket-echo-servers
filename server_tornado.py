import tornado.websoket
from tornado import gen

clients = set()


@gen.coroutine
def monitor():
    while True:
        yield gen.sleep(1)
        print(len(clients))


class WebSocketHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        if self not in clients:
            clients.add(self)

    def on_message(self, message):
        self.write_message(message)        
        
    def on_close(self):
        if self in clients:
            clients.remove(self)

app = tornado.web.Application([
    (r'/', WebSocketHandler),
])

if __name__ == '__main__':
    app.listen(8888, '0.0.0.0')
    tornado.ioloop.IOLoop.instance().add_callback(monitor)
    tornado.ioloop.IOLoop.instance().start()


#  gunicorn server_tornado:app -k tornado --workers=4 --bind=0.0.0.0:8888
