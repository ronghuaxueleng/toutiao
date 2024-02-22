# -*- coding: utf-8 -*-
import base64
import json
import time

import requests

from liblibart.LogInfo import LogInfo
from liblibart.ql import ql_env


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
        self.uuids = [
            # cq
            "02749e73219936808ff45d707b2d01cf"
        ]
        my_loras = ql_env.search("my_lora")
        self.model_dict = {}
        for my_lora in my_loras:
            value = json.loads(my_lora['value'])
            self.model_dict[value['modelId']] = value

    def getUserInfo(self):
        url = f"https://{self.api_host}/api/www/user/getUserInfo?timestamp={time.time()}"
        payload = {}
        response = requests.request("POST", url, headers=self.headers, data=payload)
        self.userInfo = json.loads(response.text)['data']


if __name__ == '__main__':
    token = 'd1894681b7c5438b9051b840431e9b59'
    userInfo = UserInfo(token)
    print(userInfo.userInfo)
