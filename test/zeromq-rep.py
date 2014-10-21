__author__ = 'yuxizhou'

import zmq
from zmq.eventloop.zmqstream import ZMQStream
from zmq.eventloop import ioloop
ioloop.install()


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5556")

stream = ZMQStream(socket)


def echo(msg):
    stream.send_multipart(msg)
stream.on_recv(echo)
ioloop.IOLoop.instance().start()