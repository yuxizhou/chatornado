__author__ = 'yuxizhou'

import tornado.websocket
import tornado.ioloop
import datetime

c = None


def cb():
    c.write_message('22222 hello')

    def print_message(m):
        print m.result()
        tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=1), cb)
    c.read_message(print_message)


def on_connection(future):
    global c
    c = future.result()
    tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=1), cb)


connect_count = 0


def continue_connect(future):
    global connect_count
    connect_count += 1
    if connect_count < 10240:
        tornado.websocket.websocket_connect('ws://127.0.0.1:8888/ws', tornado.ioloop.IOLoop.instance(), continue_connect)


def test(future):
    global c
    c = future.result()

    c.write_message('01helloworld')

tornado.websocket.websocket_connect('ws://127.0.0.1:8888/ws', tornado.ioloop.IOLoop.instance(), test)


tornado.ioloop.IOLoop.instance().start()