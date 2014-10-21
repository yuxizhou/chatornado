__author__ = 'yuxizhou'

import tornado.websocket
import tornado.ioloop
import ujson
import time
from tornado.httpclient import HTTPClient
import sys

NAME = 'barney'
if len(sys.argv) == 2:
    NAME = sys.argv[1]

total = 0
tc = 0
this = last = int(time.time())


def test(future):
    global c
    c = future.result()

    t = {
        'event': 1,
        'user': NAME,
        'token': 'aaaaaaabbbbbbbb'
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
                print str(tc) + ' ' + str(total)
                tc = 0
                last = this

        c.read_message(print_message)
    c.read_message(print_message)

# weixin1   10.161.163.144  115.29.170.94
# weixin2   10.161.163.37   115.29.171.57

c = HTTPClient()
result = c.fetch('http://10.161.163.144:8777/node?user='+NAME)
node = result.body

tornado.websocket.websocket_connect('ws://'+node+':8777/ws', tornado.ioloop.IOLoop.instance(), test)


tornado.ioloop.IOLoop.instance().start()