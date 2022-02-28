# -*- coding: utf-8 -*-
import os

from peewee import *

dbpath = os.path.join(os.path.split(os.path.realpath(__file__))[0], '..', 'config', 'account_toutiao.db')
db = SqliteDatabase(dbpath)


# 账户信息
class Account(Model):
    user_id = CharField(null=False)
    name = CharField(null=False)
    sec_user_id = CharField(null=True)
    session_key = CharField(null=False)
    userInfo = TextField(null=False)
    headers = TextField(null=False)
    commonParams = TextField(null=False)

    class Meta:
        database = db


class Task(Model):
    session_key = CharField(null=False)
    host = CharField(null=False)
    path = CharField(null=False)
    url = TextField(null=False)
    method = TextField(null=False)
    header = TextField(null=False)
    body = TextField(null=False)
    type = CharField(null=False)

    class Meta:
        database = db


class Article(Model):
    group_id = CharField(null=False)

    class Meta:
        database = db


if __name__ == '__main__':
    db.connect()
    db.create_tables([Account, Task, Article])
