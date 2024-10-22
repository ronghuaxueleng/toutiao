# -*- coding: utf-8 -*-
import base64
import json
import logging
import time
import datetime
import traceback

import requests
import zmail
from bs4 import BeautifulSoup

from app.Base import Base
from liblibart.ql import ql_env

#配置邮箱信息
sender = 'caoqianghappy@126.com'  #发件人的地址
password = 'GGVQ5CPAcHtHfkBx'  #此处是我们刚刚在邮箱中获取的授权码
server = zmail.server(sender, password)

logging.basicConfig(level=logging.ERROR,
                    filename='/mitmproxy/logs/emaillogin.log',
                    datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')
logger = logging.getLogger(__name__)


class ShakkerEmailLogin(Base):
    def __init__(self):
        super().__init__("有邮箱用户登录了")
        self.sess = None
        self.newSession()
        self.expireSeconds = 120
        self.starttime = int(time.time())

    def newSession(self):
        self.sess = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/130.0.0.0 Safari/537.36',
        }
        self.sess.headers.update(headers)
        return

    def sendLoginEmail(self, email):
        url = str(base64.b64decode("aHR0cHM6Ly93d3cuc2hha2tlci5haS9hcGkvd3d3L2xvZ2luL3NlbmRMb2dpbkVtYWls"), 'utf-8')

        payload = json.dumps({
            "email": email,
            "cid": "1729494837803rhpeyxbq",
            "redirectUrl": "aHR0cHM6Ly93d3cuc2hha2tlci5haS9tZXNzYWdl"
        })
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'dnt': '1',
            'origin': str(base64.b64decode("aHR0cHM6Ly93d3cuc2hha2tlci5haQ=="), 'utf-8'),
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': str(base64.b64decode("aHR0cHM6Ly93d3cuc2hha2tlci5haS9sb2dpbj9mcm9tPWJyYW5kX2xvZ2luJnJlZGlyZWN0X3VybD0vaG9tZQ=="), 'utf-8'),
            'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)

    def login(self, id):
        try:
            while int(time.time()) - int(self.starttime) < self.expireSeconds:
                mails = server.get_mails(subject='Sign in to Shakker')
                if len(mails) > 0:
                    mail = mails[0]
                    mail_id = mail['id']
                    content_html = mail['content_html']
                    soup = BeautifulSoup(content_html[0], "html.parser")
                    for link in soup.find_all('a'):
                        loginurl = link.get('href')
                        self.sess.get(loginurl, timeout=1000, allow_redirects=True)
                        webid = self.sess.cookies.get_dict().get('webid', '')
                        usertoken = self.sess.cookies.get_dict().get('liblibai_usertoken', '')
                        value = self.get_cookies(usertoken, webid)
                        info = ql_env.get_by_id(id)
                        if info['code'] == 200:
                            data = info['data']
                            name = data['name']
                            remarks = data['remarks']
                            logger.info(f"{remarks}登录")
                            ql_env.update(value, name, id, remarks)
                            ql_env.enable([id])
                            self.send_msg(remarks)
                            server.delete(mail_id)
                            return "登录成功"
                time.sleep(20)
            return "两分钟后未收到邮件"
        except Exception as e:
            logger.error(traceback.format_exc())
            return traceback.format_exc()

    def get_cookies(self, usertoken, webid):
        t = datetime.datetime.now()
        t1 = (t + datetime.timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
        webid_time = time.mktime(time.strptime(t1, '%Y-%m-%d %H:%M:%S'))

        t2 = (t + datetime.timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
        #转为秒级时间戳
        usertoken_time = time.mktime(time.strptime(t2, '%Y-%m-%d %H:%M:%S'))

        cookies = [
            {
                "domain": str(base64.b64decode("d3d3LnNoYWtrZXIuYWk="), 'utf-8'),
                "expirationDate": webid_time,
                "hostOnly": True,
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
                "domain": str(base64.b64decode("d3d3LnNoYWtrZXIuYWk="), 'utf-8'),
                "expirationDate": usertoken_time,
                "hostOnly": True,
                "httpOnly": False,
                "name": "liblibai_usertoken",
                "path": "/",
                "sameSite": None,
                "secure": False,
                "session": False,
                "storeId": None,
                "value": usertoken
            }
        ]
        return json.dumps(cookies, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    shakkerEmailLogin = ShakkerEmailLogin()
    shakkerEmailLogin.sendLoginEmail("scenic-silt-grecian@outlook.com")
    shakkerEmailLogin.login("536")
