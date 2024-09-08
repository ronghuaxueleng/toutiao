# -*- coding: utf-8 -*-
import base64
import json
import os
import time

import requests
from peewee import *
from playhouse.shortcuts import model_to_dict

from liblibart.CookieUtils import get_users
from liblibart.DbUtils import get_conn
from liblibart.SModel import Model as MyModel
from liblibart.LogInfo import LogInfo
from liblibart.ql import ql_env

db = get_conn(database='c2hha2tlcg==')

from dotenv import load_dotenv, find_dotenv
from pathlib import Path

env_path = Path.cwd().joinpath('env').joinpath('sos.env')
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


class SharedImgUrl(Model):
    _id = PrimaryKeyField
    user_uuid = CharField(null=False)
    image_id = TextField(null=True)
    output_id = TextField(null=True)
    generate_id = TextField(null=True)
    show_users = TextField(null=True)
    download_users = TextField(null=True)
    own_download = IntegerField(null=False, default=0)

    class Meta:
        database = db


def create_table(table):
    u"""
    如果table不存在，新建table
    """
    if not table.table_exists():
        table.create_table()


class SUserInfo(LogInfo):
    def __init__(self, token, webid, bl_uid, log_filename):
        super().__init__(log_filename)
        base64_web_host = 'd3d3LnNoYWtrZXIuYWk='
        base64_api_host = 'd3d3LnNoYWtrZXIuYWk='
        self.api_host = str(base64.b64decode(base64_api_host), 'utf-8')
        self.web_host = str(base64.b64decode(base64_web_host), 'utf-8')
        self.day = time.strftime('%Y%m%d', time.localtime())
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'content-length': '0',
            'content-type': 'application/x-www-form-urlencoded',
            'dnt': '1',
            'origin': f'https://{self.web_host}',
            'priority': 'u=1, i',
            'referer': f'https://{self.web_host}/sd',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'token': token,
            'cookie': f'webid={webid}; liblibai_usertoken={token}; _bl_uid={bl_uid}',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            'webid': webid,
            'x-language': 'zh-TW'
        }
        self.token = token
        self.webid = webid
        self.bl_uid = bl_uid
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
        ).where(MyModel.isEnable == True, MyModel.modelType == 5).execute()
        for model in models:
            user_models = self.user_model_dict.setdefault(model.user_uuid, [])
            user_models.append(model_to_dict(model))
            self.user_model_dict[model.user_uuid] = user_models
        self.to_run_checkpointId = 1511727
        # if self.uuid == 'b8b05c9cf1c1487b802fba02dbfb128d':
        #     self.to_run_checkpointId = 2367748

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

    def getImageList(self, pageNo=1, pageSize=500):
        create_table(SharedImgUrl)
        url = f"https://{self.api_host}/gateway/sd-api/gen/tool/images"

        payload = json.dumps({
            "pageNo": pageNo,
            "pageSize": pageSize,
            "sort": -1,
            "dataReload": "event_historyList",
            "cid": self.webid
        })
        headers = self.headers
        headers['content-type'] = 'application/json'
        headers['referer'] = f'https://{self.web_host}/aigenerator'

        response = requests.request("POST", url, headers=headers, data=payload)
        res = json.loads(response.text)
        if res['code'] == 0:
            img_list = res['data']['list']
            for img in img_list:
                for image in img['images']:
                    outputId = image['outputId']
                    imageId = image['imageId']
                    generateId = image['generateId']
                    query = SharedImgUrl.select().where(SharedImgUrl.image_id == imageId,
                                                SharedImgUrl.output_id == outputId,
                                                SharedImgUrl.generate_id == generateId,
                                                )
                    if not query.exists():
                        SharedImgUrl.insert(
                            user_uuid=self.uuid,
                            image_id=imageId,
                            output_id=outputId,
                            generate_id=generateId
                        ).execute()
            return res['data']['list']
        else:
            return []


if __name__ == '__main__':
    create_table(Account)
    users = get_users(True, cookie_name="shakker_cookie", usertoken_name="liblibai_usertoken")
    disable_ids = []
    enable_ids = []
    for user in users:
        try:
            if user['expirationDate'] > time.time():
                userInfo = SUserInfo(user['usertoken'], user['webid'], user['_bl_uid'],
                                 f'/mitmproxy/logs/SUserInfo_{os.getenv("RUN_OS_KEY")}.log')
                realUser = userInfo.userInfo
            else:
                realUser = None
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
