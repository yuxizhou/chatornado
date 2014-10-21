__author__ = 'yuxizhou'

import tornado.websocket
import tornado.ioloop
import ujson
import time


def register(future):
    global c
    c = future.result()

    t = {
        'event': 1,
        'user': 'peter',
        'token': 'bbbbbbaaaaaa'
    }
    c.write_message(ujson.dumps(t))

    send()


def send():
    t = {
        'event': 2,
        'from': 'peter',
        'to': 'amy',
        'content': 'hello there',
        'id': '123123123',
        'timestamp': '123123123'
    }
    while True:
        c.write_message(ujson.dumps(t))
        time.sleep(0.1)
    # def print_message(m):
    #     print m.result()
    # c.read_message(print_message)

# weixin1   10.161.163.144  115.29.170.94
# weixin2   10.161.163.37   115.29.171.57
tornado.websocket.websocket_connect('ws://127.0.0.1:8777/ws', tornado.ioloop.IOLoop.instance(), register)


tornado.ioloop.IOLoop.instance().start()