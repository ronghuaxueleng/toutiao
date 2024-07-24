# -*- coding: utf-8 -*-
import json

import requests

from CookieUtils import get_users
from UserInfo import UserInfo


class Msg(UserInfo):
    def __init__(self, token, webid, log_filename):
        super().__init__(token, webid, log_filename)

    def getMsg(self):
        url = f"https://{self.api_host}/api/www/community/myTypeMsg?firstType=1&secondType=7&page=1&pageSize=1"

        payload = {}
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cache-control': 'no-cache',
            'content-length': '0',
            'dnt': '1',
            'origin': f'https://{self.web_host}',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': f'https://{self.web_host}/message',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'token': self.token,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'webid': self.webid
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        res = json.loads(response.text)
        print(res['data'])
        # if res['data'] is not None:
        #     print(res['data'])


if __name__ == '__main__':
    users = get_users()
    for user in users:
        try:
            Msg(user['usertoken'], user['webid'], '/mitmproxy/logs/Msg.log').getMsg()
        except Exception as e:
            print('error', e)
            print(e)
