# -*- coding: utf-8 -*-
import json
import os
import time

import requests

from liblibart.CookieUtils import get_users
from liblibart.UserInfo import UserInfo
from liblibart.ql import ql_env

from dotenv import load_dotenv, find_dotenv
from pathlib import Path

# 指定env文件
env_path = Path.cwd().joinpath('..').joinpath('env').joinpath('os.env')
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

        my_loras = ql_env.search("my_lora")
        saved_models = []
        saved_model_id_map = {}
        for my_lora in my_loras:
            if my_lora['status'] == 0:
                value = json.loads(my_lora['value'])
                modelId = value['modelId']
                saved_models.append(modelId)
                saved_model_id_map[modelId] = my_lora['id']

        for pageNo in range(1, 5):
            url = f"https://{self.api_host}/api/www/model/list?timestamp={time.time()}"
            payload = json.dumps({
                "pageNo": pageNo,
                "pageSize": 20,
                "uuid": self.userInfo['uuid'],
                "status": -2,
                "type": 0
            })

            response = requests.request("POST", url, headers=headers, data=payload)
            data = json.loads(response.text)
            if len(data['data']['list']) == 0:
                break
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
                        ql_env.add("my_lora", json.dumps(to_save_data, ensure_ascii=False), model["name"])
                    else:
                        ql_env.update(json.dumps(to_save_data, ensure_ascii=False), "my_lora",
                                      saved_model_id_map[version['id']], model["name"])


if __name__ == '__main__':
    users = get_users()
    for user in users:
        try:
            SaveLora(user['usertoken'], user['webid'],
                     f'/mitmproxy/logs/SaveLora_{os.getenv("RUN_OS_KEY")}.log').get_models()
        except Exception as e:
            print('error', e)
            print(e)
