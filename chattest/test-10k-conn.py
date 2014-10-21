__author__ = 'yuxizhou'

import tornado.websocket
import tornado.ioloop
import ujson


connect_count = 0


def connection_again():
    global connect_count
    connect_count += 1
    if connect_count < 10000:
        tornado.websocket.websocket_connect('ws://10.161.163.144:8777/ws', tornado.ioloop.IOLoop.instance(), register)


def register(future):
    global c
    c = future.result()

    t = {
        'event': 1,
        'user': 'peter'+str(connect_count),
        'token': 'bbbbbbaaaaaa'
    }
    c.write_message(ujson.dumps(t))

    connection_again()


connection_again()
tornado.ioloop.IOLoop.instance().start()