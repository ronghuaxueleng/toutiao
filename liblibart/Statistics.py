# -*- coding: utf-8 -*-
import datetime
import os

from peewee import *

dbpath = os.path.join(os.path.split(os.path.realpath(__file__))[0], '..', 'liblibart', 'statistics.db')
db = SqliteDatabase(dbpath)


# 账户信息
class Statistics(Model):
    _id = PrimaryKeyField
    id = CharField()  # 模型id
    name = CharField()  # 模型名称
    user_uuid = CharField(null=False)
    runCount = IntegerField(default=0, null=False)
    downloadModelCount = IntegerField(default=0, null=False)
    downloadImageCount = IntegerField(default=0, null=False)
    timestamp = DateTimeField(null=True, default=datetime.datetime.now)

    class Meta:
        database = db


if __name__ == '__main__':
    db.connect()
    db.create_tables([Statistics])
