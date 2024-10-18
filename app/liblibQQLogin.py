# -*- coding: utf-8 -*-
import base64
import json
import os
import re
import subprocess
import time
import traceback
import uuid
from functools import partial
from random import random
from urllib.parse import urlencode

import requests

from liblibart.ql import ql_env

sourceURL = "https://graph.qq.com/oauth2.0/login_jump"

sessionMap = {}

pattern = re.compile("ptuiCB\('(?P<status>.*?)',(\s+)?'(.*?)',(\s+)?'(?P<url>.*?)',(\s+)?'(.*?)',(\s+)?'(?P<title>.*?)',(\s+)?'(?P<nickname>.*?)'(,(\s+)?(.*?)'\))?;?")

class liblibQQLogin:
    def __init__(self, session_id=None):
        self.sess = None
        self.js_ver = '24091915'
        if session_id is None:
            self.newSession()
            self.session_id = str(uuid.uuid1())
            sessionMap[self.session_id] = self.sess
        else:
            self.session_id = session_id
            self.sess = sessionMap[self.session_id]
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

    def genQRToken(self, qrsig):
        e = 0
        for i in range(0, len(qrsig)):
            e += (e << 5) + ord(qrsig[i])
        qrtoken = (e & 2147483647)
        return str(qrtoken)

    def get_g_tk(self, p_skey):
        h = 5381

        for s in p_skey:
            h += (h << 5) + ord(s)

        return h & 2147483647

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

    def ptuiCB(self, call_str):
        checked = pattern.search(call_str)
        return {
            'status' : checked.group('status'),
            'url' : checked.group('url'),
            'msg' : checked.group('title'),
            'nickname' : checked.group('nickname')
        }

    def qrShow(self):
        url = 'https://xui.ptlogin2.qq.com/cgi-bin/xlogin'
        params = {
            "appid": 716027609,
            "daid": 383,
            "style": 33,
            "login_text": "登录",
            "hide_title_bar": 1,
            "hide_border": 1,
            "target": "self",
            "s_url": sourceURL,
            "pt_3rd_aid": 102049234,
            "pt_feedback_link": "https://support.qq.com/products/77942?customInfo=.appid102049234",
            "theme": 2,
            "verify_theme": ""
        }
        resp = self.sess.get(url, params=params, timeout=1000)
        pattern = r'imgcache\.qq\.com/ptlogin/ver/(\d+)/js'
        try:
            self.js_ver = re.search(pattern, resp.content).group(1)
        except:
            pass
        self.sess.headers.update({'Referer': url})
        url = 'https://ssl.ptlogin2.qq.com/ptqrshow'
        params = {
            "appid": 716027609,
            "e": 2,
            "l": "M",
            "s": 3,
            "d": 72,
            "v": 4,
            "t": '%.17f' % (random()),
            "daid": 383,
            "pt_3rd_aid": 102049234,
            "u1": sourceURL
        }
        resp = self.sess.get(url, params=params, timeout=1000)
        file_name = f'{time.strftime("%Y%m%d%H%M%S")}.jpg'
        path = f'/mitmproxy/logs/{file_name}'
        with open(path, 'wb') as f:
            f.write(resp.content)
        return file_name

    def qrLogin(self, qrsig, login_sig, file_name, id=None):
        try:
            while int(time.time()) - int(self.starttime) < self.expireSeconds:
                url = 'https://ssl.ptlogin2.qq.com/ptqrlogin'
                params = {
                    "u1": sourceURL,
                    "ptqrtoken": self.genQRToken(qrsig),
                    "ptredirect": 0,
                    "h": 1,
                    "t": 1,
                    "g": 1,
                    "from_ui": 1,
                    "ptlang": 2052,
                    "action": '0-0-%d' % (time.time() * 1000),
                    "js_ver": self.js_ver,
                    "js_type": 1,
                    "login_sig": login_sig,
                    "pt_uistyle": 40,
                    "aid": 716027609,
                    "daid": 383,
                    "pt_3rd_aid": 102049234,
                    "o1vId": "531f114a7808a5cfef819c6f7a04c98d",
                    "pt_js_version": "v1.57.0"
                }
                res = self.sess.get(url, params=params, timeout=1000)
                _poll_res = self.ptuiCB(res.text)
                status = _poll_res.get('status')
                url = _poll_res.get('url')
                nickname = _poll_res.get('nickname')
                if status == '0' and url != '':
                    self.sess.get(url, timeout=1000, allow_redirects=True)
                    url = "https://graph.qq.com/oauth2.0/login_jump"
                    self.sess.get(url, timeout=1000, allow_redirects=True)
                    url = "https://graph.qq.com/oauth2.0/authorize"
                    data_dict = {
                        'response_type': 'code',
                        'client_id': '102049234',
                        'redirect_uri': f"{str(base64.b64decode('aHR0cHM6Ly93d3cubGlibGliLmFydC9hcGkvd3d3L2xvZ2luL2xvZ2luQnlRUUFuZFJlZGlyZWN0'), 'utf-8')}?cid=1729157068424hgnvpkyw&platform=undefined",
                        'scope': '',
                        'state': '',
                        'switch': '',
                        'from_ptlogin': '1',
                        'src': '1',
                        'update_auth': '1',
                        'openapi': '1010',
                        'g_tk': self.get_g_tk(self.sess.cookies.get_dict().get('p_skey', '')),
                        'auth_time': int(time.time() * 1000),
                        'ui': '3D5C88EA-A27B-4D14-9A7A-A7804716337E'
                    }
                    self.sess.post(url, timeout=1000, allow_redirects=True, data=urlencode(data_dict))
                    p_uin = self.sess.cookies.get_dict().get('p_uin', '')
                    webid = self.sess.cookies.get_dict().get('webid', '')
                    usertoken = self.sess.cookies.get_dict().get('usertoken', '')
                    value = self.get_cookies(usertoken, webid)
                    if id is not None and id != "" and id != "None":
                        info = ql_env.get_by_id(id)
                        if info['code'] == 200:
                            data = info['data']
                            name = data['name']
                            remarks = data['remarks']
                            ql_env.update(value, name, id, remarks)
                            ql_env.enable([id])
                    else:
                        name = 'liblib_cookie'
                        remarks = f'qq-{p_uin}-{nickname}'
                        res = ql_env.search(remarks)
                        if len(res) > 0:
                            info = res[0]
                            id = info['id']
                            ql_env.update(value, name, id, remarks)
                            ql_env.enable([id])
                        else:
                            ql_env.add(name, value, remarks)
                    break
                time.sleep(2)
        except Exception as e:
            print(traceback.format_exc())
        finally:
            try:
                del sessionMap[self.session_id]
                path = f'/mitmproxy/logs/{file_name}'
                os.remove(path)
            except Exception as e:
                print(traceback.format_exc())
