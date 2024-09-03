# -*- coding: utf-8 -*-
import datetime
import json
import os
import time

import requests

from CookieUtils import get_users
from SModel import Model
from SUserInfo import SUserInfo
from ql import ql_env

from dotenv import load_dotenv, find_dotenv
from pathlib import Path

# 指定env文件
env_path = Path.cwd().joinpath('env').joinpath('sos.env')
env_path.parent.mkdir(exist_ok=True)
load_dotenv(find_dotenv(str(env_path)))


class SSaveLora(SUserInfo):
    def __init__(self, token, webid, bl_uid, log_filename):
        super().__init__(token, webid, bl_uid, log_filename)

    def get_models(self):
        headers = {
            'authority': self.api_host,
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/json',
            'cookie': f'webid={self.webid}; liblibai_usertoken={self.token}; _bl_uid={self.bl_uid}',
            'dnt': '1',
            'origin': f'https://{self.web_host}',
            'referer': f"https://{self.web_host}/userpage/{self.userInfo['uuid']}/publish",
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'token': self.token,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36',
            'webid': self.webid,
            'x-language': 'zh-TW'
        }

        saved_models = []
        saved_model_id_map = {}
        try:
            my_loras = ql_env.search("my_shakker_lora")
            for my_lora in my_loras:
                if my_lora['status'] == 0:
                    value = json.loads(my_lora['value'])
                    modelId = value['modelId']
                    saved_models.append(modelId)
                    saved_model_id_map[modelId] = my_lora['id']
        except Exception as e:
            print(e)

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
                    to_save_data = {
                        "modelId": version["id"],
                        "type": 0,
                        "modelName": model["name"],
                        "modelVersionName": version['name'],
                        "weight": 0.8,
                        "userUuid": self.userInfo['uuid'],
                        "modelType": model['modelType']
                    }
                    if version['id'] not in saved_models:
                        ql_env.add("my_shakker_lora", json.dumps(to_save_data, ensure_ascii=False), model["name"])
                    else:
                        ql_env.update(json.dumps(to_save_data, ensure_ascii=False), "my_shakker_lora",
                                      saved_model_id_map[version['id']], model["name"])

                    query = Model.select().where(Model.user_uuid == self.userInfo['uuid'],
                                                 Model.modelId == version["id"])
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
    users = get_users(cookie_name="shakker_cookie", usertoken_name="liblibai_usertoken")
    for user in users:
        try:
            SSaveLora(user['usertoken'], user['webid'], user['_bl_uid'],
                     f'/mitmproxy/logs/SSaveLora_{os.getenv("RUN_OS_KEY")}.log').get_models()
        except Exception as e:
            print('error', e)
            print(e)
