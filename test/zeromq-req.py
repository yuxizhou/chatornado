__author__ = 'yuxizhou'

import zmq
from zmq.eventloop.zmqstream import ZMQStream
from zmq.eventloop import ioloop
ioloop.install()

import time
global total
global tc
total = 0
tc = 0
this = last = int(time.time())


context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5556")
stream = ZMQStream(socket)


def echo(stream, msg):
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

stream.on_recv_stream(echo)


def send():
    stream.send(b"Hello")
    ioloop.IOLoop.instance().add_callback(send)

ioloop.IOLoop.instance().add_callback(send)
ioloop.IOLoop.instance().start()