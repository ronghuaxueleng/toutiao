# -*- coding: utf-8 -*-
import base64
import threading

import redis
from peewee import OperationalError
from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import ReconnectMixin

# host = 'MTkyLjE0NC4yMTUuMjE4'
host = 'MTkyLjE2OC4xMC4xNQ=='


class ReconnectPooledMySQLDatabase(ReconnectMixin, PooledMySQLDatabase):
    _instance = None
    _lock = threading.Lock()  # 线程安全锁

    @classmethod
    def get_db_instance(cls, database='bGlibGli'):
        with cls._lock:  # 线程安全单例
            if not cls._instance:
                user = 'cm9vdA=='
                password = 'WGlueWFuMTIwM0BA'
                port = 'MzMwNg=='
                cls._instance = cls(
                    str(base64.b64decode(database), 'utf-8'),
                    user=str(base64.b64decode(user), 'utf-8'),
                    password=str(base64.b64decode(password), 'utf-8'),
                    host=str(base64.b64decode(host), 'utf-8'),
                    port=int(str(base64.b64decode(port), 'utf-8')),
                    # ✅ 连接池参数（直接传递）
                    max_connections=200,  # 合理最大值
                    stale_timeout=290,  # 短于MySQL超时(300秒)
                    timeout=30,  # 获取连接超时
                    # ✅ 驱动参数（使用 ** 前缀传递）
                    autocommit=True,  # 自动提交
                    **{
                        'connect_timeout': 15,  # TCP连接超时
                        'read_timeout': 30,  # 查询超时
                        'write_timeout': 30,  # 写入超时
                        'charset': 'utf8mb4',  # 字符集
                    }
                )
                # 初始化连接验证
                cls._instance.health_check()
            return cls._instance

    def health_check(self):
        """连接池健康检查"""
        try:
            with self.connection_context():
                self.execute_sql("SELECT 1")  # 心跳检测
        except OperationalError:
            self.manual_close()  # 强制重置连接池
            self.connect()


# 断线重连+连接池

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
