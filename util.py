__author__ = 'yuxizhou'

import socket
import logging
from logging.handlers import TimedRotatingFileHandler
from tornado.options import define, options, parse_command_line
import time

time_handler = None


def get_logger(module_name, log_file, level=logging.INFO):
    logger = logging.getLogger(module_name)
    logger.setLevel(level)

    global time_handler
    if not time_handler:
        time_handler = TimedRotatingFileHandler(log_file + '.time', when='midnight')
        time_handler.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        time_handler.setFormatter(formatter)

    logger.addHandler(time_handler)

    return logger


class Stat(object):
    def __init__(self):
        self.first = self.last = int(time.time())
        self.counter = {}

    def __count(self):
        self.first = int(time.time())

        if self.first != self.last:
            for c in self.counter:
                print str(self.last) + ' ' + c + ' ' + str(self.counter[c])

            self.counter = {}
            self.last = self.first

    def fire(self, event):
        if event in self.counter:
            self.counter[event] += 1
        else:
            self.counter[event] = 1
        self.__count()


define('env', default='DEVELOPMENT')
parse_command_line()
if options.env == 'PRODUCTION':
    config = {
        'redis': '10.161.163.37',
        'nsqd': ['10.161.163.37:4150'],
        # 'nsqd': [                                       # for writer
        #     '10.132.33.105:4150',
        #     '10.132.36.128:4150',
        #     '10.160.39.33:4150',
        #     '10.160.52.15:4150',
        #     '10.160.52.145:4150',
        # ],
        'nsqlookupd': ['http://10.161.163.144:4161'],   # for reader
        'hostname': socket.gethostname(),
        'nodes': [                      # outer ip
            '10.132.33.105',
            '10.132.36.128',
            '10.160.39.33',
            '10.160.52.15',
            '10.160.52.145',
        ],
        'node2hostname': {              # outer ip to hostname
            '10.132.33.105': 'chat2',
            '10.132.36.128': 'chat3',
            '10.160.39.33': 'chat4',
            '10.160.52.15': 'chat5',
            '10.160.52.145': 'chat6',
        },
        'node2inner': {              # outer ip to inner ip
            '10.132.33.105': '10.132.33.105',
            '10.132.36.128': '10.132.36.128',
            '10.160.39.33': '10.160.39.33',
            '10.160.52.15': '10.160.52.15',
            '10.160.52.145': '10.160.52.145',
        },
        'port': 8777,
    }
else:
    config = {
        'redis': '127.0.0.1',
        'nsqd': ['115.29.170.94:4150', '115.29.171.57:4150'],
        'nsqlookupd': ['http://115.29.170.94:4161'],
        'hostname': socket.gethostname(),
        'nodes': ['127.0.0.1'],
        'node2hostname': {
            '127.0.0.1': 'yuxizhou-ThinkPad-T430',
        },
        'node2hostname': {
            '127.0.0.1': '127.0.0.1',
        },
        'port': 8777
    }

# weixin1   10.161.163.144  115.29.170.94
# weixin2   10.161.163.37   115.29.171.57