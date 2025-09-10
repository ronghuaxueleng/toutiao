# -*- coding: utf-8 -*-
import base64
import json
import logging
import time
import traceback
from datetime import datetime
import uuid

import requests

from app.Base import Base
from liblibart.ql import ql_env

logging.basicConfig(level=logging.ERROR,
                    filename='/mitmproxy/logs/phonelogin.log',
                    datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')
logger = logging.getLogger(__name__)


class LiblibPhoneLogin(Base):
    def __init__(self):
        super().__init__("有手机用户登录了")
        self.sess = None
        self.newSession()
        self.expireSeconds = 120  # 验证码有效时间
        self.starttime = int(time.time())
        self.cid = "1757506011963sukpxrvq"

    def newSession(self):
        self.sess = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/140.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Origin': str(base64.b64decode('aHR0cHM6Ly93d3cubGlibGliLmFydA=='), 'utf-8'),
            'Pragma': 'no-cache',
            'Referer': str(base64.b64decode('aHR0cHM6Ly93d3cubGlibGliLmFydC9pbmNvbWVSZXBvcnQvMTU0MzA2NjE='), 'utf-8'),
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }
        self.sess.headers.update(headers)
        return

    def sendLoginPhoneCode(self, phone):
        """发送手机验证码"""
        try:
            url = str(base64.b64decode('aHR0cHM6Ly9wYXNzcG9ydC5saWJsaWIuYXJ0L2FwaS93d3cvbG9naW4vc2VuZExvZ2luUGhvbmVDb2Rl'), 'utf-8')
            payload = json.dumps({
                "phone": phone
            })

            headers = {
                'Content-Type': 'application/json'
            }

            response = self.sess.post(url, headers=headers, data=payload, timeout=30)

            logger.info(f"发送验证码响应: {response.text}")

            result = json.loads(response.text)
            if result.get('code') == 0:
                return {"status": "success", "message": "验证码发送成功", "phone": phone}
            else:
                return {"status": "error", "message": result.get('message', '发送验证码失败')}

        except Exception as e:
            logger.error(f"发送验证码异常: {traceback.format_exc()}")
            return {"status": "error", "message": str(e)}

    def loginByPhoneCode(self, phone, code, id=None):
        """使用手机验证码登录"""
        try:
            url = str(base64.b64decode('aHR0cHM6Ly9wYXNzcG9ydC5saWJsaWIuYXJ0L2FwaS93d3cvbG9naW4vbG9naW5CeVBob25lQ29kZQ=='), 'utf-8')
            payload = json.dumps({
                "phone": phone,
                "code": code,
                "cid": self.cid
            })

            headers = {
                'Content-Type': 'application/json'
            }

            response = self.sess.post(url, headers=headers, data=payload, timeout=30)

            logger.info(f"手机登录响应: {response.text}")

            result = json.loads(response.text)
            if result.get('code') == 0:
                # 从响应中提取token信息
                data = result.get('data', {})
                usertoken = data.get('token', '')
                webid = self.cid

                if usertoken and webid:
                    value = self.get_cookies(usertoken, webid)

                    if id is not None and id != "" and id != "None":
                        # 更新已存在的环境变量
                        info = ql_env.get_by_id(id)
                        if info['code'] == 200:
                            data_info = info['data']
                            name = data_info['name']
                            remarks = data_info['remarks']
                            sourcetype = '手机号'
                            username = data_info['username']
                            createtime = data_info['createtime']
                            logger.info(f"{remarks}登录")
                            ql_env.update(value, name, id, remarks, sourcetype, username, createtime)
                            ql_env.enable([id])
                            self.send_msg(remarks + '-' + username)
                    else:
                        # 创建新的环境变量
                        name = 'liblib_cookie'
                        remarks = phone
                        logger.info(f"{remarks}登录")
                        res = ql_env.search(remarks)
                        if len(res) > 0:
                            # 更新已存在的记录
                            info = res[0]
                            id = info['id']
                            sourcetype = '手机号'
                            username = info['username']
                            createtime = info['createtime']
                            ql_env.update(value, name, id, remarks, sourcetype, username, createtime)
                            ql_env.enable([id])
                            self.send_msg(remarks + '-' + username)
                        else:
                            # 创建新记录
                            sourcetype = '手机号'
                            username = ''
                            time_now = datetime.now()
                            createtime = time_now.strftime("%Y年%m月%d日 %H:%M:%S")
                            ql_env.add(name, value, remarks, sourcetype, username, createtime)
                            self.send_msg(remarks)

                    return {"status": "success", "message": "登录成功"}
                else:
                    return {"status": "error", "message": "获取登录信息失败"}
            else:
                return {"status": "error", "message": result.get('message', '登录失败')}

        except Exception as e:
            logger.error(f"手机登录异常: {traceback.format_exc()}")
            return {"status": "error", "message": str(e)}

    def get_cookies(self, usertoken, webid):
        """格式化cookies"""
        t = datetime.now()
        # 设置过期时间
        expire_time = int(time.mktime((t.replace(year=t.year + 1)).timetuple()))

        cookies = [
            {
                "domain": str(base64.b64decode("Lnd3dy5saWJsaWIuYXJ0"), 'utf-8'),
                "expirationDate": expire_time,
                "hostOnly": False,
                "httpOnly": False,
                "name": "usertoken",
                "path": "/",
                "sameSite": None,
                "secure": False,
                "session": False,
                "storeId": None,
                "value": usertoken
            },
            {
                "domain": str(base64.b64decode("Lnd3dy5saWJsaWIuYXJ0"), 'utf-8'),
                "expirationDate": expire_time,
                "hostOnly": False,
                "httpOnly": False,
                "name": "usertoken_online",
                "path": "/",
                "sameSite": None,
                "secure": False,
                "session": False,
                "storeId": None,
                "value": usertoken
            },
            {
                "domain": str(base64.b64decode("Lnd3dy5saWJsaWIuYXJ0"), 'utf-8'),
                "expirationDate": expire_time,
                "hostOnly": False,
                "httpOnly": False,
                "name": "webid",
                "path": "/",
                "sameSite": None,
                "secure": False,
                "session": False,
                "storeId": None,
                "value": webid
            },
            {
                "domain": str(base64.b64decode("Lnd3dy5saWJsaWIuYXJ0"), 'utf-8'),
                "expirationDate": expire_time,
                "hostOnly": False,
                "httpOnly": False,
                "name": "usertokenExt",
                "path": "/",
                "sameSite": None,
                "secure": False,
                "session": False,
                "storeId": None,
                "value": usertoken
            },
            {
                "domain": str(base64.b64decode("Lnd3dy5saWJsaWIuYXJ0"), 'utf-8'),
                "expirationDate": expire_time,
                "hostOnly": False,
                "httpOnly": False,
                "name": "webidExt",
                "path": "/",
                "sameSite": None,
                "secure": False,
                "session": False,
                "storeId": None,
                "value": webid
            }
        ]
        return json.dumps(cookies, ensure_ascii=False, indent=4)
