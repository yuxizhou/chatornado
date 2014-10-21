__author__ = 'yuxizhou'

import nsq
import time

this = last = int(time.time())
recv = 0


def process_message(message):
    global recv
    global this
    global last

    this = int(time.time())

    recv += 1

    if this != last:
        print str(recv)
        recv = 0
        last = this

    message.finish()

# weixin1   10.161.163.144  115.29.170.94
# weixin2   10.161.163.37   115.29.171.57
r = nsq.Reader(message_handler=process_message,
               # lookupd_http_addresses=['http://115.29.170.94:4161'],
               nsqd_tcp_addresses=['10.161.163.144:4150', '10.161.163.37:4150'],
               topic='nsq_reader3', channel='async', max_in_flight=100)
nsq.run()