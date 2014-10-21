__author__ = 'yuxizhou'

import redis

r = redis.StrictRedis()
r.set('a', 'b')