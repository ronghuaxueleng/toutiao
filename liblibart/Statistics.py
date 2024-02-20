# -*- coding: utf-8 -*-
import os

from peewee import *

dbpath = os.path.join(os.path.split(os.path.realpath(__file__))[0], '..', 'liblibart', 'statistics.db')
db = SqliteDatabase(dbpath)


# 账户信息
class Statistics(Model):
    user_id = CharField(null=False)
    name = CharField(null=False)
    sec_user_id = CharField(null=True)
    session_key = CharField(null=False)
    userInfo = TextField(null=False)
    headers = TextField(null=False)

    class Meta:
        database = db


if __name__ == '__main__':
    db.connect()
    db.create_tables([Statistics])
