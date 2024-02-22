# -*- coding: utf-8 -*-
import datetime
import os

from peewee import *

dbpath = os.path.join(os.path.split(os.path.realpath(__file__))[0], '..', 'config', 'statistics.db')
db = SqliteDatabase(dbpath)


# 账户信息
class Statistics(Model):
    _id = PrimaryKeyField
    user_uuid = CharField(null=False)
    modelId = CharField(null=False)
    modelName = CharField(null=False)
    runCount = IntegerField(default=0, null=False)
    downloadModelCount = IntegerField(default=0, null=False)
    downloadImageCount = IntegerField(default=0, null=False)
    day = CharField()
    timestamp = DateTimeField(null=True, default=datetime.datetime.now)

    class Meta:
        database = db


if __name__ == '__main__':
    db.connect()
    db.create_tables([Statistics])
