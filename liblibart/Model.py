# -*- coding: utf-8 -*-
import datetime

from peewee import *

from DbUtils import get_conn

db = get_conn()


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
    timestamp = DateTimeField(null=True, default=datetime.datetime.now)

    class Meta:
        database = db


def create_tables(tables: list):
    db.connect()
    for table in tables:
        u"""
        如果table不存在，新建table
        """
        if not table.table_exists():
            table.create_table()


if __name__ == '__main__':
    create_tables([Model])
