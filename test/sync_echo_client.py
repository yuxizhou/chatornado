__author__ = 'yuxizhou'

import tornado.websocket
import tornado.ioloop
import time

c = None
total = 0
tc = 0
this = last = int(time.time())


def test(future):
    global c
    c = future.result()

    c.write_message('01helloworld')

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
        c.write_message('01helloworld')
        c.read_message(print_message)
    c.read_message(print_message)

tornado.websocket.websocket_connect('ws://127.0.0.1:8080/', tornado.ioloop.IOLoop.instance(), test)


tornado.ioloop.IOLoop.instance().start()