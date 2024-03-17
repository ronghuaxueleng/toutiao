# -*- coding: utf-8 -*-
import base64
import json
import os
import time

import requests
from peewee import *

from liblibart.LogInfo import LogInfo
from liblibart.ql import ql_env

dbpath = os.path.join(os.path.split(os.path.realpath(__file__))[0], '..', 'config', 'statistics.db')
db = SqliteDatabase(dbpath)


class Account(Model):
    _id = PrimaryKeyField
    user_uuid = CharField(null=False)
    nickname = CharField(null=False)
    userInfo = TextField(null=False)

    class Meta:
        database = db


def create_table(table):
    u"""
    如果table不存在，新建table
    """
    if not table.table_exists():
        table.create_table()


class UserInfo(LogInfo):
    def __init__(self, token):
        super().__init__()
        base64_web_host = 'd3d3LmxpYmxpYi5hcnQ='
        base64_api_host = 'bGlibGliLWFwaS52aWJyb3UuY29t'
        self.api_host = str(base64.b64decode(base64_api_host), 'utf-8')
        self.web_host = str(base64.b64decode(base64_web_host), 'utf-8')
        self.day = time.strftime('%Y%m%d', time.localtime())
        self.headers = {
            'authority': self.api_host,
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-length': '0',
            'content-type': 'application/x-www-form-urlencoded',
            'dnt': '1',
            'origin': f'https://{self.web_host}',
            'sec-ch-ua': '"Chromium";v="119", "Not?A_Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'token': token,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.160 Safari/537.36',
            'webid': '1701652270086cvpnqgrl'
        }
        self.token = token
        self.userInfo = {}
        self.getUserInfo()
        self.uuid = self.userInfo['uuid']
        self.uuids = set()
        my_loras = ql_env.search("my_lora")
        self.model_dict = {}
        self.user_model_dict = {}
        for my_lora in my_loras:
            value = json.loads(my_lora['value'])
            self.model_dict[value['modelId']] = value
            self.uuids.add(value['userUuid'])
            if value['modelType'] == 5:
                user_models = self.user_model_dict.setdefault(value['userUuid'], [])
                user_models.append(value)
                self.user_model_dict[value['userUuid']] = user_models

    def getUserInfo(self):
        url = f"https://{self.api_host}/api/www/user/getUserInfo?timestamp={time.time()}"
        payload = {}
        response = requests.request("POST", url, headers=self.headers, data=payload)
        self.userInfo = json.loads(response.text)['data']


if __name__ == '__main__':
    create_table(Account)
    tokens = [
        'd1894681b7c5438b9051b840431e9b59',
        '3cc0cddb72874db49eb02f60d81fbf31',
        '5035e42609394bdfa3ddaee8b88a1b78',
        '66149bee12304248beb571d1c0d9e553',
        '5dfe53b85ed947a6a92586182768a84e',
        '48e8c753b8674b1499f274d8973b9e60'
    ]
    for token in tokens:
        try:
            userInfo = UserInfo(token)
            user = userInfo.userInfo
            uuid = user['uuid']
            nickname = user['nickname']
            query = Account.select().where(Account.user_uuid == uuid)
            if query.exists():
                Account.update(
                    nickname=nickname,
                    userInfo=json.dumps(user)
                ).where(Account.user_uuid == uuid).execute()
            else:
                Account.insert(
                    user_uuid=uuid,
                    nickname=nickname,
                    userInfo=json.dumps(user)
                ).execute()
        except Exception as e:
            print(e)

