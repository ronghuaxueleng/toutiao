# -*- coding: utf-8 -*-
import base64
import json
import os
import time

import requests
from peewee import *
from playhouse.shortcuts import model_to_dict

from CookieUtils import get_users
from LogInfo import LogInfo
from DbUtils import get_conn
from Model import Model as MyModel
from ql import ql_env

db = get_conn()

from dotenv import load_dotenv, find_dotenv
from pathlib import Path

env_path = Path.cwd().joinpath('env').joinpath('os.env')
env_path.parent.mkdir(exist_ok=True)
# 指定env文件
load_dotenv(find_dotenv(str(env_path)))


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
    def __init__(self, token, webid, log_filename):
        super().__init__(log_filename)
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
            'webid': webid
        }
        self.token = token
        self.webid = webid
        self.userInfo = {}
        self.getUserInfo()
        if self.userInfo is not None:
            self.uuid = self.userInfo['uuid']
        self.uuids = set()
        self.model_dict = {}
        self.user_model_dict = {}
        models = MyModel.select(
            MyModel.user_uuid,
            MyModel.modelId
        ).where(MyModel.isEnable == True,
                MyModel.modelType == 5,
                MyModel.user_uuid != self.uuid).execute()
        for model in models:
            user_models = self.user_model_dict.setdefault(model.user_uuid, [])
            user_models.append(model_to_dict(model))
            self.user_model_dict[model.user_uuid] = user_models

    def getUserInfo(self):
        url = f"https://{self.api_host}/api/www/user/getUserInfo?timestamp={time.time()}"
        payload = {}
        response = requests.request("POST", url, headers=self.headers, data=payload)
        res = json.loads(response.text)
        if res['code'] == 0:
            data = res['data']
            print(data['nickname'], data['uuid'])
            self.userInfo = data
        else:
            self.userInfo = None


if __name__ == '__main__':
    create_table(Account)
    users = get_users(True)
    disable_ids = []
    enable_ids = []
    for user in users:
        try:
            userInfo = UserInfo(user['usertoken'], user['webid'],
                                f'/mitmproxy/logs/UserInfo_{os.getenv("RUN_OS_KEY")}.log')
            realUser = userInfo.userInfo
            if realUser is not None:
                enable_ids.append(user['id'])
                uuid = realUser['uuid']
                nickname = realUser['nickname']
                query = Account.select().where(Account.user_uuid == uuid)
                if query.exists():
                    Account.update(
                        user_uuid=uuid,
                        nickname=nickname,
                        userInfo=json.dumps(realUser)
                    ).where(Account.user_uuid == uuid).execute()
                else:
                    Account.insert(
                        user_uuid=uuid,
                        nickname=nickname,
                        userInfo=json.dumps(realUser)
                    ).execute()
            else:
                disable_ids.append(user['id'])
        except Exception as e:
            print(e)
    if len(disable_ids) > 0:
        ql_env.disable(disable_ids)
    if len(enable_ids) > 0:
        ql_env.enable(enable_ids)
