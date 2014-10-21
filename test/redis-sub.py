__author__ = 'yuxizhou'


import tornadoredis
import tornado
import tornadoredis.pubsub


class TestHandler(tornadoredis.pubsub.BaseSubscriber):
    def on_message(self, msg):
        if not msg:
            return
        if msg.kind == 'message' and msg.body:
            subscribers = list(self.subscribers[msg.channel].keys())
            if subscribers:
                for subscriber in subscribers:
                    subscriber.on_message(str(msg.body))


class R(object):
    def on_message(self, msg):
        print msg

subscriber = TestHandler(tornadoredis.Client())
subscriber.subscribe('test_channel', R())

tornado.ioloop.IOLoop.instance().start()