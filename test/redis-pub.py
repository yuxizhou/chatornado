__author__ = 'yuxizhou'

import tornadoredis
import tornado
import datetime

c = tornadoredis.Client()
c.connect()


def cb():
    c.publish('test_channel', str(datetime.datetime.now()))
    tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=1), cb)


tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=1), cb)

tornado.ioloop.IOLoop.instance().start()