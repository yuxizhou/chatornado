__author__ = 'yuxizhou'

import signal
import time
import functools
import random

import util
from hash_ring import HashRing

import redis
import tornado.web
import tornado.gen
import tornado.websocket
import tornado.httpserver
import ujson
from nsq import Writer, Reader, Error
import nsq


logger = util.get_logger(__name__, 'aeshna2.log')


def sig_handler(sig, frame):
    logger.info('Caught signal: %s', sig)
    tornado.ioloop.IOLoop.instance().add_callback(shutdown)


def shutdown():
    logger.info('clean redis')
    r = redis.StrictRedis(util.config['redis'])
    for name in Aeshna2WebSocket.connection_router:
        r.delete(name)

    logger.info('Stopping http server')
    http_server.stop()

    io_loop = tornado.ioloop.IOLoop.instance()

    deadline = time.time() + 3

    def stop_loop():
        now = time.time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now + 1, stop_loop)
        else:
            io_loop.stop()
            logger.info("Server stopped")
    stop_loop()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("QT Server is OK!")


class OnlineHandler(tornado.web.RequestHandler):
    def get(self):
        template = ''
        for i in Aeshna2WebSocket.connection_router.keys():
            template += i + '<br>'
        self.write(template)


class NodeHandler(tornado.web.RequestHandler):
    @property
    def ring(self):
        return self.application.ring

    def get(self):
        user = self.get_argument('user', None)
        if user:
            self.write(self.ring.get_node(user))
        else:
            self.send_error(400)


class Aeshna2WebSocket(tornado.websocket.WebSocketHandler):
    connection_router = {}

    @property
    def hostname(self):
        return self.application.hostname

    @property
    def redis(self):
        return self.application.redis

    @property
    def redis_group(self):
        return self.application.redis_group

    @property
    def nsq_writer(self):
        return self.application.nsq_writer

    @property
    def ring(self):
        return self.application.ring

    @property
    def node2hostname(self):
        return self.application.node2hostname

    @property
    def node2inner(self):
        return self.application.node2inner

    def open(self):
        self.me = None

    def on_message(self, message):
        try:
            m = ujson.loads(message)

            if m['event'] == 1:
                #register
                self.register(m)
            elif m['event'] == 2:
                #send message to peer
                self.send(m, message)
            elif m['event'] == 3:
                #send message to group
                self.send_group(m, message)
            else:
                logger.error("unknown event id [{}]".format(message))
        except Exception, e:
            logger.error(e)
            logger.error("ujson parse message fail [{}]".format(message))
        finally:
            stat.fire('websocket')

    def on_close(self):
        if self.me and self.me in Aeshna2WebSocket.connection_router:
            del Aeshna2WebSocket.connection_router[self.me]
            self.redis.delete(self.me)
            logger.debug("user offline [{}]".format(self.me))

    def register(self, m):
        if 'user' in m:
            self.me = m['user']
            Aeshna2WebSocket.connection_router[self.me] = self
            self.redis.set(self.me, self.hostname)
            logger.debug("user online [{}]".format(self.me))
        else:
            logger.error("register name is None")

    def send(self, m, message):
        if 'from' in m and 'to' in m and 'content' in m:
            self._send(m['to'], message)
        else:
            logger.error("message format error [{}]".format(message))

    def _send(self, who, message):
        if who in Aeshna2WebSocket.connection_router:
            Aeshna2WebSocket.connection_router[who].write_message(message)
            stat.fire('to user')
        else:
            # TODO critical performance problem to query redis every time
            # whereis = self.redis.get(who)

            target_ip = self.ring.get_node(who)
            whereis = self.node2hostname[target_ip]

            if whereis and whereis != self.hostname:
                # TODO whereis need to parse content again?
                def on_write_finish(conn, data, to_who, msg):
                    if isinstance(data, Error):
                        push_it(to_who, msg)
                        # logger.error("nsq deliver failed to [{}]".format(to_who))

                callback = functools.partial(on_write_finish, to_who=who, msg=message)
                logger.debug("write to nsq [{}]".format(message))
                # self.nsq_writer.pub(whereis, str(message), callback)
                self.nsq_writer.target_pub(self.node2inner[target_ip], whereis, str(message), callback)
            else:
                push_it(who, message)
                pass

    def send_group(self, m, message):
        if 'from' in m and 'to' in m and 'content' in m:
            m['__ts'] = time.time()
            group_members = self.redis_group.smembers(m['to'])
            if group_members:
                self.push_it(None, message)
                for member in group_members:
                    m['__to'] = member
                    self._send(member, ujson.dumps(m))
            else:
                logger.error("group id is not exists [{}]".format(message))


def push_it(to_who, content):
    stat.fire('push')
    push_writer.pub('pm', str(content))
    # print 'push {} {}'.format(to_who, content)


class TargetWriter(Writer):
    def target_pub(self, target, topic, msg, callback=None):
        self._target_pub(target+':4150', topic, msg, callback)

    def _target_pub(self, target, topic, msg, callback=None):
        command = 'pub'

        if not callback:
            callback = functools.partial(self._finish_pub, command=command,
                                         topic=topic, msg=msg)

        if not self.conns:
            callback(None, nsq.SendError('no connections'))
            return

        if target in self.conns:
            conn = self.conns[target]
        else:
            conn = random.choice(self.conns.values())
        conn.callback_queue.append(callback)
        cmd = getattr(nsq, command)
        try:
            conn.send(cmd(topic, msg))
        except Exception:
            logger.exception('[%s] failed to send %s' % (conn.id, command))
            conn.close()


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/node", NodeHandler),
            (r"/online", OnlineHandler),
            (r"/ws", Aeshna2WebSocket),
        ]

        settings = dict(
            debug=False
        )

        tornado.web.Application.__init__(self, handlers, **settings)

        self.hostname = util.config['hostname']
        self.redis = redis.StrictRedis(util.config['redis'])
        self.redis_group = redis.StrictRedis(util.config['redis'], db=1)
        self.nsq_writer = TargetWriter(util.config['nsqd'], 0.001)
        self.reader = Reader(message_handler=process_message,
                             # lookupd_http_addresses=util.config['nsqlookupd'],
                             nsqd_tcp_addresses=['10.161.163.37:4150'],
                             topic=self.hostname, channel='async', max_in_flight=250)

        # TODO assert every node in ring is also in node2hostname
        self.ring = HashRing(util.config['nodes'])
        self.node2hostname = util.config['node2hostname']
        self.node2inner = util.config['node2inner']


def process_message(message):
    try:
        c = ujson.loads(message.body)
        if c['event'] == 2:
            to = c['to']
        elif c['event'] == 3:
            to = c['__to']

        if to in Aeshna2WebSocket.connection_router:
            try:
                Aeshna2WebSocket.connection_router[to].write_message(message.body)
                stat.fire('to user')
            except tornado.websocket.WebSocketClosedError, err:
                push_it(to, message)
        else:
            push_it(to, message)
    except Exception, e:
        logger.error(e)
        logger.error("process_message ujson.loads fail [{}]".format(message.body))
    finally:
        message.finish()
        stat.fire('process message')


if __name__ == "__main__":
    global push_writer
    push_writer = Writer(util.config['nsqd'], 0.001)

    global stat
    stat = util.Stat()

    global http_server
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(util.config['port'])

    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGHUP, sig_handler)

    logger.info('aeshna2 service start')
    tornado.ioloop.IOLoop.instance().start()