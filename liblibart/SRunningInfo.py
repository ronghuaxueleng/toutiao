# -*- coding: utf-8 -*-
import datetime

from peewee import *

from liblibart.DbUtils import get_conn

db = get_conn(database='c2hha2tlcg==')


# 运行信息
class RunningInfo(Model):
    _id = PrimaryKeyField
    to_run_users = TextField(null=True)
    checkpointIds = TextField(null=True)
    current_day = CharField(null=True)
    suanlibuzu_users = TextField(null=True)
    timestamp = DateTimeField(null=True, default=datetime.datetime.now)

    class Meta:
        database = db


if __name__ == '__main__':
    db.connect()
    db.create_tables([RunningInfo])
