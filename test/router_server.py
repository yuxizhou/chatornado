__author__ = 'yuxizhou'

import tornado.ioloop
import tornado.web
import tornado.websocket


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class EchoWebSocket(tornado.websocket.WebSocketHandler):
    last = None

    def open(self):
        if not EchoWebSocket.last:
            EchoWebSocket.last = self

    def on_message(self, message):
        if EchoWebSocket.last:
            EchoWebSocket.last.write_message(message)

    def on_close(self):
        pass

application = tornado.web.Application([
    (r"/", EchoWebSocket)
])

if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()