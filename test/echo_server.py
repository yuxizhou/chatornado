__author__ = 'yuxizhou'

import tornado.ioloop
import tornado.web
import tornado.websocket
import time
from util import Stat

stat = Stat()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class EchoWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        pass

    def on_message(self, message):
        stat.fire('message')
        time.sleep(0.01)
        self.write_message(message)

    def on_close(self):
        pass

application = tornado.web.Application([
    (r"/", EchoWebSocket)
])

def result():
    stat.fire('result')
    tornado.ioloop.IOLoop.instance().add_callback(result)

if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().add_callback(result)
    tornado.ioloop.IOLoop.instance().start()