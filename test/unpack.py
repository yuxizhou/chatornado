__author__ = 'yuxizhou'

import struct
import ujson
import time

a = {
        'event': 1,
        'user': 'peter',
        'token': 'bbbbbbaaaaaa'
    }
m = ujson.dumps(a)

start = time.time()
i = 1000000
while i != 0:
    b = ujson.loads(m)
    i -= 1
print time.time() - start



message = struct.pack("I256s", 1, 'peter')
print len(message)
b = struct.unpack("I256s", message)
print b
message += m
print message
print len(message)
head = message[:260]
print struct.unpack("I256s", head)[1].strip()

start = time.time()
i = 1000000
while i != 0:
    head = message[:260]
    b = struct.unpack("I256s", head)
    i -= 1
print time.time() - start



