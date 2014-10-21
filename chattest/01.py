__author__ = 'yuxizhou'

import tornado.websocket
import tornado.ioloop
import ujson


def test(future):
    global c
    c = future.result()

    t = {
        'event': 1,
        'user': 'amy',
        'token': 'aaaaaaabbbbbbbb'
    }
    c.write_message(ujson.dumps(t))

    def print_message(m):
        print m.result()
        c.read_message(print_message)
    c.read_message(print_message)

# weixin1   10.161.163.144  115.29.170.94
# weixin2   10.161.163.37   115.29.171.57
tornado.websocket.websocket_connect('ws://127.0.0.1:8777/ws', tornado.ioloop.IOLoop.instance(), test)


tornado.ioloop.IOLoop.instance().start()