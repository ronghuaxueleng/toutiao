# -*- coding: utf-8 -*-
import base64
import copy
import json
import logging
import time
import traceback
from datetime import datetime

import requests

from app.Base import Base
from liblibart.ql import ql_env

logging.basicConfig(level=logging.ERROR,
                    filename='/mitmproxy/logs/wxlogin.log',
                    datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')
logger = logging.getLogger(__name__)


class LiblibwxLogin(Base):
    def __init__(self, starttime=None):
        super().__init__("有微信用户登录了")
        self.ticket = None
        self.qrCodeUrl = None
        self.expireSeconds = 120
        self.starttime = starttime if starttime is not None else int(time.time())
        self.headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'content-type': 'application/json',
            'cache-control': 'no-cache',
            'content-length': '0',
            'dnt': '1',
            'origin': str(base64.b64decode('aHR0cHM6Ly93d3cubGlibGliLmFydA=='), 'utf-8'),
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': str(base64.b64decode('aHR0cHM6Ly93d3cubGlibGliLmFydC9tZXNzYWdl'), 'utf-8'),
            'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            'webid': '1729047875238gwboidea'
        }

    def get_qrcode(self):
        url = str(base64.b64decode("aHR0cHM6Ly93d3cubGlibGliLmFydC9hcGkvd3d3L3dlaXhpbi9sb2dpbi9zaG93cXJjb2Rl"), 'utf-8')
        payload = json.dumps({
            "source": "liblib"
        })
        response = requests.request("POST", url, headers=self.headers, data=payload)
        res = json.loads(response.text)
        data = json.loads(res["data"])
        self.ticket = data['ticket']
        self.expireSeconds = data['expireSeconds']
        self.qrCodeUrl = data['qrCodeUrl']
        return res['data']

    def qrcode(self, ticket, id=None):
        headers = copy.deepcopy(self.headers)
        headers['content-type'] = 'application/json'
        try:
            while int(time.time()) - int(self.starttime) < self.expireSeconds:
                url = str(base64.b64decode("aHR0cHM6Ly93d3cubGlibGliLmFydC9hcGkvd3d3L3dlaXhpbi9sb2dpbi9xcmNvZGU="), 'utf-8')
                payload = json.dumps({
                    "ticket": ticket
                })
                response = requests.request("POST", url, headers=headers, data=payload)
                cookies = requests.utils.dict_from_cookiejar(response.cookies)
                if len(cookies) > 0:
                    cookieArr = []
                    for key, value in cookies.items():
                        cookieArr.append('%s=%s' % (key, value))
                    headers['cookie'] = ';'.join(cookieArr)
                res = json.loads(response.text)
                data = res['data']
                if data is not None:
                    nickname = ''
                    token = data['userToken']
                    if id is None or id == "" or id == "None":
                        headers['token'] = token
                        headers['content-type'] = 'application/x-www-form-urlencoded'
                        url = str(base64.b64decode(
                            "aHR0cHM6Ly93d3cubGlibGliLmFydC9hcGkvd3d3L3VzZXIvZ2V0VXNlckluZm8/dGltZXN0YW1wPQ=="),
                                  'utf-8') + str(int(time.time()))
                        response = requests.request("POST", url, headers=headers, data={})
                        res = json.loads(response.text)
                        data = res['data']
                        nickname = data['nickname']
                    cookies = headers['cookie']
                    cookies = dict([l.split("=", 1) for l in cookies.split("; ")])
                    cookies['usertoken'] = token
                    cookies['webid'] = '1729047875238gwboidea'
                    value = self.get_cookies(cookies['usertoken'], cookies['webid'])
                    if id is not None and id != "" and id != "None":
                        info = ql_env.get_by_id(id)
                        if info['code'] == 200:
                            data = info['data']
                            name = data['name']
                            remarks = data['remarks']
                            sourcetype = '微信'
                            username = data['username']
                            createtime = data['createtime']
                            logger.info(f"{remarks}登录")
                            ql_env.update(value, name, id, remarks, sourcetype, username, createtime)
                            ql_env.enable([id])
                            self.send_msg(remarks + '-' + username)
                    else:
                        name = 'liblib_cookie'
                        remarks = f'wx-{nickname}'
                        logger.info(f"{remarks}登录")
                        res = ql_env.search(remarks)
                        if len(res) > 0:
                            info = res[0]
                            id = info['id']
                            sourcetype = '微信'
                            username = info['username']
                            createtime = info['createtime']
                            ql_env.update(value, name, id, remarks, sourcetype, username, createtime)
                            ql_env.enable([id])
                            self.send_msg(remarks + '-' + username)
                        else:
                            sourcetype = '微信'
                            username = ''
                            time_now = datetime.now()
                            createtime = time_now.strftime("%Y年%m月%d日 %H:%M:%S")
                            ql_env.add(name, value, remarks, sourcetype, username, createtime)
                            self.send_msg(remarks)
                    return 'ok'
                time.sleep(2)
        except Exception as e:
            logger.error(traceback.format_exc())
        return 'fail'

    def get_cookies(self, usertoken, webid):
        cookies = [
            {
                "domain": str(base64.b64decode("Lnd3dy5saWJsaWIuYXJ0"), 'utf-8'),
                "hostOnly": False,
                "httpOnly": False,
                "name": "usertoken",
                "path": "/",
                "sameSite": None,
                "secure": False,
                "session": True,
                "storeId": None,
                "value": usertoken
            },
            {
                "domain": str(base64.b64decode("Lnd3dy5saWJsaWIuYXJ0"), 'utf-8'),
                "hostOnly": False,
                "httpOnly": False,
                "name": "webid",
                "path": "/",
                "sameSite": None,
                "secure": False,
                "session": True,
                "storeId": None,
                "value": webid
            }
        ]
        return json.dumps(cookies, ensure_ascii=False, indent=4)