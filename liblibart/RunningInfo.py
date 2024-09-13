# -*- coding: utf-8 -*-
import datetime

from peewee import *

from liblibart.DbUtils import get_conn

db = get_conn()


# 运行信息
class RunningInfo(Model):
    _id = PrimaryKeyField
    to_run_users = TextField(null=True)
    checkpoints = TextField(null=True)
    to_runcheckpoints = TextField(null=True)
    current_day = TextField(null=True)
    suanlibuzu_users = TextField(null=True)
    timestamp = DateTimeField(null=True, default=datetime.datetime.now)

    class Meta:
        database = db

    @property
    def id(self):
        return self._id


if __name__ == '__main__':
    db.connect()
    db.create_tables([RunningInfo])
