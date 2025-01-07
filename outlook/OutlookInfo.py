# -*- coding: utf-8 -*-
import datetime

from peewee import *

from liblibart.DbUtils import get_conn

db = get_conn(database='c2hha2tlcg==')


# OutlookInfo
class OutlookInfo(Model):
    _id = PrimaryKeyField
    email = TextField(null=True)
    client_id = TextField(null=True)
    client_secret = TextField(null=True)
    refresh_token = TextField(null=True)
    timestamp = DateTimeField(null=True, default=datetime.datetime.now)

    class Meta:
        database = db

    @property
    def id(self):
        return self._id


if __name__ == '__main__':
    db.connect()
    db.create_tables([OutlookInfo])
