# -*- coding: utf-8 -*-
import os

from peewee import *

dbpath = os.path.join(os.path.split(os.path.realpath(__file__))[0], '..', 'config', 'account.db')
db = SqliteDatabase(dbpath)


# 账户信息
class Account(Model):
    user_id = CharField(null=False)
    name = CharField(null=False)
    sec_user_id = CharField(null=True)
    session_key = CharField(null=False)
    userInfo = TextField(null=False)
    headers = TextField(null=False)

    class Meta:
        database = db


class CommonParams(Model):
    user_id = CharField(null=False)
    iid = CharField(null=False)
    device_id = CharField(null=False)
    ac = CharField(null=False)
    mac_address = CharField(null=False)
    channel = CharField(null=False)
    aid = CharField(null=False)
    app_name = CharField(null=False)
    version_code = CharField(null=False)
    version_name = CharField(null=False)
    device_platform = CharField(null=False)
    ab_version = CharField(null=False)
    ab_client = CharField(null=False)
    ab_feature = CharField(null=False)
    abflag = CharField(null=False)
    ssmix = CharField(null=False)
    device_type = CharField(null=False)
    device_brand = CharField(null=False)
    language = CharField(null=False)
    os_api = CharField(null=False)
    os_version = CharField(null=False)
    uuid = CharField(null=False)
    openudid = CharField(null=False)
    manifest_version_code = CharField(null=False)
    resolution = CharField(null=False)
    dpi = CharField(null=False)
    update_version_code = CharField(null=False)
    plugin_state = CharField(null=False)
    sa_enable = CharField(null=False)
    rom_version = CharField(null=False)
    cdid = CharField(null=False)
    oaid = CharField(null=False)

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


# 京东
class Jd(Model):
    pin = CharField(null=False)
    wskey = CharField(null=False)

    class Meta:
        database = db


# 广告
class Iad(Model):
    source = CharField(null=False)
    web_url = CharField(null=False)

    class Meta:
        database = db


# 爱步宝
class Abb(Model):
    uid = CharField(null=False)
    real_name = CharField(null=True)
    nick = CharField(null=False)
    header = CharField(null=False)

    class Meta:
        database = db


if __name__ == '__main__':
    db.connect()
    db.create_tables([Abb])
