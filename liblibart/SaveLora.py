# -*- coding: utf-8 -*-
import datetime
import json
import os
import time

import requests

from liblibart.CookieUtils import get_users
from liblibart.UserInfo import UserInfo
from liblibart.Model import Model

from dotenv import load_dotenv, find_dotenv
from pathlib import Path

# 指定env文件
env_path = Path.cwd().joinpath('env').joinpath('os.env')
env_path.parent.mkdir(exist_ok=True)
load_dotenv(find_dotenv(str(env_path)))


class SaveLora(UserInfo):
    def __init__(self, token, webid, log_filename):
        super().__init__(token, webid, log_filename)

    def get_models(self):
        headers = {
            'authority': self.api_host,
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/json',
            'dnt': '1',
            'origin': f'https://{self.web_host}',
            'referer': f"https://{self.web_host}/userpage/{self.userInfo['uuid']}/publish",
            'sec-ch-ua': '"Chromium";v="119", "Not?A_Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'token': self.token,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.160 Safari/537.36',
            'webid': self.webid
        }

        pageNo = 1
        total_models = None
        while total_models is None or total_models > 0:
            url = f"https://{self.api_host}/api/www/model/list?timestamp={time.time()}"
            payload = json.dumps({
                "pageNo": pageNo,
                "pageSize": 10,
                "status": -2,
                "type": 0
            })

            response = requests.request("POST", url, headers=headers, data=payload)
            data = json.loads(response.text)
            pageNo = pageNo + 1
            total_models = len(data['data']['list'])
            for model in data['data']['list']:
                version_url = f"https://{self.api_host}/api/www/model/getByUuid/{model['uuid']}?timestamp={time.time()}"
                payload = {}
                response = requests.request("POST", version_url, headers=headers, data=payload)

                model_data = json.loads(response.text)
                for version in model_data['data']['versions']:
                    query = Model.select().where(
                        Model.user_uuid == self.userInfo['uuid'],
                        Model.modelId == version["id"]
                    )
                    if query.exists():
                        Model.update(
                            user_name=self.userInfo['nickname'],
                            modelName=model["name"],
                            modelVersionName=version['name'],
                            showType=version['showType'],
                            updateTime=version['updateTime'],
                            timestamp=datetime.datetime.now()
                        ).where(Model.user_uuid == self.userInfo['uuid'], Model.modelId == version["id"]).execute()
                    else:
                        Model.insert(
                            user_uuid=self.userInfo['uuid'],
                            user_name=self.userInfo['nickname'],
                            modelId=version["id"],
                            modelName=model["name"],
                            modelVersionName=version['name'],
                            modelType=model['modelType'],
                            showType=version['showType'],
                            createTime=version['createTime'],
                            updateTime=version['updateTime'],
                        ).execute()


if __name__ == '__main__':
    users = get_users()
    for user in users:
        try:
            SaveLora(user['usertoken'], user['webid'],
                     f'/mitmproxy/logs/SaveLora_{os.getenv("RUN_OS_KEY")}.log').get_models()
        except Exception as e:
            print('error', e)
            print(e)
