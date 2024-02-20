# -*- coding: utf-8 -*-
import json
import time

import requests

from liblibart.UserInfo import UserInfo
from liblibart.ql import ql_env


class SaveLora(UserInfo):
    def __init__(self, token):
        super().__init__(token)

    def get_models(self, pageNo):
        url = "https://liblib-api.vibrou.com/api/www/model/list?timestamp={time.time()}"
        payload = json.dumps({
            "pageNo": pageNo,
            "pageSize": 20,
            "uuid": self.userInfo['uuid'],
            "status": -2,
            "type": 0
        })
        headers = {
            'authority': 'liblib-api.vibrou.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/json',
            'dnt': '1',
            'origin': 'https://www.liblib.art',
            'referer': f"https://www.liblib.art/userpage/{self.userInfo['uuid']}/publish",
            'sec-ch-ua': '"Chromium";v="119", "Not?A_Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'token': self.token,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.160 Safari/537.36',
            'webid': '1701652270086cvpnqgrl'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        my_loras = ql_env.search("my_lora")
        saved_models = []
        for my_lora in my_loras:
            if my_lora['status'] == 0:
                saved_models.append(json.loads(my_lora['value'])['modelId'])

        data = json.loads(response.text)
        for model in data['data']['list']:
            if model['modelType'] == 5:
                version_url = f"https://liblib-api.vibrou.com/api/www/model/getByUuid/{model['uuid']}?timestamp={time.time()}"
                payload = {}
                response = requests.request("POST", version_url, headers=headers, data=payload)

                model_data = json.loads(response.text)
                for version in model_data['data']['versions']:
                    if version['id'] not in saved_models:
                        to_save_data = {
                            "modelId": version["id"],
                            "type": 0,
                            "modelName": model["name"],
                            "modelVersionName": version['name'],
                            "weight": 0.8,
                            "userUuid": self.userInfo['uuid']
                        }
                        ql_env.add("my_lora", json.dumps(to_save_data, ensure_ascii=False), model["name"])


if __name__ == '__main__':
    tokens = [
        'd1894681b7c5438b9051b840431e9b59',
        '3cc0cddb72874db49eb02f60d81fbf31',
        '5035e42609394bdfa3ddaee8b88a1b78',
        '66149bee12304248beb571d1c0d9e553',
        '5dfe53b85ed947a6a92586182768a84e'
    ]
    for pageNo in range(1, 5):
        for token in tokens:
            try:
                SaveLora(token).get_models(pageNo)
            except Exception as e:
                print(e)