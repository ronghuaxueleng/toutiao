# -*- coding: utf-8 -*-
import datetime

from peewee import *

from DbUtils import get_conn

db = get_conn(database='c2hha2tlcg==')


class Model(Model):
    _id = PrimaryKeyField
    user_uuid = CharField(null=False)
    user_name = CharField(null=False)
    modelId = CharField(null=False)
    modelName = CharField(null=False)
    modelVersionName = CharField(null=False)
    modelType = IntegerField(null=False)
    showType = IntegerField(null=False)
    createTime = DateTimeField(null=True)
    updateTime = DateTimeField(null=True)
    isEnable = IntegerField(null=False, default=1)
    vipUsed = IntegerField(null=False, default=0)
    otherInfo = TextField(null=True)
    timestamp = DateTimeField(null=True, default=datetime.datetime.now)

    class Meta:
        database = db


if __name__ == '__main__':
    db.connect()
    db.create_tables([Model])
