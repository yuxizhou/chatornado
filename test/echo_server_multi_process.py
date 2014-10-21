__author__ = 'yuxizhou'

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.process
import time
from multiprocessing import Process, Queue

from util import Stat

stat = Stat()


def task(input, output):
    while True:
        item = input.get()
        time.sleep(0.01)
        output.put(item)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class EchoWebSocket(tornado.websocket.WebSocketHandler):
    input_queue = Queue(2)
    output_queue = Queue()
    router = {}

    def open(self):
        EchoWebSocket.router['only'] = self

    def on_message(self, message):
        EchoWebSocket.input_queue.put(message)
        stat.fire('message')

    def on_close(self):
        del EchoWebSocket.router['only']

application = tornado.web.Application([
    (r"/", EchoWebSocket)
])

Process(target=task, args=(EchoWebSocket.input_queue, EchoWebSocket.output_queue)).start()
Process(target=task, args=(EchoWebSocket.input_queue, EchoWebSocket.output_queue)).start()


def result():
    stat.fire('result')
    try:
        while True:
            item = EchoWebSocket.output_queue.get_nowait()
            EchoWebSocket.router['only'].write_message(item)
            stat.fire('to user')
    except:
        pass
    finally:
        tornado.ioloop.IOLoop.instance().add_callback(result)

if __name__ == "__main__":
    # server = tornado.httpserver.HTTPServer(application)
    # server.bind(8080)
    # server.start(0)
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().add_callback(result)
    tornado.ioloop.IOLoop.instance().start()