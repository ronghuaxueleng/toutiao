# -*- coding: utf-8 -*-
import base64

import redis
from playhouse.pool import PooledMySQLDatabase


def get_conn(database='bGlibGli'):
    user = 'cm9vdA=='
    password = 'MTIzNDU2Nzg='
    host = 'MTkyLjE0NC4yMTUuMjE4'
    port = 'MzMwNjA='
    return PooledMySQLDatabase(str(base64.b64decode(database), 'utf-8'),
                               user=str(base64.b64decode(user), 'utf-8'),
                               password=str(base64.b64decode(password), 'utf-8'),
                               host=str(base64.b64decode(host), 'utf-8'),
                               port=int(str(base64.b64decode(port), 'utf-8')),
                               max_connections=20,
                               stale_timeout=300,
                               )


def get_redis_conn():
    host = 'MTkyLjE0NC4yMTUuMjE4'
    port = 'NjM3OQ=='
    pool = redis.ConnectionPool(host=host, port=port, db=1, decode_responses=True)
    return redis.Redis(connection_pool=pool)
