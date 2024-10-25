# -*- coding: utf-8 -*-
import base64

import redis
from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import ReconnectMixin

# host = 'MTkyLjE0NC4yMTUuMjE4'
host = 'd3d3LnJvbmdodWF4dWVsZW5nLnNpdGU='

# 断线重连+连接池
class ReconnectPooledMySQLDatabase(ReconnectMixin, PooledMySQLDatabase):
    _instance = None

    @classmethod
    def get_db_instance(cls, database='bGlibGli'):
        if not cls._instance:
            user = 'cm9vdA=='
            password = 'MTIzNDU2Nzg='
            port = 'MzMwNg=='
            cls._instance = cls(str(base64.b64decode(database), 'utf-8'),
                                user=str(base64.b64decode(user), 'utf-8'),
                                password=str(base64.b64decode(password), 'utf-8'),
                                host=str(base64.b64decode(host), 'utf-8'),
                                port=int(str(base64.b64decode(port), 'utf-8')),
                                max_connections=10000,
                                stale_timeout=300,)
        return cls._instance


def get_conn(database='bGlibGli'):
    return ReconnectPooledMySQLDatabase.get_db_instance(database)


def get_redis_conn():
    password = 'eGlueWFuMTIwMw=='
    port = 'NjM3OQ=='
    pool = redis.ConnectionPool(
        host=str(base64.b64decode(host), 'utf-8'),
        password=str(base64.b64decode(password), 'utf-8'),
        port=int(str(base64.b64decode(port), 'utf-8')),
        db=1
    )
    return redis.Redis(connection_pool=pool)
