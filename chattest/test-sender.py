__author__ = 'yuxizhou'

import tornado.websocket
import tornado.ioloop
import ujson
import time
from tornado.httpclient import HTTPClient
import sys

NAME = 'peter1'
if len(sys.argv) == 2:
    NAME = sys.argv[1]

TONAME = 'barney'
TONUM = 2

global total
global tc
total = 0
tc = 0
this = last = int(time.time())


def register(future):
    global c
    c = future.result()

    t = {
        'event': 1,
        'user': NAME,
        'token': 'bbbbbbaaaaaa'
    }
    c.write_message(ujson.dumps(t))

    send()


def send():
    t = {
        'event': 2,
        'from': NAME,
        'to': TONAME + str(total%TONUM),
        'content': ''
    }
    while True:
        t['to'] = TONAME + str(total%TONUM)
        t['content'] = 'hello wherkekjl   ' + str(tc)
        c.write_message(ujson.dumps(t))

        global this
        global last
        this = int(time.time())

        global tc
        global total
        tc += 1
        total += 1

        if this != last:
            print str(tc) + ' ' + str(total)
            tc = 0
            last = this

        if total == 100000:
            break



# weixin1   10.161.163.144  115.29.170.94
# weixin2   10.161.163.37   115.29.171.57

c = HTTPClient()
result = c.fetch('http://10.132.33.105:8777/node?user='+NAME)
node = result.body

tornado.websocket.websocket_connect('ws://'+node+':8777/ws', tornado.ioloop.IOLoop.instance(), register)


tornado.ioloop.IOLoop.instance().start()