import asyncore
import socket
import ujson


class HTTPClient(asyncore.dispatcher):

    def __init__(self, host, path):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect( (host, 8080) )
        self.buffer = ''

        # i=1
        # while i != 1000000:
        #     self.buffer += str(i)+'  '
        #
        #     if i % 1000 == 0:
        #         self.buffer += '::::'
        #
        #     i += 1

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
        print self.recv(8192)

    def writable(self):
        t = {
            'event': 2,
            'from': 'wfewesdvsd',
            'to': 'awefwfewef',
            'content': 'laksjfdlasjk;fdjsa;kdfjksaj;fdklsaj;lkfdjksajdfoiwjdflsajofewjojflksahdfoiwoef'
        }
        self.buffer = ujson.dumps(t)+'::::'
        return True
        # return (len(self.buffer) > 0)

    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]


client = HTTPClient('127.0.0.1', '/')
asyncore.loop()