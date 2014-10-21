import asyncore
import asynchat
import socket
import ujson
from util import Stat

stat = Stat()


class http_request_handler(asynchat.async_chat):

    def __init__(self, sock, addr, sessions, log):
        asynchat.async_chat.__init__(self, sock=sock)
        self.sessions = sessions
        self.set_terminator("::::")
        self.reading_headers = True
        self.handling = False
        self.cgi_data = None
        self.log = log
        self.buffer = []

    def collect_incoming_data(self, data):
        try:
            self.buffer.append(data)
        except Exception, e:
            pass

    def found_terminator(self):
        a = ujson.loads(''.join(self.buffer))
        self.buffer = []
        stat.fire('websocket')
        stat.fire('ws2')


class EchoServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        stat.fire('accept')
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            handler = http_request_handler(sock, addr, None, None)

server = EchoServer('localhost', 8080)
asyncore.loop()