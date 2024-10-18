# -*- coding: utf-8 -*-
import json
from datetime import datetime

import requests


class Base:
    def __init__(self, title):
        self.title = title
        self.token = '258f84f44f0246c38bffb7d03733a825'
        self.url = 'http://www.pushplus.plus/send'

    def send_msg(self, content):
        time_now = datetime.now()
        current_time = time_now.strftime("%Y年%m月%d日 %H:%M:%S")
        content = f'用户【{content}】在{current_time}登录'
        data = {
            "token": self.token,
            "title": self.title,
            "content": content
        }
        body = json.dumps(data).encode(encoding='utf-8')
        headers = {'Content-Type': 'application/json'}
        requests.post(self.url, data=body, headers=headers)
