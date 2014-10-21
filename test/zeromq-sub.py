__author__ = 'yuxizhou'

import zmq
from zmq.eventloop.zmqstream import ZMQStream
from zmq.eventloop import ioloop
ioloop.install()
import time

context = zmq.Context()

s = context.socket(zmq.SUB)
s.connect('tcp://localhost:5556')

stream = ZMQStream(s)
stream.setsockopt_unicode(zmq.SUBSCRIBE, u'10001')

global total
global tc
total = 0
tc = 0
this = last = int(time.time())


def echo(msg):
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
    # stream.send_multipart(msg)

stream.on_recv(echo)
ioloop.IOLoop.instance().start()

