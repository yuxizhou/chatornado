__author__ = 'yuxizhou'

import nsq
import tornado.ioloop
import time
import datetime

sent = 0
total = 100000


def pub_10000():
    print "start send "+str(time.time())
    send = 0
    while send != total:
        send += 1
        pub_message()
    print "finish send "+str(time.time())


def pub_message():
    writer.pub('nsq_reader3', "pub2"+time.strftime('%H:%M:%S'), finish_pub)


def finish_pub(conn, data):
    if data == 'OK':
        global sent
        sent += 1

        if sent == total:
            print "finish sent "+str(time.time())
    else:
        print data

# weixin1   10.161.163.144  115.29.170.94
# weixin2   10.161.163.37   115.29.171.57
writer = nsq.Writer(['115.29.171.57:4150', '115.29.170.94:4150'],)
tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=1), pub_10000)
nsq.run()

