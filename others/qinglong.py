import json
import base64
import requests


class QingLong():
    def __init__(self):
        self.host = "https://qinglong.ronghuaxueleng.top"
        self.client_id = "87-Qvk4Hk-nb"
        self.client_secret = "n-fxseqaQRE6F3rClKo0F1rl"
        self.token = None
        self.task_id = []

        self.header = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38'
        }

    def run(self, searchValue):
        # 获取token，启动任务
        if not self.get_qinglong_token():
            print("获取token失败")
            return False
        return self.get_cookie_list(searchValue)

    def get_qinglong_token(self):
        if not self.host and not self.client_id and not self.client_secret:
            print("参数无效")
            return False

        url = self.host + "/open/auth/token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        response = self.request_get_method(url, data)
        if response["code"] == 200:
            self.token = response["data"]["token"]
            return True
        else:
            print(response)
            print("认证失败,退出")
            return False

    def get_cookie_list(self, searchValue):
        '''获取任务列表，并筛选出指定的名称任务id'''
        url = f"{self.host}/open/envs?searchValue={searchValue}"
        return self.request_get_method(url=url)

    def request_get_method(self, url, params=None):
        '''
        青龙的get API
        :param url:
        :param params:
        :return:
        '''
        if self.token:
            self.header.update({"Authorization": f"Bearer {self.token}"})
        response = requests.get(url=url, params=params, headers=self.header, timeout=3)
        response_json = response.json()
        return response_json

    def request_post_method(self, url, data=None):
        '''
        青龙的post API
        :param url:
        :param data:
        :return:
        '''
        if self.token:
            self.header.update({"Authorization": f"Bearer {self.token}"})
        response = requests.post(url=url, json=data, headers=self.header, timeout=3)
        response_json = response.json()
        # print("request_post_method青龙响应：", response_json)
        return response_json


if __name__ == "__main__":
    response = QingLong().run('LXAPK_COOKIE')
    if response['code'] == 200:
        cookies = response['data']
        for cookie in cookies:
            print(cookie['value'])
