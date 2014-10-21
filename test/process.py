__author__ = 'yuxizhou'

import tornado.process
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.netutil
import time

a = []
total = 0
tc = 0
this = last = int(time.time())


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class EchoWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        a.append(self)
        print a

    def on_message(self, message):
        self.write_message(message)
        global this
        global last
        this = int(time.time())

        global total
        global tc
        total += 1
        tc += 1

        if this != last:
            print str(tornado.process.task_id()) + ' ' + str(tc) + ' ' + str(total)
            tc = 0
            last = this

    def on_close(self):
        a.remove(self)

application = tornado.web.Application([
    (r"/", EchoWebSocket)
])

if __name__ == "__main__":
    server = tornado.httpserver.HTTPServer(application)
    server.bind(8080)
    server.start(0)
    tornado.ioloop.IOLoop.instance().start()