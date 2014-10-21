__author__ = 'yuxizhou'

import redis

r = redis.StrictRedis('10.161.163.37', db=1)

for i in range(0, 200):
    r.sadd('G1', 'barney'+str(i))