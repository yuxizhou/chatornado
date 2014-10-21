__author__ = 'yuxizhou'

import tornado.websocket
import tornado.ioloop
import ujson
import time
from tornado.httpclient import HTTPClient

NAME = 'barney'
NUMB = 100

connect_count = -1

total = 0
tc = 0
this = last = int(time.time())


def connection_again():
    global connect_count
    connect_count += 1
    if connect_count < NUMB:
        c = HTTPClient()
        result = c.fetch('http://10.132.33.105:8777/node?user='+NAME+str(connect_count))
        node = result.body
        tornado.websocket.websocket_connect('ws://'+node+':8777/ws', tornado.ioloop.IOLoop.instance(), register)


def register(future):
    c = future.result()

    t = {
        'event': 1,
        'user': NAME+str(connect_count),
        'token': 'bbbbbbaaaaaa'
    }
    c.write_message(ujson.dumps(t))

    def print_message(m):
        if m.result():
            global this
            global last
            this = int(time.time())

            global total
            global tc
            total += 1
            tc += 1

            if this != last:
                print str(last) + ' ' + str(tc) + ' ' + str(total)
                tc = 0
                last = this

        c.read_message(print_message)
    c.read_message(print_message)

    connection_again()


# weixin1   10.161.163.144  115.29.170.94
# weixin2   10.161.163.37   115.29.171.57


connection_again()
tornado.ioloop.IOLoop.instance().start()